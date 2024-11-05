import cv2
import numpy as np
import os
import csv

def divide_image_and_highlight(image_path, square_size, output_path):
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

    # Matrix of min values
    min_matrix = np.zeros((height, width, 3), dtype=np.uint8)
    # Matrix of max values
    max_matrix = np.zeros((height, width, 3), dtype=np.uint8)
    # Matrix of mean values
    mean_matrix = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Iterate over the image in steps of square_size
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # Define the square coordinates
            x_end = min(x + square_size, width)
            y_end = min(y + square_size, height)

            # Extract the square from the image
            square = image[y:y_end, x:x_end]

            # # Calculate the color range (min and max for each channel)
            min_val = np.min(square, axis=(0, 1))
            max_val = np.max(square, axis=(0, 1))
            mean_val = np.mean(square, axis=(0, 1))

            # Round the mean values for each channel
            mean_val = np.round(mean_val, 0)

            # Store min values in the min_matrix
            min_matrix[y:y_end, x:x_end] = min_val
            # Store max values in the max_matrix
            max_matrix[y:y_end, x:x_end] = max_val
            # Store mean values in the mean_matrix
            mean_matrix[y:y_end, x:x_end] = mean_val

            # Format the values to reduce space between them
            mean_str = f"Mean: [{', '.join(f'{val:.0f}' for val in mean_val)}]"
            min_str = f"Min: [{', '.join(str(val) for val in min_val)}]"
            max_str = f"Max: [{', '.join(str(val) for val in max_val)}]"

            # Add text with the mean, min, and max values in a compact format
            cv2.putText(derivative_image, mean_str, (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(derivative_image, min_str, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(derivative_image, max_str, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


            # Highlight the square in the derivative image
            cv2.rectangle(derivative_image, (x, y), (x_end, y_end),(0, 255, 0), 2)

    # Create a min_matrix image
    cv2.imwrite('examples/data/min_matrix.jpg', min_matrix)
    # Create a max_matrix image
    cv2.imwrite('examples/data/max_matrix.jpg', max_matrix)
    # Create a mean_matrix image
    cv2.imwrite('examples/data/mean_matrix.jpg', mean_matrix)
    # Save the derivative image to the specified output file
    cv2.imwrite(output_path, derivative_image)
    print(f"Derivative image saved to: {output_path}")

# Example usage
image_path = 'data/vuedessus.jpg'  # Replace with your input image path
square_size = 25  # Change this to your desired square size
output_path = 'examples/data/output_image.jpg'  # Specify the output file path
divide_image_and_highlight(image_path, square_size, output_path)
