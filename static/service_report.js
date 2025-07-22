let uploadedImages = {};
let selectedServices = [];

// Visual inspection items
const visualInspectionItems = [
    "GENERAL APPEARANCE",
    "NAMEPLATE",
    "OVERALL FLANGE/CONNECTION CONDITION",
    "BODY",
    "BONNET",
    "YOKE",
    "DISC",
    "SEAT",
    "BONNET GASKET"
];

// Internal inspection items
const internalInspectionItems = [
    "BODY",
    "BONNET",
    "YOKE",
    "DISC",
    "SEAT",
    "BONNET GASKET",
    "STEM",
    "WHEEL NUT",
    "PACKING",
    "GLAND BUSHING",
    "BACK SEAT",
    "GLAND NUT"
];

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadValveData();
    generateVisualInspectionTable();
    generateInternalInspectionTable();
    generateDetailedPicturesContainer();
    loadPdfList();
    setCurrentStampDate();
    setCurrentDateIn();
});

function setCurrentStampDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    
    document.getElementById('stamp_date').value = formattedDate;
    document.getElementById('stamp_date_calendar').value = today.toISOString().split('T')[0];
}

function setCurrentDateIn() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    
    document.getElementById('date_in').value = formattedDate;
    document.getElementById('date_in_calendar').value = today.toISOString().split('T')[0];
}

function loadValveData() {
    fetch('/get-converted-data')
        .then(response => response.json())
        .then(data => {
            const datalist = document.getElementById('valve_wo_list');
            datalist.innerHTML = '';
            
            data.data.forEach(record => {
                const noOption = document.createElement('option');
                noOption.value = record.No || '';
                datalist.appendChild(noOption);
                
                if (record['WO ']) {
                    const woOption = document.createElement('option');
                    woOption.value = record['WO '];
                    datalist.appendChild(woOption);
                }
            });
        })
        .catch(error => {
            console.error('Error loading valve data:', error);
        });
}

