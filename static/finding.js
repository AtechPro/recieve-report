
let uploadedImages = {};
let receivedValveImages = [];



function generateFindingReport() {
    const override = document.getElementById('override_mode').checked;
    let identifier = '';
    if (override) {
        identifier = document.getElementById('manual_wo')?.value.trim();
    } else {
        identifier = document.getElementById('valve_identifier').value;
    }
    if (!identifier) {
        showStatus('findingReportStatus', override ? 'Please enter a WO number in manual input' : 'Please enter a valve No or WO number', 'error');
        return;
    }
    // Collect all form data
    const formData = collectFormData();
    // Debug: Log the form data being sent
    console.log('Form data being sent:', formData);
    console.log('Date value in form data:', formData.date_value);
    console.log('Date value type:', typeof formData.date_value);
    console.log('Date value length:', formData.date_value ? formData.date_value.length : 'null');

    showStatus('findingReportStatus', 'Generating finding report...', 'info');

    fetch('/generate-finding-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showStatus('findingReportStatus', data.message, 'success');
            loadAvailablePDFs();
            
            // Show download link
            if (data.download_url) {
                const downloadLink = document.createElement('a');
                downloadLink.href = data.download_url;
                downloadLink.textContent = 'Download PDF';
                downloadLink.className = 'btn btn-secondary';
                downloadLink.style.marginTop = '10px';
                downloadLink.style.display = 'inline-block';
                
                const statusDiv = document.getElementById('findingReportStatus');
                statusDiv.appendChild(document.createElement('br'));
                statusDiv.appendChild(downloadLink);
            }
        } else {
            showStatus('findingReportStatus', 'Generation failed: ' + data.error, 'error');
        }
    })
    .catch(error => {
        showStatus('findingReportStatus', 'Generation failed: ' + error.message, 'error');
    });
}

function toggleOverrideMode() {
    const override = document.getElementById('override_mode').checked;
    // Hide/show the WO/No search section
    const woSection = document.querySelector('.valve-selector');
    if (woSection) woSection.style.display = override ? 'none' : '';
    document.getElementById('manual_override_section').style.display = override ? '' : 'none';
}

function loadAvailablePDFs() {
    fetch('/list-pdfs')
        .then(response => response.json())
        .then(data => {
            const pdfList = document.getElementById('pdfList');
            pdfList.innerHTML = '';
            
            if (data.pdfs && data.pdfs.length > 0) {
                data.pdfs.forEach(pdf => {
                    const pdfItem = document.createElement('div');
                    pdfItem.className = 'pdf-item';
                    pdfItem.innerHTML = `
                        <span>${pdf.filename}</span>
                        <div class="pdf-actions">
                            <a href="/view-pdf/${pdf.filename}" target="_blank" class="btn btn-small btn-secondary">View</a>
                            <a href="/download-pdf/${pdf.filename}" class="btn btn-small btn-secondary">Download</a>
                            <button onclick="deletePDF('${pdf.filename}')" class="btn btn-small btn-danger">Delete</button>
                        </div>
                    `;
                    pdfList.appendChild(pdfItem);
                });
            } else {
                pdfList.innerHTML = '<p>No PDFs found</p>';
            }
        })
        .catch(error => {
            console.error('Error loading PDFs:', error);
        });
}

