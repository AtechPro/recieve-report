from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename
from recievedreport import generate_pdf
import subprocess
import json
import glob

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/temp_images'
PDF_FOLDER = 'generated_pdfs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_temp_images(image_files, received_valve_images):
    """Clean up temporary images after PDF generation"""
    try:
        # Clean up detailed images
        if image_files:
            for image_type, filepath in image_files.items():
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"Cleaned up: {filepath}")
        
        # Clean up received valve images
        if received_valve_images:
            for filepath in received_valve_images:
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"Cleaned up: {filepath}")
                    
    except Exception as e:
        print(f"Error during cleanup: {e}")

def cleanup_all_temp_images():
    """Clean up all temporary images in the temp_images folder"""
    try:
        temp_files = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
        for file_path in temp_files:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Cleaned up: {file_path}")
        return True
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return False

@app.route('/')
def index():
    # Load stamp mapping from JSON
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
        # Prepare options as a list of dicts: {value: key, label: prepared_name}
        stamp_options = [
            {'value': key, 'label': value['prepared_name']} for key, value in stamp_mapping.items()
        ]
    except Exception as e:
        print(f"Error loading stamp mapping: {e}")
        stamp_options = [{'value': 'SAO', 'label': 'Sao Lip Zhou'}]
    return render_template('recieve_valve.html', stamp_options=stamp_options)

@app.route('/finding-report')
def finding_report():
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
        stamp_options = [
            {'value': key, 'label': value['prepared_name']} for key, value in stamp_mapping.items()
        ]
    except Exception as e:
        print(f"Error loading stamp mapping: {e}")
        stamp_options = [{'value': 'SAO', 'label': 'Sao Lip Zhou'}]
    return render_template('finding_report.html', stamp_options=stamp_options)

@app.route('/service-report')
def service_report():
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
        stamp_options = [
            {'value': key, 'label': value['prepared_name']} for key, value in stamp_mapping.items()
        ]
    except Exception as e:
        print(f"Error loading stamp mapping: {e}")
        stamp_options = [{'value': 'SAO', 'label': 'Sao Lip Zhou'}]
    return render_template('service_report.html', stamp_options=stamp_options)

@app.route('/hydrotest')
def hydrotest():
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
        stamp_options = [
            {'value': key, 'label': value['prepared_name']} for key, value in stamp_mapping.items()
        ]
    except Exception as e:
        print(f"Error loading stamp mapping: {e}")
        stamp_options = [{'value': 'SAO', 'label': 'Sao Lip Zhou'}]
    return render_template('hydrotest.html', stamp_options=stamp_options)

@app.route('/excel-converter')
def excel_converter():
    return render_template('excel_converter.html')

