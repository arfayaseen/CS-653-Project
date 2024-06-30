import numpy as np
from PIL import Image, ImageFilter
import cv2
from skimage.transform import rotate
from deskew import determine_skew
from scipy.signal import wiener


def rgb_to_grayscale(image_array):
    red_channel_array = image_array[:, :, 0]
    return red_channel_array

def deskew(image_array):
    angle = determine_skew(image_array)
    # print(angle)
    rotated_array = rotate(image_array, angle, resize=True) * 255
    return rotated_array.astype(np.uint8)

def sharpen_image(image_array):
    # convert into image
    image = Image.fromarray(image_array)
    filter = ImageFilter.UnsharpMask(radius=5, percent=130, threshold=5)
    sharp_image = image.filter(filter)
    sharp_image_array = np.array(sharp_image)
    return sharp_image_array

def blur_image(image_array):
    image = Image.fromarray(image_array)
    blur_image = image.filter(ImageFilter.BoxBlur(radius=0.05))
    blur_image_array = np.array(blur_image)
    return blur_image_array

def median_filter(image_array):
    median_filtered_img = cv2.medianBlur(image_array, 3)
    return np.array(median_filtered_img)

def dilate_image(image_array):
    kernel = np.ones((3,3), np.uint8)
    dilated_image = cv2.dilate(image_array, kernel, iterations=1)
    return np.array(dilated_image)

def erode_image(image_array):
    kernel = np.ones((3,3), np.uint8)
    eroded_image = cv2.erode(image_array, kernel, iterations=1)
    return np.array(eroded_image)

# def dilate_image(image_array):
#     #     # Convert the image to grayscale
#     # Threshold the image to separate characters from the background
#     _, thresholded_image = cv2.threshold(image_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     # Apply dilation
#     kernel = np.ones((3,3), np.uint8)
#     dilated_image = cv2.dilate(image_array, kernel, iterations=1)
#     return dilated_image

# def erode_image(image_array):
#     # Convert the image to grayscale
#     # Threshold the image to separate characters from the background
#     _, thresholded_image = cv2.threshold(image_array, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     # Apply erosion
#     kernel = np.ones((3,3), np.uint8)
#     eroded_image = cv2.erode(thresholded_image, kernel, iterations=1)
#     return eroded_image

def canny(image_array):
    edges_image = cv2.Canny(image_array, 50, 200)
    return np.array(edges_image)

def match_template(image_array, template_array):
    result = cv2.matchTemplate(image_array, template_array, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.5:
        h, w = template_array.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return top_left, bottom_right
    else:
        return None, None
    
def binary_threshold(image_array, threshold=127, max_value=255):
    _, thresholded_image = cv2.threshold(image_array, threshold, max_value, cv2.THRESH_BINARY)
    return np.array(thresholded_image)

def motion_deblur(image_array):
    deblurred = wiener(image_array, (3, 3), 0.5)
    return deblurred

def geometric_mean(image, kernel_size):
    pad_size = kernel_size // 2
    padded_image = np.pad(image, pad_size, mode='constant')
    
    filtered_image = np.zeros_like(image, dtype=image.dtype)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            kernel_window = padded_image[i:i+kernel_size, j:j+kernel_size]
            
            # small value added to prevent underflow
            product = np.prod(kernel_window + 1e-10)
            geom_mean = product**(1/(kernel_size**2))
            filtered_image[i, j] = geom_mean
    
    return filtered_image

def contrast_stretching(image_array):   
    min_val = np.min(image_array)
    max_val = np.max(image_array)

    stretched_image = (image_array - min_val) / (max_val - min_val) * 255
    stretched_image = np.uint8(stretched_image)

    return stretched_image