function deletePDF(filename) {
    if (!confirm('Are you sure you want to delete this PDF?')) {
        return;
    }

    fetch(`/delete-pdf/${filename}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            loadAvailablePDFs();
        } else {
            alert('Delete failed: ' + data.error);
        }
    })
    .catch(error => {
        alert('Delete failed: ' + error.message);
    });
}

function showStatus(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = 'status ' + type;
    element.style.display = 'block';
}

function loadAvailableNumbers() {
    fetch('/available-no')
        .then(response => response.json())
        .then(data => {
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

function setCurrentStampDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    
    document.getElementById('stamp_date').value = formattedDate;
    document.getElementById('stamp_date_calendar').value = today.toISOString().split('T')[0];
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

function parseDateFromDDMMYYYY(dateString) {
    if (!dateString || !dateString.includes('/')) return null;
    
    const parts = dateString.split('/');
    if (parts.length === 3) {
        const day = parseInt(parts[0]);
        const month = parseInt(parts[1]) - 1;
        const year = parseInt(parts[2]);
        return new Date(year, month, day);
    }
    return null;
}

function toggleServiceOption(checkbox) {
    const serviceOption = checkbox.closest('.service-option');
    if (checkbox.checked) {
        serviceOption.style.background = 'rgba(44, 161, 132, 0.1)';
        serviceOption.style.borderColor = 'var(--medium-teal)';
        serviceOption.style.transform = 'scale(1.02)';
    } else {
        serviceOption.style.background = 'var(--light-gray)';
        serviceOption.style.borderColor = 'transparent';
        serviceOption.style.transform = 'scale(1)';
    }
}

// Visual Inspection Functions
function addVisualInspectionItem(desc = '', condition = '', actions = '', remarks = '') {
    const container = document.getElementById('visualInspectionContainer');
    const itemId = 'visual_' + Date.now();
    
    const isSpecial = desc === 'NAMEPLATE' || desc === 'GENERAL APPEARANCE';
    
    const itemDiv = document.createElement('div');
    itemDiv.className = 'inspection-item';
    itemDiv.style.cssText = `
        background: var(--light-gray);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid rgba(140, 184, 172, 0.3);
    `;
    
    itemDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="margin: 0; color: var(--deep-teal);">${desc}</h4>
            <!-- Fixed items cannot be removed -->
        </div>
        <div class="form-grid">
            <div class="form-group">
                <label>Condition:</label>
                ${isSpecial
                    ? `<input type="text" class="inspection-condition" value="${condition}" placeholder="e.g., Good, Damaged, Corroded">`
                    : `<select class="inspection-condition" style="min-width: 180px;">
                        <option value="">-- Select --</option>
                        <option value="OK">OK</option>
                        <option value="NOT AVAILABLE">NOT AVAILABLE</option>
                        <option value="NOT VISIBLE">NOT VISIBLE</option>
                        <option value="CORRODED & DIRTY">CORRODED & DIRTY</option>
                        <option value="NOT APPLICABLE">NOT APPLICABLE</option>
                        <option value="IN PLACED">IN PLACED</option>
                        <option value="DIRTY">DIRTY</option>
                        <option value="NOT COMPLETED">NOT COMPLETED</option>
                        <option value="MISSING">MISSING</option>
                        <option value="NEW">NEW</option>
                        <option value="DENTED">DENTED</option>
                    </select>`}
            </div>
            <div class="form-group">
                <label>Actions:</label>
                <select class="actions-select" style="min-width: 180px;">
                    <option value="">-- Select --</option>
                    <option value="SAND DOWN & CLEANING">SAND DOWN & CLEANING</option>
                    <option value="CLEANING">CLEANING</option>
                    <option value="TO REPLACE NEW">TO REPLACE NEW</option>
                    <option value="TO MACHINED">TO MACHINED</option>
                    <option value="TO LAPPING">TO LAPPING</option>
                    <option value="TO BUILD UP & MACHINE">TO BUILD UP & MACHINE</option>
                    <option value="N/A">N/A</option>
                    <option value="CLEANING & NEW PAINTING">CLEANING & NEW PAINTING</option>
                    <option value="TOUCH UP PAINTING">TOUCH UP PAINTING</option>
                </select>
            </div>
            <div class="form-group">
                <label>Remarks:</label>
                <select class="remarks-select" style="min-width: 160px;">
                    <option value="">-- Select --</option>
                    <option value="REUSEABLE">REUSEABLE</option>
                    <option value="BADLY DAMAGED">BADLY DAMAGED</option>
                    <option value="NEED TO REPLACED">NEED TO REPLACED</option>
                    <option value="NO SPARE KIT">NO SPARE KIT</option>
                    <option value="N/A">N/A</option>
                    <option value="TO FABRICATE">TO FABRICATE</option>
                </select>
            </div>
        </div>
    `;
    
    // Add event listeners for selects
    setTimeout(() => {
        const remarksSelect = itemDiv.querySelector('.remarks-select');
        remarksSelect.addEventListener('change', function() {
            remarksSelect.setAttribute('data-selected', this.value);
        });
        const actionsSelect = itemDiv.querySelector('.actions-select');
        actionsSelect.value = actions;
        actionsSelect.addEventListener('change', function() {
            actionsSelect.setAttribute('data-selected', this.value);
        });
        if (!isSpecial) {
            const conditionSelect = itemDiv.querySelector('.inspection-condition');
            conditionSelect.value = condition;
        }
    }, 0);
    
    container.appendChild(itemDiv);
}

// Internal Inspection Functions
function addInternalInspectionItem(desc = '', condition = '', actions = '', remarks = '') {
    const container = document.getElementById('internalInspectionContainer');
    const itemId = 'internal_' + Date.now();
    
    const itemDiv = document.createElement('div');
    itemDiv.className = 'inspection-item';
    itemDiv.style.cssText = `
        background: var(--light-gray);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid rgba(140, 184, 172, 0.3);
    `;
    
    itemDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="margin: 0; color: var(--deep-teal);">${desc}</h4>
            <!-- Fixed items cannot be removed -->
        </div>
        <div class="form-grid">
            <div class="form-group">
                <label>Condition:</label>
                <select class="inspection-condition">
                    <option value="">-- Select --</option>
                    <option value="MISSING">MISSING</option>
                    <option value="LOOSED">LOOSED</option>
                    <option value="OK">OK</option>
                    <option value="WORN OUT">WORN OUT</option>
                    <option value="MINOR SCRATCH">MINOR SCRATCH</option>
                    <option value="MAJOR SCRATCH">MAJOR SCRATCH</option>
                    <option value="NOT AVAILABLE">NOT AVAILABLE</option>
                    <option value="NOT VISIBLE">NOT VISIBLE</option>
                    <option value="DIRTY">DIRTY</option>
                    <option value="CORRODED">CORRODED</option>
                    <option value="NOT APPLICABLE">NOT APPLICABLE</option>
                    <option value="IN PLACED">IN PLACED</option>
                    <option value="DENTED">DENTED</option>
                    <option value="DAMAGED">DAMAGED</option>
                </select>
            </div>
            <div class="form-group">
                <label>Actions:</label>
                <select class="inspection-actions" style="min-width: 180px;">
                    <option value="">-- Select --</option>
                    <option value="SAND DOWN & CLEANING">SAND DOWN & CLEANING</option>
                    <option value="CLEANING">CLEANING</option>
                    <option value="TO REPLACE NEW">TO REPLACE NEW</option>
                    <option value="TO MACHINED">TO MACHINED</option>
                    <option value="TO LAPPED">TO LAPPED</option>
                    <option value="TO BUILD UP & MACHINE">TO BUILD UP & MACHINE</option>
                    <option value="NOT APPLICABLE">NOT APPLICABLE</option>
                </select>
            </div>
            <div class="form-group">
                <label>Remarks:</label>
                <select class="inspection-remarks" style="min-width: 160px;">
                    <option value="">-- Select --</option>
                    <option value="REUSEABLE">REUSEABLE</option>
                    <option value="BADLY DAMAGED">BADLY DAMAGED</option>
                    <option value="NEED TO REPLACED">NEED TO REPLACED</option>
                    <option value="NO SPARE KIT">NO SPARE KIT</option>
                    <option value="N/A">N/A</option>
                    <option value="TO FABRICATE">TO FABRICATE</option>
                </select>
            </div>
        </div>
    `;
    
    // Set the value if provided
    setTimeout(() => {
        const actionsSelect = itemDiv.querySelector('.inspection-actions');
        actionsSelect.value = actions;
    }, 0);
    
    container.appendChild(itemDiv);
}

// Detailed Pictures Functions
function addDetailedPictureItem(item = '', finding = '', proposedAction = '', imagePath1 = '', imagePath2 = '') {
    const container = document.getElementById('detailedPicturesContainer');
    const itemId = 'picture_' + Date.now();
    
    const itemDiv = document.createElement('div');
    itemDiv.className = 'picture-item';
    itemDiv.style.cssText = `
        background: var(--light-gray);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid rgba(140, 184, 172, 0.3);
    `;
    
    itemDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="margin: 0; color: var(--deep-teal);">${item}</h4>
            <!-- Fixed items cannot be removed -->
        </div>
        <div class="form-grid">
            <div class="form-group">
                <label>Finding:</label>
                <input type="text" class="picture-finding" value="${finding}" placeholder="Describe the finding">
            </div>
            <div class="form-group">
                <label>Proposed Action:</label>
                <input type="text" class="picture-proposed-action" value="${proposedAction}" placeholder="Describe proposed action">
            </div>
        </div>
        <div class="form-grid">
            <div class="form-group">
                <label>Image 1:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="captureImage(this, 1)">
                        📷 Camera
                    </button>
                    <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="selectFromGallery(this, 1)">
                        🖼️ Gallery
                    </button>
                    <button type="button" class="btn btn-danger" style="padding: 8px 12px; font-size: 12px;" onclick="deleteImage(this, 1)">
                        🗑️ Delete
                    </button>
                </div>
                <input type="file" class="picture-image-1" accept="image/*" capture="environment" style="display: none;" onchange="handlePictureUpload(this, 1)">
                <input type="hidden" class="picture-image-path-1" value="${imagePath1}">
                <div class="image-preview-1" style="margin-top: 10px;"></div>
            </div>
            <div class="form-group">
                <label>Image 2:</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="captureImage(this, 2)">
                        📷 Camera
                    </button>
                    <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="selectFromGallery(this, 2)">
                        🖼️ Gallery
                    </button>
                    <button type="button" class="btn btn-danger" style="padding: 8px 12px; font-size: 12px;" onclick="deleteImage(this, 2)">
                        🗑️ Delete
                    </button>
                </div>
                <input type="file" class="picture-image-2" accept="image/*" capture="environment" style="display: none;" onchange="handlePictureUpload(this, 2)">
                <input type="hidden" class="picture-image-path-2" value="${imagePath2}">
                <div class="image-preview-2" style="margin-top: 10px;"></div>
            </div>
        </div>
    `;
    
    container.appendChild(itemDiv);
}

function removeInspectionItem(button) {
    button.closest('.inspection-item, .picture-item').remove();
}

function captureImage(button, imageNum) {
    const fileInput = button.closest('.form-group').querySelector(`.picture-image-${imageNum}`);
    fileInput.setAttribute('capture', 'environment');
    fileInput.click();
}

function selectFromGallery(button, imageNum) {
    const fileInput = button.closest('.form-group').querySelector(`.picture-image-${imageNum}`);
    fileInput.removeAttribute('capture');
    fileInput.click();
}

function deleteImage(button, imageNum) {
    const formGroup = button.closest('.form-group');
    const hiddenInput = formGroup.querySelector(`.picture-image-path-${imageNum}`);
    const fileInput = formGroup.querySelector(`.picture-image-${imageNum}`);
    const previewDiv = formGroup.querySelector(`.image-preview-${imageNum}`);
    
    // Clear the file input
    fileInput.value = '';
    
    // Clear the hidden path
    hiddenInput.value = '';
    
    // Clear the preview
    previewDiv.innerHTML = '';
    
    console.log(`Image ${imageNum} deleted`);
}

function handlePictureUpload(input, imageNum) {
    const file = input.files[0];
    if (!file) return;

    // Show preview immediately
    const formGroup = input.closest('.form-group');
    const previewDiv = formGroup.querySelector(`.image-preview-${imageNum}`);
    
    const reader = new FileReader();
    reader.onload = function(e) {
        previewDiv.innerHTML = `
            <img src="${e.target.result}" style="max-width: 150px; max-height: 100px; border-radius: 8px; border: 2px solid var(--muted-green);">
        `;
    };
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append('image', file);
    formData.append('image_type', `picture_${imageNum}`);

    fetch('/upload-image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Store the filepath in the hidden input
            const hiddenInput = formGroup.querySelector(`.picture-image-path-${imageNum}`);
            hiddenInput.value = data.filepath;
            console.log(`Image ${imageNum} uploaded:`, data.filepath);
        } else {
            alert('Image upload failed: ' + data.error);
            // Remove preview if upload failed
            previewDiv.innerHTML = '';
        }
    })
    .catch(error => {
        alert('Image upload failed: ' + error.message);
        // Remove preview if upload failed
        previewDiv.innerHTML = '';
    });
}