function generateVisualInspectionTable() {
    const tbody = document.getElementById('visualInspectionTable');
    tbody.innerHTML = '';
    
    visualInspectionItems.forEach(item => {
        const isSpecial = item === 'NAMEPLATE' || item === 'GENERAL APPEARANCE';
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item}</td>
            <td>
                ${isSpecial 
                    ? '<input type="text" placeholder="e.g., Good, Damaged, Corroded">'
                    : `<select style="width: 100%; padding: 8px 12px; border: 1px solid var(--light-gray-2); border-radius: 4px; font-size: 0.9rem;">
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
            </td>
            <td>
                <select style="width: 100%; padding: 8px 12px; border: 1px solid var(--light-gray-2); border-radius: 4px; font-size: 0.9rem;">
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
            </td>
            <td>
                <select style="width: 100%; padding: 8px 12px; border: 1px solid var(--light-gray-2); border-radius: 4px; font-size: 0.9rem;">
                    <option value="">-- Select --</option>
                    <option value="CLEANED">CLEANED</option>
                    <option value="NO SPARE">NO SPARE</option>
                    <option value="SERVICED & CLEANED">SERVICED & CLEANED</option>
                    <option value="N/A">N/A</option>
                    <option value="NEW">NEW</option>
                    <option value="REUSED">REUSED</option>
                </select>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function generateInternalInspectionTable() {
    const tbody = document.getElementById('internalInspectionTable');
    tbody.innerHTML = '';
    
    internalInspectionItems.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item}</td>
            <td>
                <select style="width: 100%; padding: 8px 12px; border: 1px solid var(--light-gray-2); border-radius: 4px; font-size: 0.9rem;">
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
            </td>
            <td>
                <select style="width: 100%; padding: 8px 12px; border: 1px solid var(--light-gray-2); border-radius: 4px; font-size: 0.9rem;">
                    <option value="">-- Select --</option>
                    <option value="CLEANED">CLEANED</option>
                    <option value="NO SPARE">NO SPARE</option>
                    <option value="SERVICED & CLEANED">SERVICED & CLEANED</option>
                    <option value="N/A">N/A</option>
                    <option value="NEW">NEW</option>
                    <option value="REUSED">REUSED</option>
                </select>
            </td>
            <td>
                <select style="width: 100%; padding: 8px 12px; border: 1px solid var(--light-gray-2); border-radius: 4px; font-size: 0.9rem;">
                    <option value="">-- Select --</option>
                    <option value="CLEANED">CLEANED</option>
                    <option value="NO SPARE">NO SPARE</option>
                    <option value="SERVICED & CLEANED">SERVICED & CLEANED</option>
                    <option value="N/A">N/A</option>
                    <option value="NEW">NEW</option>
                    <option value="REUSED">REUSED</option>
                </select>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function generateDetailedPicturesContainer() {
    const container = document.getElementById('detailedPicturesContainer');
    container.innerHTML = '';
    
    for (let i = 0; i < 4; i++) {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'upload-section';
        itemDiv.style.margin = '15px 0';
        itemDiv.innerHTML = `
            <h3 style="color: var(--deep-teal); margin: 0 0 15px 0;">Item ${i + 1}</h3>
            <div class="form-group">
                <label for="proposed_action_${i}">Proposed Action:</label>
                <textarea id="proposed_action_${i}" rows="3" placeholder="Describe the proposed action or service performed..." style="width: 100%; padding: 12px 16px; border: 2px solid var(--light-gray-2); border-radius: 8px; font-size: 14px; font-family: inherit; resize: vertical;"></textarea>
            </div>
            <div class="image-upload-container">
                <div class="form-group">
                    <label>Image 1:</label>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="captureImage(this, ${i}, 1)">
                            📷 Camera
                        </button>
                        <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="selectFromGallery(this, ${i}, 1)">
                            🖼️ Gallery
                        </button>
                        <button type="button" class="btn btn-danger" style="padding: 8px 12px; font-size: 12px;" onclick="deleteImage(${i}, 1)">
                            🗑️ Delete
                        </button>
                    </div>
                    <input type="file" id="image_${i}_1" accept="image/*" capture="environment" style="display: none;" onchange="handleImageUpload(this, ${i}, 1)">
                    <div id="image_preview_${i}_1" style="margin-top: 10px;"></div>
                </div>
                <div class="form-group">
                    <label>Image 2:</label>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="captureImage(this, ${i}, 2)">
                            📷 Camera
                        </button>
                        <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="selectFromGallery(this, ${i}, 2)">
                            🖼️ Gallery
                        </button>
                        <button type="button" class="btn btn-danger" style="padding: 8px 12px; font-size: 12px;" onclick="deleteImage(${i}, 2)">
                            🗑️ Delete
                        </button>
                    </div>
                    <input type="file" id="image_${i}_2" accept="image/*" capture="environment" style="display: none;" onchange="handleImageUpload(this, ${i}, 2)">
                    <div id="image_preview_${i}_2" style="margin-top: 10px;"></div>
                </div>
                <div class="form-group">
                    <label>Image 3:</label>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="captureImage(this, ${i}, 3)">
                            📷 Camera
                        </button>
                        <button type="button" class="btn btn-secondary" style="padding: 8px 12px; font-size: 12px;" onclick="selectFromGallery(this, ${i}, 3)">
                            🖼️ Gallery
                        </button>
                        <button type="button" class="btn btn-danger" style="padding: 8px 12px; font-size: 12px;" onclick="deleteImage(${i}, 3)">
                            🗑️ Delete
                        </button>
                    </div>
                    <input type="file" id="image_${i}_3" accept="image/*" capture="environment" style="display: none;" onchange="handleImageUpload(this, ${i}, 3)">
                    <div id="image_preview_${i}_3" style="margin-top: 10px;"></div>
                </div>
            </div>
        `;
        container.appendChild(itemDiv);
    }
}

function handleImageUpload(input, itemIndex, imageIndex) {
    const file = input.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('image_type', `detailed_picture_${itemIndex}_${imageIndex}`);

        fetch('/upload-image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Store the filepath for later use
                if (!uploadedImages[itemIndex]) {
                    uploadedImages[itemIndex] = {};
                }
                uploadedImages[itemIndex][`image_path_${imageIndex}`] = data.filepath;
                
                // Show preview
                const previewDiv = document.getElementById(`image_preview_${itemIndex}_${imageIndex}`);
                previewDiv.innerHTML = `
                    <div class="image-preview" style="position: relative; display: inline-block; margin-top: 10px;">
                        <img src="${URL.createObjectURL(file)}" alt="Uploaded image" style="max-width: 120px; max-height: 80px; border-radius: 6px; border: 2px solid var(--medium-teal);">
                        <button class="remove-image" onclick="removeImage(${itemIndex}, ${imageIndex})" style="position: absolute; top: -8px; right: -8px; background: #dc3545; color: white; border: none; border-radius: 50%; width: 24px; height: 24px; cursor: pointer; font-size: 14px; font-weight: bold; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">×</button>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error uploading image:', error);
        });
    }
}

function removeImage(itemIndex, imageIndex) {
    if (uploadedImages[itemIndex] && uploadedImages[itemIndex][`image_path_${imageIndex}`]) {
        delete uploadedImages[itemIndex][`image_path_${imageIndex}`];
    }
    
    const previewDiv = document.getElementById(`image_preview_${itemIndex}_${imageIndex}`);
    previewDiv.innerHTML = '';
    
    // Reset the file input
    document.getElementById(`image_${itemIndex}_${imageIndex}`).value = '';
}

