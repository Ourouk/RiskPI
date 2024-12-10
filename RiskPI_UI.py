import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

from experiment_zone.mask_pieces import get_mask_pieces

# Placeholder for your backend script
def process_image(input_path):
    full_mask, _ = get_mask_pieces(input_path, False, False)
    return full_mask

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing UI")
        self.root.geometry("800x600")

        # Original and Processed Image Containers
        self.original_image = None
        self.processed_image = None

        # Layout
        self.setup_ui()

    def setup_ui(self):
        # Buttons
        self.btn_load = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.btn_process = tk.Button(self.root, text="Process Image", command=self.process_image, state=tk.DISABLED)
        self.btn_process.pack(pady=10)

        self.btn_save = tk.Button(self.root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.btn_save.pack(pady=10)

        # Canvas to display images
        self.canvas_original = tk.Canvas(self.root, width=400, height=400, bg="gray")
        self.canvas_original.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas_processed = tk.Canvas(self.root, width=400, height=400, bg="gray")
        self.canvas_processed.pack(side=tk.RIGHT, padx=10, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
        )
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.canvas_original)
            self.btn_process.config(state=tk.NORMAL)

    def process_image(self):
        if not self.original_image:
            messagebox.showerror("Error", "No image loaded!")
            return
        
        try:
            # Run your backend processing script
            self.processed_image = process_image(self.original_image.filename)
            self.display_image(self.processed_image, self.canvas_processed)
            self.btn_save.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Processing Error", f"An error occurred: {e}")

    def save_image(self):
        if not self.processed_image:
            messagebox.showerror("Error", "No processed image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred: {e}")

    def display_image(self, image, canvas):
        # If the input is a numpy array, convert it to a PIL Image
        if isinstance(image, np.ndarray):
            if len(image.shape) == 2:  # Grayscale
                image = Image.fromarray(image)
            else:  # Color (Assuming BGR format from OpenCV)
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Resize the image to fit the canvas
        img = image.copy()
        img.thumbnail((400, 400))
        tk_image = ImageTk.PhotoImage(img)
        canvas.create_image(200, 200, image=tk_image, anchor=tk.CENTER)
        canvas.image = tk_image  # Prevent garbage collection


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
