import tesserocr
import numpy as np
from PIL import Image, ImageDraw
import os
import preprocess25
import LineSegmentation
import re

def ocr(image_path, template_array_1, template_array_2):
    image = Image.open(image_path)
    image_array = np.array(image)
    gray_img_array = preprocess25.rgb_to_grayscale(image_array)

    # template matching to find the region of interest (ROI) which needs to be deskewed
    top_left_1, bottom_right_1 = preprocess25.match_template(gray_img_array, template_array_1)
    if top_left_1 and bottom_right_1:
        roi_1 = gray_img_array[top_left_1[1]:bottom_right_1[1], top_left_1[0]:bottom_right_1[0]]
    else:
        # use the whole image if no match is found
        roi_1 = gray_img_array 

    deskewed_array = preprocess25.deskew(roi_1)

    # template matching to find the region of interest (ROI) which needs to be OCR-ed
    top_left_2, bottom_right_2 = preprocess25.match_template(deskewed_array, template_array_2)
    if top_left_2 and bottom_right_2:
        roi_2 = deskewed_array[top_left_2[1]:bottom_right_2[1], top_left_2[0]:bottom_right_2[0]]
    else:
        # use the whole image if no match is found
        roi_2 = deskewed_array 

    # preprocessing
    sharp_img_array = preprocess25.sharpen_image(roi_2)
    denoised_img_array = preprocess25.median_filter(sharp_img_array)
    # dilated_img_array = preprocess25.dilate_image(denoised_img_array)
    # eroded_img_array = preprocess25.erode_image(dilated_img_array)
    contrasted_img_array = preprocess25.contrast_stretching(denoised_img_array)
    
    LineSegmentation.segment_lines_of_text(contrasted_img_array)

    print(os.path.basename(image_path))

    input_image_paths = []
    for i in range(len(os.listdir('./cropped_images_for_ocr/'))):
        input_image_paths.append(os.path.join('./cropped_images_for_ocr/', f"input_image_{i+1}.bmp"))

    ocr_results = []
    nonempty_paths = []

    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        for input_image_path in input_image_paths:
            api.SetImageFile(input_image_path)
            ocr_result = api.GetUTF8Text().strip()  # remove any trailing whitespace or newlines
            if ocr_result != "":
                ocr_results.append(ocr_result)
                nonempty_paths.append(input_image_path)
            
        cleaned_strs = []
        for result in ocr_results:
            cleaned_string = re.sub(r'[^a-zA-Z0-9\s.=+:]', '', result)
            cleaned_strs.append(cleaned_string)

        ocr_dict = dict(zip(nonempty_paths, cleaned_strs))
        cleaned_results = LineSegmentation.unique_values(ocr_dict)
        print(cleaned_results.keys())

        for img_path in cleaned_results.keys():
            img = Image.open(img_path)

            it = api.GetIterator() # for iterating over recognized characters 
            draw = ImageDraw.Draw(img) # create a draw object
            while it.Next(tesserocr.RIL.SYMBOL):
                bbox = it.BoundingBox(tesserocr.RIL.SYMBOL)
                draw.rectangle(bbox, outline='black')

            # save the image with bounding boxes
            bboxed_images_dir = './bboxed_images_set-25/'
            if not os.path.exists(bboxed_images_dir):
                os.makedirs(bboxed_images_dir)
            bboxed_image_path = os.path.join(bboxed_images_dir, 'bboxed_' + os.path.basename(image_path) + "_" + os.path.basename(img_path))
            print(bboxed_image_path)
            img.save(bboxed_image_path)


    output_files_dir = './AccuracyMeasure/outputs-set-25/'
    if not os.path.exists(output_files_dir):
        os.makedirs(output_files_dir)

    base_filename, _ = os.path.splitext(os.path.basename(image_path))
    output_filename = os.path.join(output_files_dir, base_filename + '.txt')
        
    with open(output_filename, 'w') as output_file:
        for i, result in enumerate(cleaned_results.items()):
            input_images_dir = './cropped-images/'
            bf, _ = os.path.splitext(os.path.basename(result[0]))
            input_image_dir = os.path.join(input_images_dir, base_filename + '/')

            if not os.path.exists(input_image_dir):
                os.makedirs(input_image_dir)

            save_img_path = os.path.join(input_image_dir, bf + '.bmp')
            # print(result[0])
            cropped_image = Image.open(result[0])
            # print(save_img_path)
            cropped_image.save(save_img_path)
            if i < len(cleaned_results) - 1:
                output_file.write(result[1] + '\n')  # add newline character after each line except the last one
            else:
                output_file.write(result[1])         # do not add newline character after the last line

        
# load the template for template matching
template_dir = "./templates/"
template_1_path = os.path.join(template_dir, "template_1.bmp")
template_2_path = os.path.join(template_dir, "template_2.bmp")
template_1 = Image.open(template_1_path)
template_2 = Image.open(template_2_path)
template_array_1 = np.array(template_1)
template_array_2 = np.array(template_2)

testfiles_dir = "./AccuracyMeasure/inputs"

# perform ocr on each image in the directory
for filename in os.listdir(testfiles_dir):
    if filename.endswith('.bmp'):
        image_path = os.path.join(testfiles_dir, filename)
        ocr(image_path, template_array_1, template_array_2)


