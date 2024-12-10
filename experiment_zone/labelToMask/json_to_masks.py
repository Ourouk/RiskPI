import json
import numpy as np
from PIL import Image, ImageDraw
import os

# Define paths
images_dir = "images/"
annotations_dir = "labels/"
masks_dir = "masks/"
os.makedirs(masks_dir, exist_ok=True)

def hex_to_rgb(hex_color):
    """Convert a hex color (e.g., '#ff0000') to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_mask_from_json(image_path, json_path):
    # Load image to get dimensions
    with Image.open(image_path) as img:
        width, height = img.size

    # Initialize a blank RGB mask (3 channels)
    mask = np.zeros((height, width, 3), dtype=np.uint8)

    # Load annotation JSON
    with open(json_path) as f:
        annotations = json.load(f)

    # Process each polygon object in the JSON
    for obj in annotations:
        # Get the RGB color from 'labelColor' (hex)
        color = (255,0,0)

        # Extract the polygon points
        polygon = [(point["x"], point["y"]) for point in obj["content"]]

         # Create a temporary mask for the polygon in RGB
        img_polygon = Image.new("RGB", (width, height), (0, 0, 0))
        ImageDraw.Draw(img_polygon).polygon(polygon, outline=color, fill=color)

        # Overlay the polygon mask onto the main RGB mask
        mask = np.maximum(mask, np.array(img_polygon))
    
    return mask

# Loop through images and JSON files to create masks
for image_file in os.listdir(images_dir):
    if image_file.endswith(".jpg"):
        image_path = os.path.join(images_dir, image_file)
        json_path = os.path.join(annotations_dir, image_file.replace('.jpg', '.json'))
        
        if os.path.exists(json_path):
            mask = create_mask_from_json(image_path, json_path)
            mask_image = Image.fromarray(mask)
            mask_image.save(os.path.join(masks_dir, image_file))  # Save mask as PNG