@app.route('/get-converted-data')
def get_converted_data():
    """Get the converted JSON data"""
    try:
        with open('extracted_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'No converted data found. Please upload an Excel file first.'}), 404
    except Exception as e:
        return jsonify({'error': f'Error reading converted data: {str(e)}'}), 500

@app.route('/get-extracted-data')
def get_extracted_data():
    """Get the extracted data for table viewer"""
    try:
        with open('extracted_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'extracted_data.json file not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error reading extracted data: {str(e)}'}), 500

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    image_type = request.form.get('image_type', 'unknown')  # inlet_connection, outlet_connection, etc.
    
    if image.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        # Create unique filename with image type
        name, ext = os.path.splitext(filename)
        unique_filename = f"{image_type}_{name}{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        image.save(filepath)
        return jsonify({
            'message': 'Image uploaded successfully',
            'filename': unique_filename,
            'filepath': filepath,
            'image_type': image_type
        }), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    identifier = data.get('identifier')
    user_data = data.get('user_data', None)
    image_files = data.get('image_files', None)
    received_valve_images = data.get('received_valve_images', None)
    stamp_selection = data.get('stamp_selection', 'SAO')  # Default to SAO
    date_value = data.get('date_value', '7/7/2027')  # Default date
    selected_services = data.get('selected_services', [])  # Service selections from user (array)
    comment = data.get('comment', '')  # Get the comment from the request
    override_mode = data.get('override_mode', False)  # Get override_mode from request
    
    if not identifier:
        return jsonify({'error': 'Missing required field: identifier (No or WO)'}), 400

    try:
        pdf_filename = generate_pdf(identifier, user_data, image_files, received_valve_images, stamp_selection, date_value, selected_services, override_mode=override_mode)
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        
        # Clean up temporary images after PDF generation
        cleanup_temp_images(image_files, received_valve_images)
        
        return jsonify({
            'message': f'PDF generated successfully for identifier = {identifier}.',
            'pdf_filename': pdf_filename,
            'pdf_path': pdf_path,
            'download_url': f'/download-pdf/{pdf_filename}',
            'view_url': f'/view-pdf/{pdf_filename}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-finding-report', methods=['POST'])
def generate_finding_report():
    data = request.get_json()
    identifier = data.get('identifier')
    stamp_selection = data.get('stamp_selection', 'SAO')
    date_value = data.get('date_value', '')
    selected_services = data.get('selected_services', [])
    comment = data.get('comment', '')  # Get comment from request
    override_mode = data.get('override_mode', False)  # Accept override_mode from request
    # Debug: Log the received data
    print(f"DEBUG: Received date_value: '{date_value}'")
    print(f"DEBUG: date_value type: {type(date_value)}")
    print(f"DEBUG: date_value length: {len(date_value) if date_value else 'None'}")
    # Extract additional data for finding report
    visual_inspection = data.get('visual_inspection', [])
    internal_inspection = data.get('internal_inspection', [])
    detailed_pictures = data.get('detailed_pictures', [])
    pretest = data.get('pretest', {})
    if not identifier:
        return jsonify({'error': 'Missing required field: identifier (No or WO)'}), 400
    try:
        # Import the finding report generation function
        from findingreport import generate_pdf as generate_finding_pdf
        # Create user_data with the collected form data
        user_data = {
            'client_info': data.get('client_info', {}),
            'visual_inspection': visual_inspection,
            'internal_inspection': internal_inspection,
            'detailed_pictures': detailed_pictures,
            'pretest': pretest,
            'comment': comment,  # Include comment in user_data
            'stamp_info': {
                'date_value': date_value
            }
        }
        pdf_filename = generate_finding_pdf(
            identifier=identifier,
            user_data=user_data,
            stamp_selection=stamp_selection,
            date_value=date_value,
            selected_services=selected_services,
            override_mode=override_mode  # Pass override_mode to PDF generator
        )
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        return jsonify({
            'message': f'Finding report generated successfully for identifier = {identifier}.',
            'pdf_filename': pdf_filename,
            'pdf_path': pdf_path,
            'download_url': f'/download-pdf/{pdf_filename}',
            'view_url': f'/view-pdf/{pdf_filename}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-hydrotest', methods=['POST'])
def generate_hydrotest():
    data = request.get_json()
    identifier = data.get('identifier')
    stamp_selection = data.get('stamp_selection', 'SAO')
    date_value = data.get('date_value', '')
    selected_services = data.get('selected_services', [])
    comment = data.get('comment', '')  # Get comment from request
    override_mode = data.get('override_mode', False)  # Accept override_mode from request
    # Extract additional data for hydrotest report
    visual_inspection = data.get('visual_inspection', [])
    internal_inspection = data.get('internal_inspection', [])
    pretest = data.get('pretest', {})
    posttest = data.get('posttest', {})
    if not identifier:
        return jsonify({'error': 'Missing required field: identifier (No or WO)'}), 400
    try:
        # Import the hydrotest generation function
        from hydrotest import generate_pdf as generate_hydrotest_pdf
        # Create user_data with the collected form data
        user_data = {
            'client_info': data.get('client_info', {}),
            'visual_inspection': visual_inspection,
            'internal_inspection': internal_inspection,
            'pretest': pretest,
            'posttest': posttest,
            'comment': comment,  # Include comment in user_data
            'stamp_info': {
                'date_value': date_value
            }
        }
        pdf_filename = generate_hydrotest_pdf(
            identifier=identifier,
            user_data=user_data,
            stamp_selection=stamp_selection,
            date_value=date_value,
            selected_services=selected_services,
            override_mode=override_mode  # Pass override_mode to PDF generator
        )
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        return jsonify({
            'message': f'Hydrotest report generated successfully for identifier = {identifier}.',
            'pdf_filename': pdf_filename,
            'pdf_path': pdf_path,
            'download_url': f'/download-pdf/{pdf_filename}',
            'view_url': f'/view-pdf/{pdf_filename}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-service-report', methods=['POST'])
def generate_service_report():
    data = request.get_json()
    identifier = data.get('identifier')
    stamp_selection = data.get('stamp_selection', 'SAO')
    date_value = data.get('date_value', '')
    selected_services = data.get('selected_services', [])
    comment = data.get('comment', '')  # Get comment from request
    override_mode = data.get('override_mode', False)  # Accept override_mode from request
    # Extract additional data for service report
    visual_inspection = data.get('visual_inspection', [])
    internal_inspection = data.get('internal_inspection', [])
    detailed_pictures = data.get('detailed_pictures', [])
    
    if not identifier:
        return jsonify({'error': 'Missing required field: identifier (No or WO)'}), 400

    try:
        # Import the service report generation function
        from servicerep import generate_pdf as generate_service_pdf
        # Create user_data with the collected form data
        user_data = {
            'client_info': data.get('client_info', {}),
            'visual_inspection': visual_inspection,
            'internal_inspection': internal_inspection,
            'detailed_pictures': detailed_pictures,
            'comment': comment,  # Include comment in user_data
            'stamp_info': {
                'date_value': date_value
            }
        }
        pdf_filename = generate_service_pdf(
            identifier=identifier,
            user_data=user_data,
            stamp_selection=stamp_selection,
            date_value=date_value,
            selected_services=selected_services,
            comment=comment,
            override_mode=override_mode  # Pass override_mode to PDF generator
        )
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        return jsonify({
            'message': f'Service report generated successfully for identifier = {identifier}.',
            'pdf_filename': pdf_filename,
            'pdf_path': pdf_path,
            'download_url': f'/download-pdf/{pdf_filename}',
            'view_url': f'/view-pdf/{pdf_filename}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload-excel', methods=['POST'])
def upload_excel():
    if 'excel' not in request.files:
        return jsonify({'error': 'No Excel file provided'}), 400

    excel = request.files['excel']
    if excel.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Only allow .xlsx or .xls
    if not (excel.filename.endswith('.xlsx') or excel.filename.endswith('.xls')):
        return jsonify({'error': 'Invalid file type'}), 400

    # Save to a temp directory
    excel_folder = 'static/temp_excel'
    os.makedirs(excel_folder, exist_ok=True)
    filename = secure_filename(excel.filename)
    filepath = os.path.join(excel_folder, filename)
    excel.save(filepath)

    # Trigger the extraction script
    try:
        result = subprocess.run(
            ['python', 'extract_excel_to_json.py', filepath],
            capture_output=True, text=True, check=True
        )
        extract_output = result.stdout
        
        # Clean up the Excel file after successful extraction
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Cleaned up Excel file: {filepath}")
            
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': 'Excel uploaded, but extraction failed.',
            'details': e.stderr
        }), 500

    return jsonify({
        'message': 'Excel file uploaded and extracted successfully',
        'filename': filename,
        'extract_output': extract_output
    }), 200

@app.route('/available-no', methods=['GET'])
def available_no():
    try:
        with open('extracted_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        numbers = [record.get('No') for record in data.get('data', []) if record.get('No')]
        wo_numbers = [record.get('WO ') for record in data.get('data', []) if record.get('WO ')]
        return jsonify({'numbers': numbers, 'wo_numbers': wo_numbers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-pdf/<filename>')
def download_pdf(filename):
    """Download a specific PDF file"""
    try:
        return send_from_directory(PDF_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'File not found: {filename}'}), 404

@app.route('/view-pdf/<filename>')
def view_pdf(filename):
    """View a specific PDF file in browser"""
    try:
        return send_from_directory(PDF_FOLDER, filename)
    except Exception as e:
        return jsonify({'error': f'File not found: {filename}'}), 404

@app.route('/list-pdfs', methods=['GET'])
def list_pdfs():
    """List all available PDF files"""
    try:
        pdf_files = glob.glob(os.path.join(PDF_FOLDER, '*.pdf'))
        pdf_list = []
        for pdf_file in pdf_files:
            filename = os.path.basename(pdf_file)
            pdf_list.append({
                'filename': filename,
                'download_url': f'/download-pdf/{filename}',
                'view_url': f'/view-pdf/{filename}',
                'size': os.path.getsize(pdf_file)
            })
        return jsonify({'pdfs': pdf_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-pdf/<filename>', methods=['DELETE'])
def delete_pdf(filename):
    """Delete a specific PDF file"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or '/' in filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        pdf_path = os.path.join(PDF_FOLDER, filename)
        
        if not os.path.exists(pdf_path):
            return jsonify({'error': f'PDF file not found: {filename}'}), 404
        
        # Delete the file
        os.remove(pdf_path)
        print(f"Deleted PDF: {pdf_path}")
        
        return jsonify({
            'message': f'PDF "{filename}" deleted successfully',
            'filename': filename
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to delete PDF: {str(e)}'}), 500

@app.route('/cleanup-temp', methods=['POST'])
def cleanup_temp():
    """Clean up all temporary files (images and Excel)"""
    try:
        # Clean up temp images
        images_cleaned = cleanup_all_temp_images()
        
        # Clean up temp Excel files
        excel_folder = 'static/temp_excel'
        excel_files_cleaned = 0
        if os.path.exists(excel_folder):
            excel_files = glob.glob(os.path.join(excel_folder, '*'))
            for file_path in excel_files:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    excel_files_cleaned += 1
                    print(f"Cleaned up Excel: {file_path}")
        
        return jsonify({
            'message': f'Cleanup completed successfully',
            'images_cleaned': images_cleaned,
            'excel_files_cleaned': excel_files_cleaned
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/valvecert')
def valvecert():
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
        stamp_options = [
            {'value': key, 'label': value['prepared_name']} for key, value in stamp_mapping.items()
        ]
    except Exception as e:
        print(f"Error loading stamp mapping: {e}")
        stamp_options = [{'value': 'SAO', 'label': 'Sao Lip Zhou'}]
    return render_template('valvecert.html', stamp_options=stamp_options)

@app.route('/generate-valvecert', methods=['POST'])
def generate_valvecert():
    data = request.get_json()
    identifier = data.get('identifier')
    stamp_selection = data.get('stamp_selection', 'SAO')
    date_value = data.get('date_value', '')
    selected_services = data.get('selected_services', [])
    comment = data.get('comment', '')
    override_mode = data.get('override_mode', False)
    # Extract additional data for valve cert report
    visual_inspection = data.get('visual_inspection', [])
    internal_inspection = data.get('internal_inspection', [])
    pretest = data.get('pretest', {})
    posttest = data.get('posttest', {})
    if not identifier:
        return jsonify({'error': 'Missing required field: identifier (No or WO)'}), 400
    try:
        from valvecert import generate_pdf as generate_valvecert_pdf
        user_data = {
            'client_info': data.get('client_info', {}),
            'visual_inspection': visual_inspection,
            'internal_inspection': internal_inspection,
            'pretest': pretest,
            'posttest': posttest,
            'comment': comment,
            'stamp_info': {
                'date_value': date_value
            }
        }
        pdf_filename = generate_valvecert_pdf(
            identifier=identifier,
            user_data=user_data,
            stamp_selection=stamp_selection,
            date_value=date_value,
            selected_services=selected_services,
            override_mode=override_mode
        )
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        return jsonify({
            'message': f'Valve certificate generated successfully for identifier = {identifier}.',
            'pdf_filename': pdf_filename,
            'pdf_path': pdf_path,
            'download_url': f'/download-pdf/{pdf_filename}',
            'view_url': f'/view-pdf/{pdf_filename}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/edit-stamps')
def edit_stamps():
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
    except Exception as e:
        print(f"Error loading stamp mapping: {e}")
        stamp_mapping = {}
    return render_template('edit_stamps.html', stamps=stamp_mapping)

@app.route('/upload-stamp', methods=['POST'])
def upload_stamp():
    name = request.form.get('prepared_name')
    file = request.files.get('stamp_image')
    key = request.form.get('stamp_key') or name.upper().replace(' ', '_')
    if not name or not file:
        return 'Missing name or file', 400
    # Save file
    ext = os.path.splitext(file.filename)[1]
    filename = f"{key}{ext}"
    save_path = os.path.join('stamp', filename)
    file.save(save_path)
    # Update JSON
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
    except Exception:
        stamp_mapping = {}
    stamp_mapping[key] = {
        'stamp_path': f'stamp/{filename}',
        'prepared_name': name
    }
    with open('stamp_mapping.json', 'w') as f:
        json.dump(stamp_mapping, f, indent=2)
    return 'OK', 200

@app.route('/delete-stamp', methods=['POST'])
def delete_stamp():
    key = request.form.get('stamp_key')
    if not key:
        return 'Missing stamp_key', 400
    # Update JSON
    try:
        with open('stamp_mapping.json', 'r') as f:
            stamp_mapping = json.load(f)
    except Exception:
        return 'Could not load mapping', 500
    stamp = stamp_mapping.pop(key, None)
    if stamp:
        # Remove file
        try:
            os.remove(stamp['stamp_path'])
        except Exception as e:
            print(f"Warning: could not delete file {stamp['stamp_path']}: {e}")
        with open('stamp_mapping.json', 'w') as f:
            json.dump(stamp_mapping, f, indent=2)
        return 'OK', 200
    return 'Not found', 404

if __name__ == '__main__':
    app.run(debug=True, port=5300, host='0.0.0.0') 