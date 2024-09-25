# patch_extractor_from_coordinates.py

import cv2
import numpy as np
import os
from PIL import Image

def extract_patches_from_coordinates(annotations_folder, patch_folder, patch_size=64):
    """Extracts patches of the specified size from images in the patch folder based on coordinates calculated from images in the annotations folder."""

    half_patch_size = patch_size // 2

    for filename in os.listdir(annotations_folder):
        if filename.endswith((".png", ".jpg")):
            annotation_path = os.path.join(annotations_folder, filename)
            patch_path = os.path.join(patch_folder, filename)  # Assuming the same filename in the patch folder

            # Calculate center coordinates from the annotation image
            img = cv2.imread(annotation_path, 0)  
            _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

            white_pixel_count = np.sum(thresh == 255)
            total_x = np.sum(np.where(thresh == 255)[1])
            total_y = np.sum(np.where(thresh == 255)[0])

            if white_pixel_count > 0:
                center_x = total_x // white_pixel_count
                center_y = total_y // white_pixel_count
            else:
                print(f"Warning: No white pixels found in annotation {filename}. Skipping patch extraction.")
                continue

            # Extract patch from the corresponding image in the patch folder
            with Image.open(patch_path) as img:
                top_left_x = max(0, center_x - half_patch_size)
                top_left_y = max(0, center_y - half_patch_size)

                if top_left_x + patch_size > img.width:
                    top_left_x = img.width - patch_size
                if top_left_y + patch_size > img.height:
                    top_left_y = img.height - patch_size

                patch = img.crop((top_left_x, top_left_y, top_left_x + patch_size, top_left_y + patch_size))
                patch.save(os.path.join(patch_folder, filename)) 
