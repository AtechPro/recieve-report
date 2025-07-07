from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from petronas_pdf_generator import generate_pdf
import subprocess
import json

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/temp_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

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
    no = data.get('no')
    user_data = data.get('user_data', None)
    image_files = data.get('image_files', None)
    received_valve_images = data.get('received_valve_images', None)
    
    if not no:
        return jsonify({'error': 'Missing required field: no'}), 400

    try:
        generate_pdf(no, user_data, image_files, received_valve_images)
        return jsonify({'message': f'PDF generated for No = {no}.'}), 200
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
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': 'Excel uploaded, but extraction failed.',
            'details': e.stderr
        }), 500

    return jsonify({
        'message': 'Excel file uploaded and extracted successfully',
        'filename': filename,
        'filepath': filepath,
        'extract_output': extract_output
    }), 200

@app.route('/available-no', methods=['GET'])
def available_no():
    try:
        with open('extracted_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        numbers = [record.get('No') for record in data.get('data', []) if record.get('No')]
        return jsonify({'numbers': numbers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 