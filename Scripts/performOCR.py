import tesserocr
import numpy as np
from PIL import Image, ImageDraw
import os
import preprocess15
from scipy.ndimage import generic_filter


def ocr(image_path, template_array_1, template_array_2, allowed_chars):
    image = Image.open(image_path)
    image_array = np.array(image)
    gray_img_array = preprocess15.rgb_to_grayscale(image_array)

    # template matching to find the region of interest (ROI) which needs to be deskewed
    top_left_1, bottom_right_1 = preprocess15.match_template(gray_img_array, template_array_1)
    if top_left_1 and bottom_right_1:
        roi_1 = gray_img_array[top_left_1[1]:bottom_right_1[1], top_left_1[0]:bottom_right_1[0]]
    else:
        # use the whole image if no match is found
        roi_1 = gray_img_array 

    deskewed_array = preprocess15.deskew(roi_1)

    # template matching to find the region of interest (ROI) which needs to be OCR-ed
    top_left_2, bottom_right_2 = preprocess15.match_template(deskewed_array, template_array_2)
    if top_left_2 and bottom_right_2:
        roi_2 = deskewed_array[top_left_2[1]:bottom_right_2[1], top_left_2[0]:bottom_right_2[0]]
    else:
        # use the whole image if no match is found
        roi_2 = deskewed_array 

    # preprocessing
    sharp_img_array = preprocess15.sharpen_image(roi_2)
    denoised_img_array = preprocess15.geometric_mean(sharp_img_array, 3)
    dilated_img_array = preprocess15.dilate_image(denoised_img_array)
    eroded_img_array = preprocess15.erode_image(dilated_img_array)

    # convert to pillow image object
    input_image = Image.fromarray(eroded_img_array)
    # input_image.show()
    input_image.save('input.bmp')
    print(os.path.basename(image_path))

    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        api.SetVariable("tessedit_char_whitelist", allowed_chars)
        api.SetImageFile('input.bmp')
        
        ocr_result = api.GetUTF8Text()
        print(ocr_result)

        # save result in .txt file
        text_files_dir = './AccuracyMeasure/outputs-set-30/'
        if not os.path.exists(text_files_dir):
            os.makedirs(text_files_dir)

        base_filename, _ = os.path.splitext(os.path.basename(image_path))
        text_filename = os.path.join(text_files_dir, base_filename + '.txt')
        with open(text_filename, 'w') as text_file:
            text_file.write(ocr_result)

        # visualize the results
        image_for_analysis = input_image
        it = api.GetIterator() # for iterating over recognized characters 
        draw = ImageDraw.Draw(image_for_analysis) # create a draw object
        while it.Next(tesserocr.RIL.SYMBOL):
            bbox = it.BoundingBox(tesserocr.RIL.SYMBOL)
            draw.rectangle(bbox, outline='black')

        # save the image with bounding boxes
        bboxed_images_dir = './bboxed_images_set-15/'
        if not os.path.exists(bboxed_images_dir):
            os.makedirs(bboxed_images_dir)
        bboxed_image_path = os.path.join(bboxed_images_dir, 'bboxed_' + os.path.basename(image_path))
        image_for_analysis.save(bboxed_image_path)

        
# load the template for template matching
template_dir = "./templates/"
template_1_path = os.path.join(template_dir, "template_1.bmp")
template_2_path = os.path.join(template_dir, "template_2.bmp")
template_1 = Image.open(template_1_path)
template_2 = Image.open(template_2_path)
template_array_1 = np.array(template_1)
template_array_2 = np.array(template_2)
allowed_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:.=+ '

testfiles_dir = "./AccuracyMeasure/inputs/" # "../../10gBoxes_15-03-2023/OK"
# "./AccuracyMeasure/inputs/" 

# perform ocr on each image in the directory
for filename in os.listdir(testfiles_dir):
    if filename.endswith('.bmp'):
        image_path = os.path.join(testfiles_dir, filename)
        ocr(image_path, template_array_1, template_array_2, allowed_chars)



