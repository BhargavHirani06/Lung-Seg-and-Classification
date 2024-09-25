# main.py
import is_dcm_file
import convert_dcm
import patch_extractor
import nodule_predictor
import image_utils
import patch_extractor_from_coordinates
import nodule_classifier
import os
import shutil

def main():
    patch_folder_name = "patch"
    output_folder = "annotations"
    

    # Get the directory where main.py is located
    script_dir = os.path.dirname(__file__)
    model_path = os.path.join(script_dir, "model.h5")
    model_path_c = os.path.join(script_dir, "my_model_innet.h5")

    while True:
        file_path = input("Enter the path to your DICOM file: ")

        if is_dcm_file.check_dcm(file_path):
            # Convert DICOM to PNG and get the file path
            png_file_path = convert_dcm.normalize_and_convert(file_path)
            print("Convertion Done !!!!!!!!!!")

            if png_file_path:
                png_dir = os.path.dirname(png_file_path)
                patch_output_dir = os.path.join(png_dir, patch_folder_name)
                os.makedirs(patch_output_dir, exist_ok=True)
                patch_extractor.extract_patches(png_file_path, patch_output_dir)
                print("Patches Created !!!!!!!!!!")

                # Predict nodules
                nodule_predictor.predict_nodules(patch_output_dir, output_folder, model_path)
                print("Nodules Segmented !!!!!!!!!!")

                # Remove images with excess white pixels
                image_utils.remove_images(output_folder)
                
                # Find and delete missing files in the patch folder
                missing_files = image_utils.find_missing_file(output_folder, patch_output_dir)
                image_utils.delete_files(patch_output_dir, missing_files)
                print("Black and unwanted data is cleaned !!!!!!!!!!")

                # Extract patches based on coordinates (directly from the output folder)
                patch_extractor_from_coordinates.extract_patches_from_coordinates(output_folder, patch_output_dir)
                print("Nodules identified and Resized to 64*64")

                # Classify nodules
                nodule_classifier.classify_nodules(patch_folder_name, model_path_c)

                os.remove(png_file_path)
                shutil.rmtree(output_folder)


            else:
                print(
                    "Error converting DICOM to PNG. Please check the file or conversion process."
                )

            break  # Exit the loop after processing one file
        else:
            print("Please select a valid DICOM (.dcm) file.")

if __name__ == "__main__":
    main()
