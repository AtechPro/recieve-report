document.addEventListener('DOMContentLoaded', function() {
    loadAvailableNumbers();
    setCurrentStampDate();
    initializeVisualInspection();
    initializeInternalInspection();
});

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

function initializeVisualInspection() {
    const container = document.getElementById('visualInspectionContainer');
    const descriptions = [
        'GENERAL APPEARANCE',
        'NAMEPLATE',
        'OVERALL FLANGE/CONNECTION CONDITION',
        'STEM',
        'VALVE BODY',
        'HANDWHEEL',
        'VALVE BONNET',
        'YOKE',
        'BOLD NUT',
        'GEARBOX/ACTUATOR'
    ];
    
    descriptions.forEach((desc, index) => {
        addInspectionItem(container, 'visual', desc, index);
    });
}

function initializeInternalInspection() {
    const container = document.getElementById('internalInspectionContainer');
    const descriptions = [
        'BODY',
        'BONNET',
        'YOKE',
        'DISC',
        'SEAT',
        'BONNET GASKET',
        'STEM',
        'WHEEL NUT',
        'PACKING',
        'GLAND BUSHING',
        'BACK SEAT',
        'GLAND NUT'
    ];
    
    descriptions.forEach((desc, index) => {
        addInspectionItem(container, 'internal', desc, index);
    });
}

function addInspectionItem(container, type, desc, index) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'inspection-item';
    itemDiv.innerHTML = `
        <h4>${desc}</h4>
        <div class="inspection-grid">
            <div class="form-group">
                <label for="${type}_${index}_condition">Condition:</label>
                <input type="text" id="${type}_${index}_condition" placeholder="Enter condition" class="form-control">
            </div>
            <div class="form-group">
                <label for="${type}_${index}_actions">Actions:</label>
                <input type="text" id="${type}_${index}_actions" placeholder="Enter actions" class="form-control">
            </div>
            <div class="form-group">
                <label for="${type}_${index}_remarks">Remarks:</label>
                <input type="text" id="${type}_${index}_remarks" placeholder="Enter remarks" class="form-control">
            </div>
        </div>
    `;
    container.appendChild(itemDiv);
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

function generateReport() {
    const overrideMode = document.getElementById('override_mode').checked;
    let identifier = '';
    if (overrideMode) {
        identifier = document.getElementById('manual_wo')?.value.trim();
    } else {
        identifier = document.getElementById('valve_identifier').value;
    }
    if (!identifier) {
        showAlert('error', 'Please enter a ' + (overrideMode ? 'WO number in manual input' : 'valve No or WO number'));
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('alertContainer').innerHTML = '';
    document.getElementById('pdfActions').style.display = 'none';

    // Collect form data
    let inletType = document.getElementById('inlet_type').value;
    if (inletType === "Other") inletType = document.getElementById('inlet_type_other').value.trim();
    let outletType = document.getElementById('outlet_type').value;
    if (outletType === "Other") outletType = document.getElementById('outlet_type_other').value.trim();
    let clientInfo = {};
    if (overrideMode) {
        clientInfo = {
            client: document.getElementById('client_name').value,
            project: document.getElementById('project_name').value,
            location: document.getElementById('location').value,
            date_in: formatDateDMY(document.getElementById('date_in').value),
            inlet_type: inletType,
            outlet_type: outletType,
            ...collectManualOverrideData()
        };
    } else {
        clientInfo = {
            client: document.getElementById('client_name').value,
            project: document.getElementById('project_name').value,
            location: document.getElementById('location').value,
            date_in: formatDateDMY(document.getElementById('date_in').value),
            inlet_type: inletType,
            outlet_type: outletType
        };
    }

    const data = {
        identifier: identifier,
        override_mode: overrideMode,
        stamp_selection: document.getElementById('stamp_selection').value,
        date_value: document.getElementById('stamp_date').value,
        selected_services: getSelectedServices(),
        visual_inspection: getVisualInspectionData(),
        internal_inspection: getInternalInspectionData(),
        pretest: getPretestData(),
        posttest: getPosttestData(),
        comment: document.getElementById('comment').value,
        client_info: clientInfo
    };

    // Send request
    fetch('/generate-hydrotest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message) {
            showAlert('success', result.message);
            document.getElementById('viewPdf').href = result.view_url;
            document.getElementById('downloadPdf').href = result.download_url;
            document.getElementById('pdfActions').style.display = 'block';
        } else {
            showAlert('error', result.error || 'Failed to generate report');
        }
    })
    .catch(error => {
        showAlert('error', 'Network error: ' + error.message);
    })
    .finally(() => {
        document.getElementById('loading').style.display = 'none';
    });
}

function formatDateDMY(dateStr) {
    if (!dateStr) return '';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
}

