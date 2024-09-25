import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import is_dcm_file
import convert_dcm
import patch_extractor
import nodule_predictor
import image_utils
import patch_extractor_from_coordinates
import nodule_classifier
import os
import shutil
import threading
from PIL import Image, ImageTk

image_frame = None


def reset_output():
    global image_frame
    file_path_entry.delete(0, tk.END)
    output_text.delete("1.0", tk.END)

    if image_frame:
        for widget in image_frame.winfo_children():
            widget.destroy()
        image_frame.pack_forget()
        image_frame = None


def process_dicom(file_path):
    if not file_path or not is_dcm_file.check_dcm(file_path):
        output_text.insert(tk.END, "Invalid DICOM file selected.\n")
        return

    patch_folder_name = "patch"
    output_folder = "annotations"

    script_dir = os.path.dirname(__file__)
    model_path = os.path.join(script_dir, "model.h5")
    model_path_c = os.path.join(script_dir, "my_model_innet.h5")

    png_file_path = convert_dcm.normalize_and_convert(file_path)
    output_text.insert(tk.END, "Conversion Done !!!!!!!!!!\n")

    if png_file_path:
        png_dir = os.path.dirname(png_file_path)
        patch_output_dir = os.path.join(png_dir, patch_folder_name)
        os.makedirs(patch_output_dir, exist_ok=True)
        patch_extractor.extract_patches(png_file_path, patch_output_dir)
        output_text.insert(tk.END, "Patches Created !!!!!!!!!!\n")

        nodule_predictor.predict_nodules(
            patch_output_dir, output_folder, model_path
        )
        output_text.insert(tk.END, "Nodules Segmented !!!!!!!!!1\n")

        image_utils.remove_images(output_folder)
        missing_files = image_utils.find_missing_file(output_folder, patch_output_dir)
        image_utils.delete_files(patch_output_dir, missing_files)
        output_text.insert(tk.END, "Black and unwanted data is cleaned !!!!!!!!!!\n")

        patch_extractor_from_coordinates.extract_patches_from_coordinates(output_folder, patch_output_dir)
        output_text.insert(tk.END, "Nodules identified and Resized to 64*64\n")

        results = nodule_classifier.classify_nodules(patch_folder_name, model_path_c)
        if results:
            for result in results:
                output_text.insert(tk.END, f"{result}\n")
        else:
            output_text.insert(tk.END, "No nodules found or classification failed.\n")

        patch_from_coordinates_folder = 'patch'
        image_files = [f for f in os.listdir(patch_from_coordinates_folder) if f.endswith('.jpg')]
        image_frame = tk.Frame(window)
        image_frame.pack(pady=10)
        image_width = 100
        image_height = 100

        for image_file in image_files:
            image_path = os.path.join(patch_from_coordinates_folder, image_file)
            try:
                img = Image.open(image_path)
                img = img.resize((image_width, image_height))
                img_tk = ImageTk.PhotoImage(img)
                image_label = tk.Label(image_frame, image=img_tk)
                image_label.image = img_tk
                image_label.pack(side=tk.LEFT, padx=5) 
                output_text.insert(tk.END, f"Displaying: {image_file}\n")
            except Exception as e:
                output_text.insert(tk.END, f"Error displaying image {image_file}: {e}\n")
        os.remove(png_file_path)
        shutil.rmtree(output_folder)
        
        # Auto-adjust window size to fit images
        window.update_idletasks()
        required_width = len(image_files) * (image_width + 5) + 20
        window.geometry(f"{required_width}x500")  
        
    else:
        output_text.insert(tk.END, "Error converting DICOM to PNG. Please check the file or conversion process.\n")



# Create main window
window = tk.Tk()
window.title("DICOM Nodule Prediction")
window.geometry("600x400")


# File path input
file_path_label = tk.Label(window, text="DICOM File Path:")
file_path_label.pack(pady=10)
file_path_entry = tk.Entry(window, width=50)
file_path_entry.pack()

# Button frame to hold Predict, Reset, and End buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

# Predict button
def on_predict_click():
    file_path = file_path_entry.get()
    threading.Thread(target=process_dicom, args=(file_path,)).start()  

predict_button = tk.Button(button_frame, text="Predict", command=on_predict_click)
predict_button.pack(side=tk.LEFT, padx=5)

# Reset button
reset_button = tk.Button(button_frame, text="Reset", command=reset_output)
reset_button.pack(side=tk.LEFT, padx=5)

# End button
def on_end_click():
    window.destroy()

end_button = tk.Button(button_frame, text="End", command=on_end_click)
end_button.pack(side=tk.LEFT, padx=5)

# Output text area
output_text = scrolledtext.ScrolledText(window, width=70, height=15)
output_text.pack(pady=10)

# Image frame (initialized earlier)
image_frame = tk.Frame(window)
image_frame.pack(pady=10)

window.mainloop()
