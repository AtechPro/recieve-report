let uploadedImages = {};
let receivedValveImages = [];
let currentPDFData = null;



function uploadImage(imageType, inputElement) {
    const file = inputElement.files[0];
    
    if (!file) {
        showStatus(imageType + '_status', 'Please select a file first.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('image_type', imageType);

    fetch('/upload-image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showStatus(imageType + '_status', data.message, 'success');
            uploadedImages[imageType] = data.filepath;
            
            // Show preview container
            const container = document.getElementById(imageType + '_container');
            const preview = document.getElementById(imageType + '_preview');
            preview.src = URL.createObjectURL(file);
            if (container) container.style.display = 'block';
        } else {
            showStatus(imageType + '_status', data.error, 'error');
        }
    })
    .catch(error => {
        showStatus(imageType + '_status', 'Upload failed: ' + error.message, 'error');
    });
}

function uploadReceivedValveImage(imageNumber, inputElement) {
    const file = inputElement.files[0];
    if (!file) {
        showStatus('received_valve_' + imageNumber + '_status', 'Please select a file first.', 'error');
        return;
    }
    const formData = new FormData();
    formData.append('image', file);
    formData.append('image_type', 'received_valve_' + imageNumber);

    fetch('/upload-image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showStatus('received_valve_' + imageNumber + '_status', data.message, 'success');
            
            // Store the image in the array at the correct position (0-based index)
            const index = imageNumber - 1;
            receivedValveImages[index] = data.filepath;
            
            // Show preview container
            const container = document.getElementById('received_valve_' + imageNumber + '_container');
            const preview = document.getElementById('received_valve_' + imageNumber + '_preview');
            preview.src = URL.createObjectURL(file);
            if (container) container.style.display = 'block';
        } else {
            showStatus('received_valve_' + imageNumber + '_status', data.error, 'error');
        }
    })
    .catch(error => {
        showStatus('received_valve_' + imageNumber + '_status', 'Upload failed: ' + error.message, 'error');
    });
}

function deleteImage(imageType) {
    // Remove from uploadedImages object
    delete uploadedImages[imageType];
    
    // Hide preview container
    const container = document.getElementById(imageType + '_container');
    if (container) container.style.display = 'none';
    
    // Clear both camera and gallery inputs
    const cameraInput = document.getElementById('camera_input_' + imageType);
    const galleryInput = document.getElementById('gallery_input_' + imageType);
    if (cameraInput) cameraInput.value = '';
    if (galleryInput) galleryInput.value = '';
    
    // Clear status
    const statusDiv = document.getElementById(imageType + '_status');
    statusDiv.innerHTML = '';
    
    showStatus(imageType + '_status', 'Image deleted successfully.', 'success');
}

function deleteReceivedValveImage(imageNumber) {
    // Remove from receivedValveImages array
    const index = imageNumber - 1;
    receivedValveImages[index] = null;
    
    // Hide preview container
    const container = document.getElementById('received_valve_' + imageNumber + '_container');
    if (container) container.style.display = 'none';
    
    // Clear file input
    const fileInput = document.getElementById('received_valve_' + imageNumber);
    fileInput.value = '';
    
    // Clear status
    const statusDiv = document.getElementById('received_valve_' + imageNumber + '_status');
    statusDiv.innerHTML = '';
    
    showStatus('received_valve_' + imageNumber + '_status', 'Image deleted successfully.', 'success');
}