function captureImage(button, itemIndex, imageIndex) {
    const fileInput = document.getElementById(`image_${itemIndex}_${imageIndex}`);
    fileInput.setAttribute('capture', 'environment');
    fileInput.click();
}

function selectFromGallery(button, itemIndex, imageIndex) {
    const fileInput = document.getElementById(`image_${itemIndex}_${imageIndex}`);
    fileInput.removeAttribute('capture');
    fileInput.click();
}

function deleteImage(itemIndex, imageIndex) {
    if (uploadedImages[itemIndex] && uploadedImages[itemIndex][`image_path_${imageIndex}`]) {
        delete uploadedImages[itemIndex][`image_path_${imageIndex}`];
    }
    
    const previewDiv = document.getElementById(`image_preview_${itemIndex}_${imageIndex}`);
    previewDiv.innerHTML = '';
    
    // Reset the file input
    document.getElementById(`image_${itemIndex}_${imageIndex}`).value = '';
}

function toggleServiceOption(checkbox) {
    if (checkbox.checked) {
        selectedServices.push(checkbox.value);
    } else {
        const index = selectedServices.indexOf(checkbox.value);
        if (index > -1) {
            selectedServices.splice(index, 1);
        }
    }
}

function toggleOverrideMode() {
    const overrideCheckbox = document.getElementById('override_mode');
    const manualSection = document.getElementById('manual_override_section');
    if (overrideCheckbox.checked) {
        manualSection.style.display = '';
    } else {
        manualSection.style.display = 'none';
    }
}

function collectManualOverrideData() {
    return {
        doc_info: document.getElementById('manual_doc_no').value,
        size_inlet: document.getElementById('manual_size_inlet').value,
        inlet_rating: document.getElementById('manual_inlet_rating').value,
        size_outlet: document.getElementById('manual_size_outlet').value,
        outlet_rating: document.getElementById('manual_outlet_rating').value,
        wo_number: document.getElementById('manual_wo').value,
        manufacturer: document.getElementById('manual_manufacturer').value,
        tag_no: document.getElementById('manual_tag_no').value,
        valve_type: document.getElementById('manual_valve_type').value,
        valve_operated_type: document.getElementById('manual_valve_operated_type').value
    };
}

function updateCalendarFromDateIn() {
    const dateInput = document.getElementById('date_in');
    const calendarInput = document.getElementById('date_in_calendar');
    const date = parseDate(dateInput.value);
    if (date) {
        calendarInput.value = date.toISOString().split('T')[0];
    }
}

function updateDateInInput() {
    const dateInput = document.getElementById('date_in');
    const calendarInput = document.getElementById('date_in_calendar');
    const date = new Date(calendarInput.value);
    if (!isNaN(date.getTime())) {
        dateInput.value = formatDate(date);
    }
}

function updateCalendarFromStampDate() {
    const dateInput = document.getElementById('stamp_date');
    const calendarInput = document.getElementById('stamp_date_calendar');
    const date = parseDate(dateInput.value);
    if (date) {
        calendarInput.value = date.toISOString().split('T')[0];
    }
}

function updateStampDateInput() {
    const dateInput = document.getElementById('stamp_date');
    const calendarInput = document.getElementById('stamp_date_calendar');
    const date = new Date(calendarInput.value);
    if (!isNaN(date.getTime())) {
        dateInput.value = formatDate(date);
    }
}

function parseDate(dateString) {
    if (!dateString) return null;
    const parts = dateString.split('/');
    if (parts.length === 3) {
        return new Date(parts[2], parts[1] - 1, parts[0]);
    }
    return null;
}

function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
}

function collectVisualInspectionData() {
    const rows = document.getElementById('visualInspectionTable').getElementsByTagName('tr');
    const data = [];
    
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        if (cells.length >= 4) {
            const conditionElement = cells[1].querySelector('input, select');
            const actionsElement = cells[2].querySelector('select');
            const remarksElement = cells[3].querySelector('select');
            
            data.push({
                desc: visualInspectionItems[i],
                condition: conditionElement ? conditionElement.value : '',
                actions: actionsElement ? actionsElement.value : '',
                remarks: remarksElement ? remarksElement.value : ''
            });
        }
    }
    
    return data;
}

