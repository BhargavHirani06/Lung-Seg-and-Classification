# nodule_predictor.py
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K

# Dice Coefficient and Loss Functions
smooth = 1e-15

def dice_coef(y_true, y_pred):
    y_true = tf.keras.layers.Flatten()(y_true)
    y_pred = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true * y_pred)
    if tf.reduce_sum(y_true) == 0:
        return tf.constant(1.0)
    else:
        return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)

def dice_loss(y_true, y_pred):
    return 1.0 - dice_coef(y_true, y_pred)

# Intersection over Union (IoU) and Loss Functions
def iou(y_true, y_pred):
    intersection = K.sum(K.abs(y_true * y_pred))
    sum_ = K.sum(y_true) + K.sum(y_pred)

    if K.sum(y_true) == 0:
        return tf.constant(1.0)
    else:
        jac = intersection / (sum_ - intersection)
        return jac

def iou_loss(y_true, y_pred):
    return 1 - iou(y_true, y_pred)

# Preprocessing and Prediction
def preprocess_image_for_prediction(image_path):
    x = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Load image in color
    x = cv2.resize(x, (128, 128))
    x = x / 255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x, axis=0)  # Adding a batch dimension for prediction
    return x

def save_prediction_as_image(predicted_mask, save_path):
    predicted_mask = (predicted_mask.squeeze() * 255.0).astype(np.uint8)
    cv2.imwrite(save_path, predicted_mask)

# Main Prediction Function
def predict_nodules(input_folder, output_folder, model_path):
    """Loads the model and predicts nodules for images in the input folder."""

    model = tf.keras.models.load_model(
        model_path,
        custom_objects={
            "dice_loss": dice_loss,
            "iou": iou,
            "dice_coef": dice_coef,
        },
    )

    os.makedirs(output_folder, exist_ok=True)

    for image_file in os.listdir(input_folder):
        if image_file.lower().endswith((".png", ".jpg")):
            image_path = os.path.join(input_folder, image_file)
            image_to_predict = preprocess_image_for_prediction(image_path)
            predicted_mask = model.predict(image_to_predict)
            mask_save_path = os.path.join(output_folder, image_file)
            save_prediction_as_image(predicted_mask, mask_save_path)
