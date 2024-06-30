import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64
from performOCR import ocr
from evaluate import load

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
GROUND_TRUTH_FOLDER = 'ground-truths'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

cer = load("cer")

def encode_image(image_array):
    image = Image.fromarray(image_array)
    image_buffer = BytesIO()
    image.save(image_buffer, format="PNG")
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
    return encoded_image

def read_ground_truth(filename):
    ground_truth_path = os.path.join(GROUND_TRUTH_FOLDER, f"{filename}.txt")
    if os.path.isfile(ground_truth_path):
        with open(ground_truth_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return None

def calc_accuracy(ground_truth_text, output_text):   
    ground_truth_text = [ground_truth_text] if isinstance(ground_truth_text, str) else ground_truth_text
    output_text = [output_text] if isinstance(output_text, str) else output_text
    max_length = max(len(output_text), len(ground_truth_text))
    output_text.extend([""] * (max_length - len(output_text)))
    ground_truth_text.extend([""] * (max_length - len(ground_truth_text)))
    if '' not in ground_truth_text:
        cer_score = cer.compute(predictions=output_text, references=ground_truth_text)
        accuracy = (1 - cer_score) * 100
        return round(accuracy, 2)
    else:
        return None


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # Save the uploaded file
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Call the OCR function
    ocr_result = ocr(file_path)
    
    # Check if ocr_result is not None
    if ocr_result is None:
        return 'OCR failed', 500
    
    # Extract OCR results
    gray_scale_image = ocr_result[0][0]
    sharpened_ocr_result = ocr_result[1][1]
    sharpened_image = ocr_result[1][0]
    denoised_ocr_result = ocr_result[2][1]
    denoised_image = ocr_result[2][0]
    dilated_ocr_result = ocr_result[4][1]
    dilated_image = ocr_result[4][0]
    eroded_ocr_result = ocr_result[3][1]
    eroded_image = ocr_result[3][0]
    original_image = ocr_result[5][0]

    # Encode processed images
    encoded_gray_scale_image = encode_image(gray_scale_image)
    encoded_sharpened_image = encode_image(sharpened_image)
    encoded_denoised_image = encode_image(denoised_image)
    encoded_dilated_image = encode_image(dilated_image)
    encoded_eroded_image = encode_image(eroded_image)
    encoded_original_image = encode_image(original_image)
    # Get ground truth text
    ground_truth_text = read_ground_truth(os.path.splitext(filename)[0])
    
    # Calculate accuracy
    sharpened_accuracy = calc_accuracy(ground_truth_text, sharpened_ocr_result)
    denoised_accuracy = calc_accuracy(ground_truth_text, denoised_ocr_result)
    dilated_accuracy = calc_accuracy(ground_truth_text, dilated_ocr_result)
    eroded_accuracy = calc_accuracy(ground_truth_text, eroded_ocr_result)

    # Construct response JSON
    response = {
        'original_image':encoded_original_image,
        'gray_scale_image': encoded_gray_scale_image,
        'sharpened_ocr_result': sharpened_ocr_result,
        'sharpened_image': encoded_sharpened_image,
        'sharpened_accuracy': sharpened_accuracy,
        'denoised_ocr_result': denoised_ocr_result,
        'denoised_image': encoded_denoised_image,
        'denoised_accuracy': denoised_accuracy,
        'dilated_ocr_result': dilated_ocr_result,
        'dilated_image': encoded_dilated_image,
        'dilated_accuracy': dilated_accuracy,
        'eroded_ocr_result': eroded_ocr_result,
        'eroded_image': encoded_eroded_image,
        'eroded_accuracy': eroded_accuracy
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
