from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
from models import dice
import tensorflow.keras.backend as K
import os
import threading

app = Flask(__name__)

# Load the TensorFlow model
ModelPath = "models/maskModel.h5"
global graph
global sess
graph = tf.compat.v1.get_default_graph()
sess = K.get_session()
model = tf.keras.models.load_model(ModelPath, custom_objects={"dice": dice})

# Define labels and hues for masking
labels = ['background', 'infantry', 'cavalery', 'artillery']
hues = {'background': 0, 'infantry': 120, 'cavalery': 60, 'artillery': 30}

def add_masks(pred):
    blank = np.zeros(shape=(256, 256, 3), dtype=np.uint8)

    for i, label in enumerate(labels):
        hue = np.full(shape=(256, 256), fill_value=hues[label], dtype=np.uint8)
        sat = np.full(shape=(256, 256), fill_value=255, dtype=np.uint8)
        val = pred[:, :, i].astype(np.uint8)

        im_hsv = cv2.merge([hue, sat, val])
        im_rgb = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2RGB)
        blank = cv2.add(blank, im_rgb)

    return blank

@app.route("/predict", methods=["POST"])
def predict():
    # Get the file path from the request
    file_path = request.json.get('image_path')
    output_folder = request.json.get('output_folder')
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    # Preprocess the image
    im = cv2.imread(file_path, 1)
    if im is None:
        return jsonify({"error": "Image not found at the provided path"}), 404

    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im = im.reshape(256, 256, 3)
    im = np.expand_dims(im, axis=0)

    # Use the stored graph and session for prediction
    with graph.as_default():
        try:
            # Ensure the session is set correctly
            K.set_session(sess)
            preds = model.predict(im)
        except tf.errors.FailedPreconditionError:
            # If session is not initialized, reinitialize and try again
            K.set_session(sess)
            preds = model.predict(im)

    pred = np.squeeze(preds) * 255.0

    # Apply mask to the prediction
    mask = add_masks(pred)

    # Save the output image to disk
    output_path = newImagePath(file_path, output_folder)
    cv2.imwrite(output_path, mask)

    # Return the output image path in the response
    return jsonify({"output_image_path": output_path})

def newImagePath(image_path, folderPath):
    return os.path.join(folderPath, os.path.basename(image_path))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True)
