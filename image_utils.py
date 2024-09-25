import os
import cv2
import numpy as np

def remove_images(directory, threshold=400):
    """Removes images from a directory with a high proportion of white pixels."""
    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".png")):
            img = cv2.imread(os.path.join(directory, filename), 0)  # Load as grayscale
            white_pixels = np.sum(img >= 240)
            total_pixels = np.prod(img.shape)
            print(white_pixels)

            if white_pixels <= threshold:
                os.remove(os.path.join(directory, filename))
                print(f"Removed: {filename}")

def find_missing_file(folder1, folder2):
    """Finds files in folder2 that are not in folder1."""
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))
    missing_files = files2 - files1
    return missing_files

def delete_files(folder, files):
    """Deletes the specified files from a folder."""
    for file_name in files:
        file_path = os.path.join(folder, file_name)
        os.remove(file_path)
        print(f"Deleted: {file_path}")
