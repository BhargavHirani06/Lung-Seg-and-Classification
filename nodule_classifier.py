import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
from keras.models import load_model

def classify_nodules(image_folder, model_path, image_width=64, image_height=64):
    """Classifies nodules in images and returns the results."""

    model = load_model(model_path)
    results = [] 

    def preprocess_image(image_path):
        image = plt.imread(image_path)
        resized_image = resize(image, (image_width, image_height, 3))
        return np.expand_dims(resized_image, axis=0)  

    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        image = preprocess_image(image_path)
        prediction = model.predict(image)

        if prediction > 0.5:
            label = 'Malignant'
        else:
            label = 'Benign'

        results.append(f"Image: {image_file}, Predicted Label: {label}, Confidence: {prediction[0][0]:.4f}")

    return results 
