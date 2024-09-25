import pydicom
import numpy as np
from PIL import Image
import os

use_16bit_depth = False

def normalize_and_convert(dicom_file_path,window_center=-600, window_width=1600):
    ds = pydicom.dcmread(dicom_file_path)
    pixel_array = ds.pixel_array

    try:
        slope = ds.RescaleSlope
        intercept = ds.RescaleIntercept
    except AttributeError:
        slope = 1
        intercept = 0

    pixel_array = pixel_array * slope + intercept

    min_value = window_center - window_width // 2
    max_value = window_center + window_width // 2
    pixel_array = np.clip(pixel_array, min_value, max_value)

    pixel_array = ((pixel_array - min_value) / (max_value - min_value)) * 255
    pixel_array = pixel_array.astype(np.uint8)

    image = Image.fromarray(pixel_array)
    if use_16bit_depth:
        image = image.convert("I")

    output_filename = "Image.png"
    output_file = os.path.join(output_filename)

    image.save(output_file)
    return output_file
