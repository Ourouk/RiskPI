import cv2
import numpy as np
import os

def simplify(image_path, square_size, output_path):
    # Check if the file exists
    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not open or find the image at {image_path}.")
        return

    height, width, _ = image.shape

    # Create a derivative image (copy of the original)
    derivative_image = image.copy()

    # erode the image
    kernel = np.ones((5,5),np.uint8)
#gradient
    derivative_image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    # dilatation
    derivative_image = cv2.dilate(derivative_image, kernel, iterations=1)


    # Save the derivative image to the specified output file
    cv2.imwrite(output_path, derivative_image)
    print(f"Derivative image saved to: {output_path}")

# Example usage
image_path = 'data/vuedessus.jpg'  # Replace with your input image path
square_size = 200  # Change this to your desired square size
output_path = 'experiment_zone/data/output_image.jpg'  # Specify the output file path
simplify(image_path, square_size, output_path)
