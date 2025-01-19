import time
import threading
import tkinter as tk
from tkinter import ttk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageTk
import requests
import numpy as np
from io import BytesIO

watch_folder = "./watch_folder"


class ImageWatcher(FileSystemEventHandler):
    def __init__(self, original_label, prediction_label):
        self.original_label = original_label
        self.prediction_label = prediction_label
        self.current_image = None
        self.predicted_image = None

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith((".png", ".jpg", ".jpeg")):
            time.sleep(0.5)  # Wait for the file to be fully written
            print(f"New image detected: {event.src_path}")
            
            # Display the original image
            self.current_image = Image.open(event.src_path).resize((400, 400))
            img_tk = ImageTk.PhotoImage(self.current_image)
            self.original_label.config(image=img_tk)
            self.original_label.image = img_tk  # Keep a reference to avoid garbage collection

            # Send the image to the API for prediction            
            img_path = self.send_image_to_api(event.src_path)

            # Display the predicted image
            self.predicted_image = Image.open(img_path).resize((400, 400))
            img_predicted_tk = ImageTk.PhotoImage(self.predicted_image)
            self.prediction_label.config(image=img_predicted_tk)
            self.prediction_label.image = img_predicted_tk


    
    def send_image_to_api(self, image_path):
        url = "http://127.0.0.1:5000/predict"
        
        # Send the image path as a JSON request
        response = requests.post(url, json={"image_path": image_path, "output_folder": "./output_folder"})

        if response.status_code == 200:
            # Get the output image path from the response
            response_data = response.json()
            output_image_path = response_data["output_image_path"]
            return output_image_path
        else:
            return f"Error: {response.status_code}"
     
    

def start_folder_watcher(folder, original_label, prediction_label):
    event_handler = ImageWatcher(original_label, prediction_label)
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    observer.join()

def create_gui():
    root = tk.Tk()
    root.title("TensorFlow Model & Image Viewer")

    # Create a frame to hold both images side by side
    images_frame = ttk.Frame(root)
    images_frame.pack(pady=20, side="bottom")

    # Create a frame to hold the original image
    original_frame = ttk.Frame(images_frame)
    original_frame.pack(side="left", padx=20)

    prediction_frame = ttk.Frame(images_frame)
    prediction_frame.pack(side="left", padx=20)

    # Title Label
    title_label = ttk.Label(root, text="TensorFlow Model & Image Viewer", font=("Arial", 16))
    title_label.pack(pady=10, side="top")

    # Title Original Image
    title_original_image = ttk.Label(original_frame, text="Original Image", font=("Arial", 12))
    title_original_image.pack(pady=10, side="top")

    # Image Display (Original Image)
    original_image_label = ttk.Label(original_frame)
    original_image_label.pack(side="bottom", padx=20)  # Align to left with padding

    # Title Prediction
    title_prediction = ttk.Label(prediction_frame, text="Prediction", font=("Arial", 12))
    title_prediction.pack(pady=10, side="top")

    # Prediction Display
    prediction_label = ttk.Label(prediction_frame)
    prediction_label.pack(side="bottom", padx=20)  # Align to left with padding

    # Start folder watcher
    monitor_thread = threading.Thread(
        target=start_folder_watcher, args=(watch_folder, original_image_label, prediction_label), daemon=True
    )
    monitor_thread.start()

    root.mainloop()




if __name__ == "__main__":
    create_gui()
