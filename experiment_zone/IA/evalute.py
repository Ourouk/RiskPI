import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from models import preprocess_input, dice
import cv2
import matplotlib.pyplot as plt

def predict(model, path):
        im = cv2.imread(path, 1)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = im.reshape(256, 256, 3)

        im = np.expand_dims(im, axis=0)
        pred = model.predict(im)
        pred = np.squeeze(pred) * 255.0
        mask = add_masks(pred)
        return mask

labels = ['background', 'infantry', 'cavalery', 'artillery']
hues = {'background': 0, 'infantry': 120, 'cavalery': 60, 'artillery': 30}

def add_masks(pred):
        blank = np.zeros(shape=(256,256,3), dtype=np.uint8)

        for i, label in enumerate(labels):
            hue = np.full(shape=(256,256), fill_value=hues[label], dtype=np.uint8)
            sat = np.full(shape=(256,256), fill_value=255, dtype=np.uint8)
            val = pred[:,:,i].astype(np.uint8)

            im_hsv = cv2.merge([hue, sat, val])
            im_rgb = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2RGB)
            blank = cv2.add(blank, im_rgb)

        return blank


if __name__ == "__main__":
        model_path = "models/maskModel.h5"
        image_path = "images/28.jpg"
        target_size = (256, 256) 

        model = tf.keras.models.load_model(model_path, custom_objects={'dice': dice})

        prediction = predict(model, image_path)

        print("Prédiction:", prediction)
        # cv2.imshow('image', prediction)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
