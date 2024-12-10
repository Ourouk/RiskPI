import os
import cv2
from pathlib import Path
from mask_pieces import get_mask_pieces

import argparse
import sys



def process_images_in_folder(input_folder, output_folder):
    """
    Processes all images in the input folder and saves the processed images in the output folder.

    Args:
        input_folder (str): Path to the folder containing input images.
        output_folder (str): Path to the folder to save processed images.
    """
    # Ensure the output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Iterate over all files in the input folder
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)

        # Check if the file is an image
        if not os.path.isfile(input_path) or not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            print(f"Skipping non-image file: {file_name}")
            continue

        try:
            # Process the image
            processed_image, _ = get_mask_pieces(input_path, True, True)

            # Construct the output path
            output_path = os.path.join(output_folder, file_name)

            # Save the processed image
            cv2.imwrite(output_path, processed_image)
            print(f"Processed and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

def argParsing():
    parser = argparse.ArgumentParser(
        description="This script applies a preprocess to every image in a given folder and saves the processed images in an output folder.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )

    parser.add_argument("-i", "--input", type=str, help="Path to the input folder", required=True)
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", required=True)
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input):
        raise FileNotFoundError(f"The input file {args.input} does not exist.")
    
    if not os.path.isdir(args.output):
        raise NotADirectoryError(f"The output directory {args.output} does not exist.")
    
    return (args.input, args.output)

if __name__ == "__main__":
    (input_folder, output_folder) = argParsing()
    process_images_in_folder(input_folder, output_folder)