function toggleOtherInput(type) {
    const select = document.getElementById(type);
    const otherInput = document.getElementById(type + '_other');
    if (select.value === "Other") {
        otherInput.style.display = '';
    } else {
        otherInput.style.display = 'none';
        otherInput.value = '';
    }
}

function collectFormData() {
    const override = document.getElementById('override_mode').checked;
    let identifier = '';
    if (override) {
        identifier = document.getElementById('manual_wo')?.value.trim();
    } else {
        identifier = document.getElementById('valve_identifier').value;
    }
    if (!identifier) {
        showStatus('findingReportStatus', override ? 'Please enter a WO number in manual input' : 'Please enter a valve No or WO number', 'error');
        return;
    }
    const dateValue = document.getElementById('stamp_date').value;
    let finalDateValue = dateValue;
    if (!dateValue || dateValue.trim() === '') {
        const today = new Date();
        const day = String(today.getDate()).padStart(2, '0');
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const year = today.getFullYear();
        finalDateValue = `${day}/${month}/${year}`;
    }
    const dateInValue = document.getElementById('date_in').value;
    let inletType = document.getElementById('inlet_type').value;
    if (inletType === "Other") inletType = document.getElementById('inlet_type_other').value.trim();
    let outletType = document.getElementById('outlet_type').value;
    if (outletType === "Other") outletType = document.getElementById('outlet_type_other').value.trim();

    let client_info = {};
    if (override) {
        // Use manual override fields if present, else fallback to main fields
        client_info = {
            client: document.getElementById('client_name')?.value.trim() || 'PETRONAS CHEMICALS FERTILISER SABAH SDN BHD',
            project: document.getElementById('project_name')?.value.trim() || 'VALVE MAINTENANCE PROJECT 2025',
            location: document.getElementById('location')?.value.trim() || 'Sipitang',
            date_in: dateInValue,
            inlet_type: inletType,
            outlet_type: outletType,
            doc_info: document.getElementById('manual_doc_no')?.value.trim() || '',
            size_inlet: document.getElementById('manual_size_inlet')?.value.trim() || '',
            inlet_rating: document.getElementById('manual_inlet_rating')?.value.trim() || '',
            size_outlet: document.getElementById('manual_size_outlet')?.value.trim() || '',
            outlet_rating: document.getElementById('manual_outlet_rating')?.value.trim() || '',
            wo_number: document.getElementById('manual_wo')?.value.trim() || '',
            manufacturer: document.getElementById('manual_manufacturer')?.value.trim() || '',
            tag_no: document.getElementById('manual_tag_no')?.value.trim() || '',
            valve_type: document.getElementById('manual_valve_type')?.value.trim() || '',
            valve_operated_type: document.getElementById('manual_valve_operated_type')?.value.trim() || ''
        };
    } else {
        client_info = {
            client: document.getElementById('client_name')?.value.trim() || 'PETRONAS CHEMICALS FERTILISER SABAH SDN BHD',
            project: document.getElementById('project_name')?.value.trim() || 'VALVE MAINTENANCE PROJECT 2025',
            location: document.getElementById('location')?.value.trim() || 'Sipitang',
            date_in: dateInValue,
            inlet_type: inletType,
            outlet_type: outletType
        };
    }

    const data = {
        identifier: identifier,
        override_mode: override,
        stamp_selection: document.getElementById('stamp_selection').value,
        date_value: finalDateValue,
        selected_services: Array.from(document.querySelectorAll('.service-option input[type="checkbox"]:checked')).map(cb => cb.value),
        comment: document.getElementById('additional_comment').value,
        client_info: client_info,
        pretest: {
            type_test: document.getElementById('type_test').value,
            test_medium: document.getElementById('test_medium').value,
            shell: {
                pressure: document.getElementById('shell_pressure').value,
                duration: document.getElementById('shell_duration').value,
                result_remarks: document.getElementById('shell_result').value
            },
            backseat: {
                pressure: document.getElementById('backseat_pressure').value,
                duration: document.getElementById('backseat_duration').value,
                result_remarks: document.getElementById('backseat_result').value
            },
            seat: {
                pressure: document.getElementById('seat_pressure').value,
                duration: document.getElementById('seat_duration').value,
                result_remarks: document.getElementById('seat_result').value
            },
            test_accordance_to: document.getElementById('test_accordance_to').value
        },
        visual_inspection: [],
        internal_inspection: [],
        detailed_pictures: []
    };
    // Collect visual inspection data
    document.querySelectorAll('#visualInspectionContainer .inspection-item').forEach(item => {
        const descElement = item.querySelector('h4');
        data.visual_inspection.push({
            desc: descElement ? descElement.textContent : '',
            condition: item.querySelector('.inspection-condition') ? item.querySelector('.inspection-condition').value : '',
            actions: item.querySelector('.actions-select') ? item.querySelector('.actions-select').getAttribute('data-selected') || item.querySelector('.actions-select').value : '',
            remarks: item.querySelector('.remarks-select') ? item.querySelector('.remarks-select').getAttribute('data-selected') || item.querySelector('.remarks-select').value : ''
        });
    });
    // Collect internal inspection data
    document.querySelectorAll('#internalInspectionContainer .inspection-item').forEach(item => {
        const descElement = item.querySelector('h4');
        data.internal_inspection.push({
            desc: descElement ? descElement.textContent : '',
            condition: item.querySelector('.inspection-condition') ? item.querySelector('.inspection-condition').value : '',
            actions: item.querySelector('.inspection-actions') ? item.querySelector('.inspection-actions').value : '',
            remarks: item.querySelector('.inspection-remarks') ? item.querySelector('.inspection-remarks').value : ''
        });
    });
    // Collect detailed pictures data
    document.querySelectorAll('#detailedPicturesContainer .picture-item').forEach(item => {
        const imagePath1Input = item.querySelector('.picture-image-path-1');
        const imagePath2Input = item.querySelector('.picture-image-path-2');
        data.detailed_pictures.push({
            item: item.querySelector('.picture-item-name') ? item.querySelector('.picture-item-name').value : '',
            finding: item.querySelector('.picture-finding') ? item.querySelector('.picture-finding').value : '',
            proposed_action: item.querySelector('.picture-proposed-action') ? item.querySelector('.picture-proposed-action').value : '',
            image_path_1: imagePath1Input ? imagePath1Input.value : '',
            image_path_2: imagePath2Input ? imagePath2Input.value : ''
        });
    });
    return data;
}

