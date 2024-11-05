import cv2
import numpy as np
import os

def detect_board_end(image_path, square_size, output_path):
    # Check if the file exists
    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not open or find the image at {image_path}.")
        return

    #Define the looked after color in hsv rgbg 0.2126, 0.7152, 0.022,2.2
    # Initial RGB values
    red = 179
    green = 2
    blue = 18
    #define a tolerated range around the color
    tolerance = 0.3
    real_tolerance = round(tolerance*255, 0)
    #convert the color to hsv
    lower_range = np.array([red-real_tolerance, green-real_tolerance, blue-real_tolerance])
    upper_range = np.array([red+real_tolerance, green+real_tolerance, blue+real_tolerance])
    #convert the image to hsv
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #create a mask
    mask = cv2.inRange(image_rgb, lower_range, upper_range)
    #apply the mask
    derivative_image = cv2.bitwise_and(image, image, mask=mask)

    # Save the derivative image to the specified output file
    cv2.imwrite(output_path, derivative_image)
    print(f"Derivative image saved to: {output_path}")

# Example usage
image_path = 'data/vuedessus.jpg'  # Replace with your input image path
square_size = 200  # Change this to your desired square size
output_path = 'experiment_zone/data/output_image.jpg'  # Specify the output file path
detect_board_end(image_path, square_size, output_path)
