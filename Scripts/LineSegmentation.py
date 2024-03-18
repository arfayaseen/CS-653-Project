import numpy as np
from PIL import Image
import os

def find_clusters(peaks):
    clusters = []
    cluster = [peaks[0]]
    
    for i in range(1, len(peaks)):
        if peaks[i] - peaks[i-1] == 1:
            cluster.append(peaks[i])
        else:
            clusters.append(cluster)
            cluster = [peaks[i]]
    clusters.append(cluster)
    return clusters

def crop_image_by_clusters(image, clusters):
    cropped_images = []

    for i in range(len(clusters)-1):
        top = clusters[i][0]
        if top != 0:
            top = top - 3
        bottom = clusters[i+1][-1]
        if bottom != clusters[-1][-1]:
            bottom = bottom + 3
        cropped_image = image.crop((0, top, image.width, bottom))
        cropped_images.append(cropped_image)
    return cropped_images

def segment_lines_of_text(image_array):
    row_sum = np.sum(image_array, axis=1)
    row_sum_normalized = row_sum / np.max(row_sum) * 255
    
    threshold = 202
    peaks = np.where(row_sum_normalized > threshold)[0]
    # print(peaks)
    clusters = find_clusters(peaks)
    # print(clusters)

    image = Image.fromarray(image_array)
    cropped_images = crop_image_by_clusters(image, clusters)

    i=1
    cropped_images_dir = './cropped_images_for_ocr/'
    if not os.path.exists(cropped_images_dir):
        os.makedirs(cropped_images_dir)
    for smol_image in cropped_images:
        image_path =  os.path.join(cropped_images_dir, f"input_image_{i}.bmp")
        smol_image.save(image_path)
        i += 1

def unique_values(d):
    seen_values = set()
    new_dict = {}
    for key, value in d.items():
        if value not in seen_values:
            seen_values.add(value)
            new_dict[key] = value
        if len(new_dict) == 3:
            break
    # print(new_dict)
    # print(seen_values)
    return new_dict