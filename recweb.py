from flask import Flask, request, jsonify
from petronas_pdf_generator import generate_pdf

app = Flask(__name__)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    image = request.files['image']
    # Mock: Just return the filename, don't actually save
    return jsonify({'message': 'Image uploaded (mock)', 'filename': image.filename}), 200

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    no = data.get('no')
    user_data = data.get('user_data', None)
    image_files = data.get('image_files', None)  # Accept image filenames (mock)
    if not no:
        return jsonify({'error': 'Missing required field: no'}), 400

    # For now, the PDF generator will use the default images provided in the directory
    try:
        generate_pdf(no, user_data)
        return jsonify({'message': f'PDF generated for No = {no}.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 