function collectInternalInspectionData() {
    const rows = document.getElementById('internalInspectionTable').getElementsByTagName('tr');
    const data = [];
    
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        if (cells.length >= 4) {
            const conditionElement = cells[1].querySelector('select');
            const actionsElement = cells[2].querySelector('select');
            const remarksElement = cells[3].querySelector('select');
            
            data.push({
                desc: internalInspectionItems[i],
                condition: conditionElement ? conditionElement.value : '',
                actions: actionsElement ? actionsElement.value : '',
                remarks: remarksElement ? remarksElement.value : ''
            });
        }
    }
    
    return data;
}

function collectDetailedPicturesData() {
    const data = [];
    
    for (let i = 0; i < 4; i++) {
        const proposedAction = document.getElementById(`proposed_action_${i}`).value;
        const itemData = {
            proposed_action: proposedAction,
            image_path_1: '',
            image_path_2: '',
            image_path_3: ''
        };
        
        if (uploadedImages[i]) {
            if (uploadedImages[i].image_path_1) itemData.image_path_1 = uploadedImages[i].image_path_1;
            if (uploadedImages[i].image_path_2) itemData.image_path_2 = uploadedImages[i].image_path_2;
            if (uploadedImages[i].image_path_3) itemData.image_path_3 = uploadedImages[i].image_path_3;
        }
        
        data.push(itemData);
    }
    
    return data;
}

function generateServiceReport() {
    const overrideMode = document.getElementById('override_mode').checked;
    let identifier = '';
    if (overrideMode) {
        identifier = document.getElementById('manual_wo')?.value.trim();
    } else {
        identifier = document.getElementById('valve_identifier').value;
    }
    if (!identifier) {
        showStatus('Please enter a ' + (overrideMode ? 'WO number in manual input' : 'valve No or WO number') + '.', 'error');
        return;
    }
    const stampDate = document.getElementById('stamp_date').value;
    let finalDateValue = stampDate;
    if (!stampDate || stampDate.trim() === '') {
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
    let clientInfo = {};
    if (overrideMode) {
        clientInfo = {
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
        clientInfo = {
            client: document.getElementById('client_name')?.value.trim() || 'PETRONAS CHEMICALS FERTILISER SABAH SDN BHD',
            project: document.getElementById('project_name')?.value.trim() || 'VALVE MAINTENANCE PROJECT 2025',
            location: document.getElementById('location')?.value.trim() || 'Sipitang',
            date_in: dateInValue,
            inlet_type: inletType,
            outlet_type: outletType
        };
    }
    const visualInspection = collectVisualInspectionData();
    const internalInspection = collectInternalInspectionData();
    const detailedPictures = collectDetailedPicturesData();
    const stampSelection = document.getElementById('stamp_selection').value;
    const additionalComment = document.getElementById('additional_comment').value;
    const requestData = {
        identifier: identifier,
        override_mode: overrideMode,
        stamp_selection: stampSelection,
        date_value: finalDateValue,
        selected_services: selectedServices,
        comment: additionalComment,
        client_info: clientInfo,
        visual_inspection: visualInspection,
        internal_inspection: internalInspection,
        detailed_pictures: detailedPictures
    };
    showStatus('Generating service report...', 'info');
    fetch('/generate-service-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showStatus(data.message, 'success');
            loadPdfList();
        } else if (data.error) {
            showStatus(data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showStatus('An error occurred while generating the report.', 'error');
    });
}

function showStatus(message, type) {
    const statusDiv = document.getElementById('serviceReportStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 5000);
    }
}

function loadPdfList() {
    fetch('/list-pdfs')
        .then(response => response.json())
        .then(data => {
            const pdfList = document.getElementById('pdfList');
            pdfList.innerHTML = '';
            
            if (data.pdfs && data.pdfs.length > 0) {
                data.pdfs.forEach(pdf => {
                    if (pdf.filename && pdf.filename.includes('Service_report_')) {
                        const pdfItem = document.createElement('div');
                        pdfItem.className = 'pdf-item';
                        pdfItem.innerHTML = `
                            <span>${pdf.filename}</span>
                            <div class="pdf-actions">
                                <a href="/download-pdf/${pdf.filename}" class="btn btn-small btn-secondary">Download</a>
                                <a href="/view-pdf/${pdf.filename}" target="_blank" class="btn btn-small">View</a>
                                <button class="btn btn-small btn-danger" onclick="deletePdf('${pdf.filename}')">Delete</button>
                            </div>
                        `;
                        pdfList.appendChild(pdfItem);
                    }
                });
            } else {
                pdfList.innerHTML = '<p>No service reports generated yet.</p>';
            }
        })
        .catch(error => {
            console.error('Error loading PDF list:', error);
        });
}

function deletePdf(filename) {
    if (confirm('Are you sure you want to delete this PDF?')) {
        fetch(`/delete-pdf/${filename}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                loadPdfList();
            }
        })
        .catch(error => {
            console.error('Error deleting PDF:', error);
        });
    }
}