function getSelectedServices() {
    const services = [];
    if (document.getElementById('insitu_testing').checked) services.push('insitu_testing');
    if (document.getElementById('service_repair').checked) services.push('service_repair');
    if (document.getElementById('testing_only').checked) services.push('testing_only');
    if (document.getElementById('replace_new_valve').checked) services.push('replace_new_valve');
    return services;
}

function getVisualInspectionData() {
    const data = [];
    const descriptions = [
        'GENERAL APPEARANCE',
        'NAMEPLATE',
        'OVERALL FLANGE/CONNECTION CONDITION',
        'STEM',
        'VALVE BODY',
        'HANDWHEEL',
        'VALVE BONNET',
        'YOKE',
        'BOLD NUT',
        'GEARBOX/ACTUATOR'
    ];
    
    descriptions.forEach((desc, index) => {
        data.push({
            desc: desc,
            condition: document.getElementById(`visual_${index}_condition`).value,
            actions: document.getElementById(`visual_${index}_actions`).value,
            remarks: document.getElementById(`visual_${index}_remarks`).value
        });
    });
    
    return data;
}

function getInternalInspectionData() {
    const data = [];
    const descriptions = [
        'BODY',
        'BONNET',
        'YOKE',
        'DISC',
        'SEAT',
        'BONNET GASKET',
        'STEM',
        'WHEEL NUT',
        'PACKING',
        'GLAND BUSHING',
        'BACK SEAT',
        'GLAND NUT'
    ];
    
    descriptions.forEach((desc, index) => {
        data.push({
            desc: desc,
            condition: document.getElementById(`internal_${index}_condition`).value,
            actions: document.getElementById(`internal_${index}_actions`).value,
            remarks: document.getElementById(`internal_${index}_remarks`).value
        });
    });
    
    return data;
}

function getPretestData() {
    return {
        type_test: document.getElementById('pretest_type').value,
        test_medium: document.getElementById('pretest_medium').value,
        shell: {
            pressure: document.getElementById('pretest_shell_pressure').value,
            duration: document.getElementById('pretest_shell_duration').value,
            result_remarks: document.getElementById('pretest_shell_result').value
        },
        backseat: {
            pressure: document.getElementById('pretest_backseat_pressure').value,
            duration: document.getElementById('pretest_backseat_duration').value,
            result_remarks: document.getElementById('pretest_backseat_result').value
        },
        seatA: {
            pressure: document.getElementById('pretest_seatA_pressure').value,
            duration: document.getElementById('pretest_seatA_duration').value,
            result_remarks: document.getElementById('pretest_seatA_result').value
        },
        seatB: {
            pressure: document.getElementById('pretest_seatB_pressure').value,
            duration: document.getElementById('pretest_seatB_duration').value,
            result_remarks: document.getElementById('pretest_seatB_result').value
        },
        test_accordance_to: document.getElementById('pretest_accordance').value
    };
}

function getPosttestData() {
    return {
        type_test: document.getElementById('posttest_type').value,
        test_medium: document.getElementById('posttest_medium').value,
        shell: {
            pressure: document.getElementById('posttest_shell_pressure').value,
            duration: document.getElementById('posttest_shell_duration').value,
            result_remarks: document.getElementById('posttest_shell_result').value
        },
        backseat: {
            pressure: document.getElementById('posttest_backseat_pressure').value,
            duration: document.getElementById('posttest_backseat_duration').value,
            result_remarks: document.getElementById('posttest_backseat_result').value
        },
        seatA: {
            pressure: document.getElementById('posttest_seatA_pressure').value,
            duration: document.getElementById('posttest_seatA_duration').value,
            result_remarks: document.getElementById('posttest_seatA_result').value
        },
        seatB: {
            pressure: document.getElementById('posttest_seatB_pressure').value,
            duration: document.getElementById('posttest_seatB_duration').value,
            result_remarks: document.getElementById('posttest_seatB_result').value
        },
        test_accordance_to: document.getElementById('posttest_accordance').value
    };
}

function showAlert(type, message) {
    const alertContainer = document.getElementById('alertContainer');
    const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
    
    alertContainer.innerHTML = `
        <div class="alert ${alertClass}">
            ${message}
        </div>
    `;
    
    // Auto-hide success alerts after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            alertContainer.innerHTML = '';
        }, 5000);
    }
}

function clearForm() {
    // Reset all form elements
    document.getElementById('valve_identifier').value = '';
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
    document.querySelectorAll('input[type="text"], input[type="date"], select, textarea').forEach(input => {
        if (input.id === 'stamp_date' || input.id === 'stamp_date_calendar') {
            setCurrentStampDate();
        } else {
            input.value = '';
        }
    });
    
    // Reset service options styling
    document.querySelectorAll('.service-option').forEach(option => {
        option.style.background = 'var(--light-gray)';
        option.style.borderColor = 'transparent';
        option.style.transform = 'scale(1)';
    });
    
    document.getElementById('alertContainer').innerHTML = '';
    document.getElementById('pdfActions').style.display = 'none';
}
