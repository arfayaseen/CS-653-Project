import tesserocr
import numpy as np
from PIL import Image, ImageDraw
import os
import preprocess15
from evaluate import load

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            return file.read().splitlines()
        
cer = load("cer")

def write_best_ocr_result(image_path, sharp_ocr_lines, denoised_ocr_lines, dilated_ocr_lines, eroded_ocr_lines, accuracies):
    accuracies_dict = {
        "sharp": accuracies[0],
        "denoised": accuracies[1],
        "dilated": accuracies[2],
        "eroded": accuracies[3]
    }

    best_preprocessing = max(accuracies_dict, key=accuracies_dict.get)

    if best_preprocessing == "sharp":
        ocr_lines = sharp_ocr_lines
    elif best_preprocessing == "denoised":
        ocr_lines = denoised_ocr_lines
    elif best_preprocessing == "dilated":
        ocr_lines = dilated_ocr_lines
    elif best_preprocessing == "eroded":
        ocr_lines = eroded_ocr_lines

    text_files_dir = r"C:\Users\Ali Raza\Desktop\plzmanplz"
    if not os.path.exists(text_files_dir):
        os.makedirs(text_files_dir)

    base_filename, _ = os.path.splitext(os.path.basename(image_path))
    text_filename = os.path.join(text_files_dir, base_filename + '.txt')
    
    with open(text_filename, 'w') as text_file:
        for line in ocr_lines:
            text_file.write(line + '\n')

def ocr(image_path, template_array_1, template_array_2):
    image = Image.open(image_path)
    image_array = np.array(image)
    gray_img_array = preprocess15.rgb_to_grayscale(image_array)

    top_left_1, bottom_right_1 = preprocess15.match_template(gray_img_array, template_array_1)
    if top_left_1 and bottom_right_1:
        roi_1 = gray_img_array[top_left_1[1]:bottom_right_1[1], top_left_1[0]:bottom_right_1[0]]
    else:
        roi_1 = gray_img_array 

    deskewed_array = preprocess15.deskew(roi_1)

    top_left_2, bottom_right_2 = preprocess15.match_template(deskewed_array, template_array_2)
    if top_left_2 and bottom_right_2:
        roi_2 = deskewed_array[top_left_2[1]:bottom_right_2[1], top_left_2[0]:bottom_right_2[0]]
    else:
        roi_2 = deskewed_array 

    sharp_img_array = preprocess15.sharpen_image(roi_2)
    denoised_img_array = preprocess15.geometric_mean(sharp_img_array, 3)
    eroded_img_array = preprocess15.erode_image(denoised_img_array)
    dilated_img_array = preprocess15.dilate_image(eroded_img_array)

    sharp_image = Image.fromarray(sharp_img_array)
    denoised_image = Image.fromarray(denoised_img_array)
    dilated_image = Image.fromarray(dilated_img_array)
    eroded_image = Image.fromarray(eroded_img_array)

    sharp_image.save('sharp.bmp')
    denoised_image.save('denoised.bmp')
    dilated_image.save('dilated.bmp')
    eroded_image.save('eroded.bmp')

    sharp_accuracy = 0
    denoised_accuracy = 0
    dilated_accuracy = 0
    eroded_accuracy = 0

    ground_truth_path = image_path.replace('OK', 'all').replace('.bmp', '.txt')
    ground_truth_text = read_file(ground_truth_path)
    
    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        api.SetImageFile('sharp.bmp')
        sharp_ocr = api.GetUTF8Text()
        sharp_ocr_lines = sharp_ocr.splitlines()
        if len(sharp_ocr_lines) == 3:
            cer_score = cer.compute(predictions=sharp_ocr_lines, references=ground_truth_text)
            sharp_accuracy = (1 - cer_score) * 100
    
    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        api.SetImageFile('denoised.bmp')
        denoised_ocr = api.GetUTF8Text()
        denoised_ocr_lines = denoised_ocr.splitlines()
        if len(denoised_ocr_lines) == 3:
            cer_score = cer.compute(predictions=denoised_ocr_lines, references=ground_truth_text)
            denoised_accuracy = (1 - cer_score) * 100

    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        api.SetImageFile('dilated.bmp')
        dilated_ocr = api.GetUTF8Text()
        dilated_ocr_lines = dilated_ocr.splitlines()
        if len(dilated_ocr_lines) == 3:
            cer_score = cer.compute(predictions=dilated_ocr_lines, references=ground_truth_text)
            dilated_accuracy = (1 - cer_score) * 100

    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        api.SetImageFile('eroded.bmp')
        eroded_ocr = api.GetUTF8Text()
        eroded_ocr_lines = eroded_ocr.splitlines()
        if len(eroded_ocr_lines) == 3:
            cer_score = cer.compute(predictions=eroded_ocr_lines, references=ground_truth_text)
            eroded_accuracy = (1 - cer_score) * 100

    accuracies = [sharp_accuracy, denoised_accuracy, dilated_accuracy, eroded_accuracy]
    write_best_ocr_result(image_path, sharp_ocr_lines, denoised_ocr_lines, dilated_ocr_lines, eroded_ocr_lines, accuracies)

# load the template for template matching
template_dir = r"C:\Users\Ali Raza\Desktop\project\Subset\templates"
template_1_path = os.path.join(template_dir, "template_1.bmp")
template_2_path = os.path.join(template_dir, "template_2.bmp")
template_1 = Image.open(template_1_path)
template_2 = Image.open(template_2_path)
template_array_1 = np.array(template_1)
template_array_2 = np.array(template_2)
    
testfiles_dir = r"C:\Users\Ali Raza\Desktop\Dataset\OK"
for filename in os.listdir(testfiles_dir):
    if filename.endswith('.bmp'):
        image_path = os.path.join(testfiles_dir, filename)
        ocr(image_path, template_array_1, template_array_2)
