
Medical Image Nodule Classification System

This project is designed to classify nodules from DICOM (Digital Imaging and Communications in Medicine) images using deep learning techniques. It includes various utilities for handling DICOM images, extracting patches, and running a classification model to detect potential nodules.

Table of Contents
- Overview
- Features
- Requirements
- Installation
- Usage
- Project Structure
- Contributing
- License

Overview
This repository provides tools to:
- Convert DICOM files into image formats for processing.
- Preprocess DICOM images by extracting patches.
- Classify the images using a nodule classifier to identify nodules.
- Run predictions on DICOM files for detecting nodules.

Features
- DICOM File Handling: Convert and validate DICOM files for use in medical imaging workflows.
- Patch Extraction: Extract patches from images based on coordinates.
- Nodule Classification: Use a deep learning model to classify nodules from patches of medical images.

Requirements
The required dependencies are listed in the requirements.txt file:
pydicom
opencv-python
numpy
pillow
pandas
tensorflow
scikit-image
matplotlib

Installation
1. Clone the repository:
   git clone https://github.com/your-repo-url/nodule-classifier.git
   cd nodule-classifier

2. Install the dependencies:
   pip install -r requirements.txt

Usage

1. Converting DICOM Files
You can convert DICOM files to standard image formats for easier processing using:
   python convert_dcm.py <path-to-dicom-file>

2. Nodule Prediction
Run nodule predictions on DICOM images:
   python nodule_predictor.py <path-to-dicom-file>

3. Extracting Patches
Extract patches from DICOM images based on given coordinates:
   python patch_extractor_from_coordinates.py <path-to-dicom-file> <coordinates>

4. Running the GUI
To launch the GUI for the application:
   python Main(GUI).py

Project Structure

convert_dcm.py                   # Convert DICOM files to standard image formats
image_utils.py                   # Utilities for image processing
is_dcm_file.py                   # Checks if a file is in DICOM format
Main(GUI).py                     # GUI for the system
main.py                          # Main execution file
nodule_classifier.py             # Nodule classification model and utilities
nodule_predictor.py              # Runs predictions for nodules in DICOM files
patch_extractor.py               # Extracts patches from images
patch_extractor_from_coordinates.py # Extract patches based on coordinates
requirements.txt                 # Project dependencies

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License.
