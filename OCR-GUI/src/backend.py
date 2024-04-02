import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64

# Creating a Flask application  and enabling CORS to allow cross-origin requests.
# Define the folder where uploaded files will be stored.
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define a function encode_image which takes a NumPy array representation of an image, 
# converts it to a PIL image, saves it as a PNG format in a buffer, encodes the buffer content as base64, 
# and returns the encoded image as a string.
    
def encode_image(image_array):
    image = Image.fromarray(image_array)
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
    return encoded_image

# Define a route /upload that accepts POST requests for uploading files. When a file is uploaded, it saves the file to the specified 
# upload folder. It then calls an OCR function ocr from the performOCR (this is diff from the standard perform ocr file, 
# in the sense that it only returns ocr for one image etc) module passing the file path. It expects ocr to return the recognized text 
# and processed images. Processed images are encoded using the encode_image function. The recognized text and encoded images are returned as JSON response.

@app.route('/upload', methods=['POST'])
def upload_file():
    from performOCR import ocr
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    ocr_text, processed_images = ocr(file_path)
    encoded_images = [encode_image(img) for img in processed_images]
    print(len(processed_images))
    return jsonify({'ocr_text': ocr_text, 'processed_images': encoded_images}), 200

if __name__ == '__main__':
    app.run(debug=True)