function deletePDF(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"? This action cannot be undone.`)) {
        return;
    }

    fetch(`/delete-pdf/${filename}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Show success message
            alert(data.message);
            // Reload the PDF list to reflect the changes
            loadAvailablePDFs();
        } else {
            alert('Delete failed: ' + data.error);
        }
    })
    .catch(error => {
        alert('Delete failed: ' + error.message);
    });
}

function collectFormData() {
    // Collect all form data for PDF generation, similar to finding_report.html
    const overrideMode = document.getElementById('override_mode')?.checked || false;
    if (overrideMode) {
        // Collect manual values
        const user_data = { client_info: {} };
        user_data.client_info.client = document.getElementById('client_name')?.value || '';
        user_data.client_info.project = document.getElementById('project_name')?.value || '';
        user_data.client_info.location = document.getElementById('location')?.value || '';
        user_data.client_info.date_in = document.getElementById('date_in')?.value || '';
        user_data.client_info.doc_info = document.getElementById('manual_doc_no').value || '';
        user_data.client_info.wo_number = document.getElementById('manual_wo').value || '';
        user_data.client_info.manufacturer = document.getElementById('manual_manufacturer').value || '';
        user_data.client_info.tag_no = document.getElementById('manual_tag_no').value || '';
        user_data.client_info.valve_type = document.getElementById('manual_valve_type').value || '';
        user_data.client_info.valve_operated_type = document.getElementById('manual_valve_operated_type').value || '';
        // Inlet/Outlet fields
        user_data.client_info.size_inlet = document.getElementById('manual_size_inlet').value || '';
        user_data.client_info.inlet_rating = document.getElementById('manual_inlet_rating').value || '';
        user_data.client_info.inlet_type = (function() {
            let val = document.getElementById('inlet_type')?.value || '';
            if (val === 'Other') {
                val = document.getElementById('inlet_type_other')?.value.trim() || '';
            }
            return val;
        })();
        user_data.client_info.size_outlet = document.getElementById('manual_size_outlet').value || '';
        user_data.client_info.outlet_rating = document.getElementById('manual_outlet_rating').value || '';
        user_data.client_info.outlet_type = (function() {
            let val = document.getElementById('outlet_type')?.value || '';
            if (val === 'Other') {
                val = document.getElementById('outlet_type_other')?.value.trim() || '';
            }
            return val;
        })();

        // AS RECEIVED VALVE CONDITION fields from default form (handle 'Other')
        let inletConnectionCondition = document.getElementById('inlet_connection_condition')?.value || '';
        if (inletConnectionCondition === 'Other') {
            inletConnectionCondition = document.getElementById('inlet_connection_condition_other')?.value.trim() || '';
        }
        user_data.client_info.inlet_connection_condition = inletConnectionCondition;

        let outletConnectionCondition = document.getElementById('outlet_connection_condition')?.value || '';
        if (outletConnectionCondition === 'Other') {
            outletConnectionCondition = document.getElementById('outlet_connection_condition_other')?.value.trim() || '';
        }
        user_data.client_info.outlet_connection_condition = outletConnectionCondition;

        let connectionMajorDamage = document.getElementById('connection_major_damage')?.value || '';
        if (connectionMajorDamage === 'Other') {
            connectionMajorDamage = document.getElementById('connection_major_damage_other')?.value.trim() || '';
        }
        user_data.client_info.connection_major_damage = connectionMajorDamage;

        let valveBodyCondition = document.getElementById('valve_body_condition')?.value || '';
        if (valveBodyCondition === 'Other') {
            valveBodyCondition = document.getElementById('valve_body_condition_other')?.value.trim() || '';
        }
        user_data.client_info.valve_body_condition = valveBodyCondition;

        let majorDefectOnBody = document.getElementById('major_defect_on_body')?.value || '';
        if (majorDefectOnBody === 'Other') {
            majorDefectOnBody = document.getElementById('major_defect_on_body_other')?.value.trim() || '';
        }
        user_data.client_info.major_defect_on_body = majorDefectOnBody;

        let overallValveCondition = document.getElementById('overall_valve_condition')?.value || '';
        if (overallValveCondition === 'Other') {
            overallValveCondition = document.getElementById('overall_valve_condition_other')?.value.trim() || '';
        }
        user_data.client_info.overall_valve_condition = overallValveCondition;

        // Transport details
        user_data.client_info.transport_mode = document.getElementById('transport_mode')?.value || '';
        user_data.client_info.packaging = document.getElementById('packaging')?.value || '';
        user_data.client_info.transport_by = document.getElementById('transport_by')?.value || '';
        user_data.client_info.received_by = document.getElementById('received_by')?.value || '';
        user_data.client_info.transport_comment = document.getElementById('transport_comment')?.value || '';

        // Add other fields as needed
        // Compose the rest of the data as before
        const stampSelection = document.getElementById('stamp_selection')?.value || '';
        const stampDate = document.getElementById('stamp_date')?.value.trim() || '';
        const selectedServices = Array.from(document.querySelectorAll('input[name="service_options"]:checked')).map(cb => cb.value);
        const image_files = uploadedImages;
        const received_valve_images = receivedValveImages.filter(img => img);
        return {
            identifier: user_data.client_info.wo_number || '',
            user_data: user_data,
            image_files: image_files,
            received_valve_images: received_valve_images,
            stamp_selection: stampSelection,
            date_value: stampDate || '',
            selected_services: selectedServices,
            override_mode: true
        };
    } else {
        const valveWO = document.getElementById('valve_wo')?.value || '';
        const clientName = document.getElementById('client_name')?.value.trim() || '';
        const projectName = document.getElementById('project_name')?.value.trim() || '';
        const location = document.getElementById('location')?.value.trim() || '';
        const dateIn = document.getElementById('date_in')?.value.trim() || '';
        const transportMode = document.getElementById('transport_mode')?.value.trim() || '';
        const transportBy = document.getElementById('transport_by')?.value.trim() || '';
        const packaging = document.getElementById('packaging')?.value.trim() || '';
        const receivedBy = document.getElementById('received_by')?.value.trim() || '';
        const transportComment = document.getElementById('transport_comment')?.value.trim() || '';
        let inletType = document.getElementById('inlet_type')?.value || '';
        if (inletType === "Other") inletType = document.getElementById('inlet_type_other')?.value.trim() || '';
        let outletType = document.getElementById('outlet_type')?.value || '';
        if (outletType === "Other") outletType = document.getElementById('outlet_type_other')?.value.trim() || '';
        let inletConnectionCondition = document.getElementById('inlet_connection_condition')?.value || '';
        if (inletConnectionCondition === "Other") inletConnectionCondition = document.getElementById('inlet_connection_condition_other')?.value.trim() || '';
        let outletConnectionCondition = document.getElementById('outlet_connection_condition')?.value || '';
        if (outletConnectionCondition === "Other") outletConnectionCondition = document.getElementById('outlet_connection_condition_other')?.value.trim() || '';
        let connectionMajorDamage = document.getElementById('connection_major_damage')?.value || '';
        if (connectionMajorDamage === "Other") connectionMajorDamage = document.getElementById('connection_major_damage_other')?.value.trim() || '';
        let valveBodyCondition = document.getElementById('valve_body_condition')?.value || '';
        if (valveBodyCondition === "Other") valveBodyCondition = document.getElementById('valve_body_condition_other')?.value.trim() || '';
        let majorDefectOnBody = document.getElementById('major_defect_on_body')?.value || '';
        if (majorDefectOnBody === "Other") majorDefectOnBody = document.getElementById('major_defect_on_body_other')?.value.trim() || '';
        let overallValveCondition = document.getElementById('overall_valve_condition')?.value || '';
        if (overallValveCondition === "Other") overallValveCondition = document.getElementById('overall_valve_condition_other')?.value.trim() || '';

        // Get service selections (multiple checkboxes)
        const selectedServices = document.querySelectorAll('input[name="service_options"]:checked');
        const serviceSelections = Array.from(selectedServices).map(checkbox => checkbox.value);

        // Get stamp selection and date
        const stampSelection = document.getElementById('stamp_selection')?.value || '';
        const stampDate = document.getElementById('stamp_date')?.value.trim() || '';

        // Images
        // uploadedImages and receivedValveImages are global variables
        const image_files = uploadedImages;
        const received_valve_images = receivedValveImages.filter(img => img);

        // Compose user_data
        let user_data = null;
        if (
            clientName || projectName || location || dateIn ||
            transportMode || transportBy || packaging || receivedBy ||
            inletType || outletType || inletConnectionCondition || outletConnectionCondition ||
            connectionMajorDamage || valveBodyCondition || majorDefectOnBody || overallValveCondition ||
            transportComment
        ) {
            user_data = { client_info: {} };
            if (clientName) user_data.client_info.client = clientName;
            if (projectName) user_data.client_info.project = projectName;
            if (location) user_data.client_info.location = location;
            if (dateIn) user_data.client_info.date_in = dateIn;
            if (transportMode) user_data.client_info.transport_mode = transportMode;
            if (transportBy) user_data.client_info.transport_by = transportBy;
            if (packaging) user_data.client_info.packaging = packaging;
            if (receivedBy) user_data.client_info.received_by = receivedBy;
            if (transportComment) user_data.client_info.transport_comment = transportComment;
            if (inletType) user_data.client_info.inlet_type = inletType;
            if (outletType) user_data.client_info.outlet_type = outletType;
            if (inletConnectionCondition) user_data.client_info.inlet_connection_condition = inletConnectionCondition;
            if (outletConnectionCondition) user_data.client_info.outlet_connection_condition = outletConnectionCondition;
            if (connectionMajorDamage) user_data.client_info.connection_major_damage = connectionMajorDamage;
            if (valveBodyCondition) user_data.client_info.valve_body_condition = valveBodyCondition;
            if (majorDefectOnBody) user_data.client_info.major_defect_on_body = majorDefectOnBody;
            if (overallValveCondition) user_data.client_info.overall_valve_condition = overallValveCondition;
        }

        // Get override mode
        const overrideMode = document.getElementById('override_mode')?.checked || false;

        // Compose the request data
        return {
            identifier: valveWO,
            user_data: user_data,
            image_files: image_files,
            received_valve_images: received_valve_images,
            stamp_selection: stampSelection,
            date_value: stampDate || '',
            selected_services: serviceSelections,
            override_mode: overrideMode
        };
    }
}

function generatePDF() {
    const requestData = collectFormData();
    if (!requestData.identifier) {
        showStatus('pdf_status', 'Please enter a Work Order (WO) number.', 'error');
        return;
    }
    // Show loading state
    showStatus('pdf_status', 'Generating PDF... Please wait.', 'info');
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showStatus('pdf_status', data.message, 'success');
            currentPDFData = data;

            // Show PDF viewer section
            const pdfViewerSection = document.getElementById('pdf_viewer_section');
            if (pdfViewerSection) {
                pdfViewerSection.style.display = 'block';
            }

            // Load PDF in viewer
            const pdfViewer = document.getElementById('pdf_viewer');
            if (pdfViewer) {
                pdfViewer.src = data.view_url;
            }

            // Scroll to PDF viewer
            if (pdfViewerSection) {
                pdfViewerSection.scrollIntoView({ behavior: 'smooth' });
            }

            // Refresh the PDF list after generating a new PDF
            loadAvailablePDFs();
        } else {
            showStatus('pdf_status', data.error, 'error');
        }
    })
    .catch(error => {
        showStatus('pdf_status', 'Generation failed: ' + error.message, 'error');
    });
}

function downloadPDF() {
    if (currentPDFData && currentPDFData.download_url) {
        window.open(currentPDFData.download_url, '_blank');
    } else {
        alert('No PDF available for download.');
    }
}

function viewPDF() {
    if (currentPDFData && currentPDFData.view_url) {
        window.open(currentPDFData.view_url, '_blank');
    } else {
        alert('No PDF available for viewing.');
    }
}

function loadAvailablePDFs() {
    const container = document.getElementById('pdf_list_container');
    const loading = document.getElementById('pdf_list_loading');
    
    if (loading) loading.style.display = 'block';
    if (container) container.innerHTML = '<div id="pdf_list_loading" style="text-align: center; padding: 20px; color: var(--deep-teal);">Loading available PDFs...</div>';

    fetch('/list-pdfs')
        .then(response => response.json())
        .then(data => {
            if (loading) loading.style.display = 'none';
            
            if (data.pdfs && data.pdfs.length > 0) {
                let html = '<div style="display: grid; gap: 15px;">';
                data.pdfs.forEach(pdf => {
                    const fileSize = (pdf.size / 1024).toFixed(1); // Convert to KB
                    html += `
                        <div style="background: var(--light-gray); padding: 15px; border-radius: 8px; border: 1px solid var(--muted-green);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <strong style="color: var(--deep-teal);">${pdf.filename}</strong>
                                <span style="color: #666; font-size: 0.9rem;">${fileSize} KB</span>
                            </div>
                            <div style="display: flex; gap: 10px; align-items: center;">
                                <button class="btn" onclick="window.open('${pdf.download_url}', '_blank')" style="padding: 8px 16px; font-size: 0.9rem;">
                                    📥 Download
                                </button>
                                <button class="btn btn-secondary" onclick="window.open('${pdf.view_url}', '_blank')" style="padding: 8px 16px; font-size: 0.9rem;">
                                    👁️ View
                                </button>
                                <button class="delete-pdf-btn" onclick="deletePDF('${pdf.filename}')" title="Delete PDF">
                                    ⚠️ Delete
                                </button>
                            </div>
                        </div>
                    `;
                });
                html += '</div>';
                if (container) container.innerHTML = html;
            } else {
                if (container) container.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">No PDF reports available yet. Generate your first report above!</div>';
            }
        })
        .catch(error => {
            if (loading) loading.style.display = 'none';
            if (container) container.innerHTML = '<div style="text-align: center; padding: 20px; color: #dc3545;">Error loading PDFs: ' + error.message + '</div>';
        });
}

function showStatus(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = 'status ' + type;
}

function loadAvailableNumbers() {
    fetch('/available-no')
        .then(response => response.json())
        .then(data => {
            // Populate WO datalist
            const woDatalist = document.getElementById('valve_wo_list');
            woDatalist.innerHTML = '';
            if (data.wo_numbers && data.wo_numbers.length > 0) {
                data.wo_numbers.forEach(wo => {
                    const option = document.createElement('option');
                    option.value = wo;
                    woDatalist.appendChild(option);
                });
            }
        });
}

function setCurrentDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    
    document.getElementById('date_in').value = formattedDate;
    document.getElementById('date_in_calendar').value = today.toISOString().split('T')[0];
}

function setCurrentStampDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    
    document.getElementById('stamp_date').value = formattedDate;
    document.getElementById('stamp_date_calendar').value = today.toISOString().split('T')[0];
}

function updateDateInput() {
    const calendarInput = document.getElementById('date_in_calendar');
    const textInput = document.getElementById('date_in');
    
    if (calendarInput.value) {
        const date = new Date(calendarInput.value);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const formattedDate = `${day}/${month}/${year}`;
        
        textInput.value = formattedDate;
    }
}

function formatDateForDisplay(dateString) {
    if (!dateString) return '';
    
    // Handle dd/mm/yyyy format
    if (dateString.includes('/')) {
        const parts = dateString.split('/');
        if (parts.length === 3) {
            const day = parts[0];
            const month = parts[1];
            const year = parts[2];
            return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        }
    }
    
    return dateString;
}

function parseDateFromDDMMYYYY(dateString) {
    if (!dateString || !dateString.includes('/')) return null;
    
    const parts = dateString.split('/');
    if (parts.length === 3) {
        const day = parseInt(parts[0]);
        const month = parseInt(parts[1]) - 1; // Month is 0-based in JavaScript
        const year = parseInt(parts[2]);
        return new Date(year, month, day);
    }
    return null;
}

function updateCalendarFromText() {
    const textInput = document.getElementById('date_in');
    const calendarInput = document.getElementById('date_in_calendar');
    
    if (textInput.value) {
        const date = parseDateFromDDMMYYYY(textInput.value);
        if (date && !isNaN(date.getTime())) {
            calendarInput.value = date.toISOString().split('T')[0];
        }
    }
}

function updateStampDateInput() {
    const calendarInput = document.getElementById('stamp_date_calendar');
    const textInput = document.getElementById('stamp_date');
    
    if (calendarInput.value) {
        const date = new Date(calendarInput.value);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const formattedDate = `${day}/${month}/${year}`;
        
        textInput.value = formattedDate;
    }
}

function updateCalendarFromStampDate() {
    const textInput = document.getElementById('stamp_date');
    const calendarInput = document.getElementById('stamp_date_calendar');
    
    if (textInput.value) {
        const date = parseDateFromDDMMYYYY(textInput.value);
        if (date && !isNaN(date.getTime())) {
            calendarInput.value = date.toISOString().split('T')[0];
        }
    }
}

function cleanupTempFiles() {
    if (!confirm('Are you sure you want to clean up all temporary files? This will remove all uploaded images and Excel files.')) {
        return;
    }

    fetch('/cleanup-temp', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Cleanup completed successfully!');
            // Clear any uploaded image previews
            const containers = document.querySelectorAll('.image-preview-container');
            containers.forEach(container => {
                container.style.display = 'none';
                const preview = container.querySelector('.image-preview');
                if (preview) {
                    preview.src = '';
                }
            });
            // Clear uploaded images arrays
            uploadedImages = {};
            receivedValveImages = [];
        } else {
            alert('Cleanup failed: ' + data.error);
        }
    })
    .catch(error => {
        alert('Cleanup failed: ' + error.message);
    });
}

function toggleOtherInput(selectId) {
    const select = document.getElementById(selectId);
    const otherInput = document.getElementById(selectId + '_other');
    if (select.value === 'Other') {
        if (otherInput) otherInput.style.display = 'block';
    } else {
        if (otherInput) otherInput.style.display = 'none';
        if (otherInput) otherInput.value = '';
    }
}

function toggleServiceOption(checkbox) {
    const serviceOption = checkbox.closest('.service-option');
    if (checkbox.checked) {
        if (serviceOption) serviceOption.style.background = 'rgba(44, 161, 132, 0.1)';
        if (serviceOption) serviceOption.style.borderColor = 'var(--medium-teal)';
        if (serviceOption) serviceOption.style.transform = 'scale(1.02)';
    } else {
        if (serviceOption) serviceOption.style.background = 'var(--light-gray)';
        if (serviceOption) serviceOption.style.borderColor = 'transparent';
        if (serviceOption) serviceOption.style.transform = 'scale(1)';
    }
}

function toggleOverrideMode() {
    const override = document.getElementById('override_mode').checked;
    document.getElementById('wo_section').style.display = override ? 'none' : '';
    document.getElementById('manual_override_section').style.display = override ? '' : 'none';
}

function triggerCameraInput(identifier) {
    document.getElementById('camera_input_' + identifier).click();
}
function triggerGalleryInput(identifier) {
    document.getElementById('gallery_input_' + identifier).click();
}

window.onload = function() {
    loadAvailableNumbers();
    loadAvailablePDFs();
    
    // Set current date by default
    setCurrentDate();
    setCurrentStampDate();
    toggleOverrideMode(); // Ensure correct visibility on load
};