window.onload = function() {
    loadAvailableNumbers();
    loadAvailablePDFs();
    setCurrentStampDate();
    // Set default value for Date In
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    document.getElementById('date_in').value = formattedDate;
    document.getElementById('date_in_calendar').value = today.toISOString().split('T')[0];
    
    // Debug: Check if date is set correctly
    setTimeout(() => {
        const dateValue = document.getElementById('stamp_date').value;
        console.log('Date value after setCurrentStampDate:', dateValue);
    }, 100);
    
    // Add default visual inspection items with fixed descriptions
    addVisualInspectionItem('GENERAL APPEARANCE', '', '', '');
    addVisualInspectionItem('NAMEPLATE', '', '', '');
    addVisualInspectionItem('OVERALL FLANGE/CONNECTION CONDITION', '', '', '');
    addVisualInspectionItem('BODY', '', '', '');
    addVisualInspectionItem('BONNET', '', '', '');
    addVisualInspectionItem('YOKE', '', '', '');
    addVisualInspectionItem('DISC', '', '', '');
    addVisualInspectionItem('SEAT', '', '', '');
    addVisualInspectionItem('BONNET GASKET', '', '', '');
    
    // Add default internal inspection items with fixed descriptions
    addInternalInspectionItem('BODY', '', '', '');
    addInternalInspectionItem('BONNET', '', '', '');
    addInternalInspectionItem('YOKE', '', '', '');
    addInternalInspectionItem('DISC', '', '', '');
    addInternalInspectionItem('SEAT', '', '', '');
    addInternalInspectionItem('BONNET GASKET', '', '', '');
    addInternalInspectionItem('STEM', '', '', '');
    addInternalInspectionItem('WHEEL NUT', '', '', '');
    addInternalInspectionItem('PACKING', '', '', '');
    addInternalInspectionItem('GLAND BUSHING', '', '', '');
    addInternalInspectionItem('BACK SEAT', '', '', '');
    addInternalInspectionItem('GLAND NUT', '', '', '');
    
    // Add exactly 3 fixed picture items
    addDetailedPictureItem('ITEM 1', '', '', '', '');
    addDetailedPictureItem('ITEM 2', '', '', '', '');
    addDetailedPictureItem('ITEM 3', '', '', '', '');
};
// Add sync functions for Date In
function updateDateInInput() {
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
function updateCalendarFromDateIn() {
    const textInput = document.getElementById('date_in');
    const calendarInput = document.getElementById('date_in_calendar');
    if (textInput.value) {
        const date = parseDateFromDDMMYYYY(textInput.value);
        if (date && !isNaN(date.getTime())) {
            calendarInput.value = date.toISOString().split('T')[0];
        }
    }
}
