import os
from flask import Flask, request
from flask_cors import CORS  # Import CORS

from performOCR import ocr  # Importing the perform_ocr function from ocr_logic.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    # Perform OCR and return the result
    ocr_text = ocr(file_path)
    return ocr_text, 200

if __name__ == '__main__':
    app.run(debug=True)
