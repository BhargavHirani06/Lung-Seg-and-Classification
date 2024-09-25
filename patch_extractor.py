import os
import cv2

def extract_patches(image_path, output_dir, patch_size=128, overlap=0.5):
    """Extracts patches from an image and saves them in the specified directory."""

    original_image = cv2.imread(image_path)
    image_name_noext = os.path.splitext(os.path.basename(image_path))[0]

    patch_width, patch_height = patch_size, patch_size
    stride_width = int(patch_width * (1 - overlap))
    stride_height = int(patch_height * (1 - overlap))

    os.makedirs(output_dir, exist_ok=True)  # Create output directory if not exists
    patch_count = 0

    for y in range(0, original_image.shape[0] - patch_height + 1, stride_height):
        for x in range(0, original_image.shape[1] - patch_width + 1, stride_width):
            patch = original_image[y:y+patch_height, x:x+patch_width]
            patch_filename = f"{image_name_noext}_patch_{patch_count+1}.jpg"
            patch_path = os.path.join(output_dir, patch_filename)
            cv2.imwrite(patch_path, patch)
            patch_count += 1
