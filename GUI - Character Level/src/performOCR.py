import tesserocr
import numpy as np
from PIL import Image, ImageDraw
import os
import preprocess15

template_dir = "./templates"
template_1_path = os.path.join(template_dir, "template_1.bmp")
template_2_path = os.path.join(template_dir, "template_2.bmp")
template_1 = Image.open(template_1_path)
template_2 = Image.open(template_2_path)
template_array_1 = np.array(template_1)
template_array_2 = np.array(template_2)

def ocr(image_path):
    image = Image.open(image_path)
    image_array = np.array(image)
    gray_img_array = preprocess15.rgb_to_grayscale(image_array)

    # preprocessing
    sharp_img_array = preprocess15.sharpen_image(gray_img_array)
    # denoised_img_array = preprocess15.geometric_mean(sharp_img_array, 3)
    # eroded_img_array = preprocess15.dilate_image(denoised_img_array)
    # dilated_img_array = preprocess15.erode_image(eroded_img_array)
    # contrasted_img_array = preprocess15.contrast_stretching(eroded_img_array)

    # convert to pillow image object
    sharp_image = Image.fromarray(sharp_img_array)
    # denoised_image = Image.fromarray(denoised_img_array)
    # dilated_image = Image.fromarray(dilated_img_array)
    # eroded_image = Image.fromarray(eroded_img_array)
    grayScale_image = Image.fromarray(gray_img_array)
    # contrasted_image = Image.fromarray(contrasted_img_array)

    # input_image.show()
    sharp_image.save('sharp.bmp')
    # denoised_image.save('denoised.bmp')
    # dilated_image.save('dilated.bmp')
    # eroded_image.save('eroded.bmp')
    grayScale_image.save('gray.bmp')

    # contrasted_image.save('contrasted.bmp')

    # print(os.path.basename(image_path))

    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        api.SetImageFile('gray.bmp')
        gray_ocr = api.GetUTF8Text()
        # print(gray_ocr)

    with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
        api.SetImageFile('sharp.bmp')
        sharp_ocr = api.GetUTF8Text()
        print("sharp")
        print(sharp_ocr)


    # with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
    #     api.SetImageFile('denoised.bmp')
    #     denoised_ocr = api.GetUTF8Text()
    #     print("denoised")
    #     print(denoised_ocr)

    # with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
    #     api.SetImageFile('eroded.bmp')
    #     eroded_ocr = api.GetUTF8Text()
    #     print("eroded")
    #     print(eroded_ocr)
    
    # with tesserocr.PyTessBaseAPI(psm=6, lang='alp_num', oem=3) as api:
    #     api.SetImageFile('dilated.bmp')
    #     dilated_ocr = api.GetUTF8Text()
    #     print("dilated result")
    #     print(dilated_ocr)

    results = [
        [gray_img_array, gray_ocr],
        [sharp_img_array, sharp_ocr], 
        # [denoised_img_array, denoised_ocr],
        # [eroded_img_array, eroded_ocr],
        # [dilated_img_array, dilated_ocr],
        [image_array]
    ]

    return results
