import cv2
import json
import numpy as np
import argparse
import sys
import os

# Try this : 
# python .\mask_pieces.py -i ..\data\gsm\small_images\im31.jpg -o ..\data\gsm\outputs -n test.jpg -d -m -r

def get_mask_pieces(filePath, morphology, rmNoise):
    im = cv2.imread(filePath)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # Convert the image to HSV
    imHSV = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)

    # Open the config file with ranges
    color_range = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'HSV_color_range.json'), 'r'))

    # Mask for red
    lowerR1 = np.array(color_range['red']['lower'])
    upperR1 = np.array(color_range['red']['upper'])
    maskR1 = cv2.inRange(imHSV, lowerR1, upperR1)

    # Mask for saturated red
    lowerR2 = np.array(color_range['red2']['lower'])
    upperR2 = np.array(color_range['red2']['upper'])
    maskR2 = cv2.inRange(imHSV, lowerR2, upperR2)

    # Mask for green
    lowerG = np.array(color_range['green']['lower'])
    upperG = np.array(color_range['green']['upper'])
    maskG = cv2.inRange(imHSV, lowerG, upperG)
    
    # Mask for blue
    lowerB = np.array(color_range['blue']['lower'])
    upperB = np.array(color_range['blue']['upper'])
    maskB = cv2.inRange(imHSV, lowerB, upperB)

    # Mask for yellow
    lowerY = np.array(color_range['yellow']['lower'])
    upperY = np.array(color_range['yellow']['upper'])
    maskY = cv2.inRange(imHSV, lowerY, upperY)
    
    # Applies pre-processing if required
    if morphology:
        maskR1 = cv2.morphologyEx(maskR1, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        maskR2 = cv2.morphologyEx(maskR2, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        maskG = cv2.morphologyEx(maskG, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        maskB = cv2.morphologyEx(maskB, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        maskY = cv2.morphologyEx(maskY, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        
    if rmNoise:
        maskR1 = removeNoise(maskR1)
        maskR2 = removeNoise(maskR2)
        maskG = removeNoise(maskG)
        maskB = removeNoise(maskB)
        maskY = removeNoise(maskY)

    # Add the masks
    mask = np.zeros_like(maskR1)
    cv2.bitwise_or(maskR1, maskR2, mask)
    cv2.bitwise_or(mask, maskG, mask)
    cv2.bitwise_or(mask, maskB, mask)
    cv2.bitwise_or(mask, maskY, mask)

    return mask, [maskR1, maskR2, maskG, maskB, maskY]

def removeNoise(im):
    nb_blobs, im_with_separated_blobs, stats, _ = cv2.connectedComponentsWithStats(im)

    # We retreive the area of each blob
    sizes = stats[:, cv2.CC_STAT_AREA]
    
    # We exclude the background
    blob_sizes = sizes[1:]

    if len(blob_sizes) == 0:
        # If there are no blobs, return the original empty mask
        return np.zeros_like(im, dtype=np.uint8)
    
    # Calculate the mean size of the blobs
    mean_size = np.mean(blob_sizes)

    # create empty output image with will contain only the biggest composents
    im_result = np.zeros_like(im)

    # We keep only the blobs that are in the range
    for index_blob in range(1, nb_blobs):
        if sizes[index_blob] >= mean_size:
            im_result[im_with_separated_blobs == index_blob] = 255
    
    return im_result


def argParsing():
    parser = argparse.ArgumentParser(
        description="This script generates a mask for the given image based on predefined HSV color ranges.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )

    parser.add_argument("-i", "--input", type=str, help="Path to the input image file", required=True)
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", required=True)
    parser.add_argument("-n", "--name", type=str, help="Name of the output file")
    parser.add_argument("-d", "--debug", action="store_true", help="Display every masks and store them in a directory")
    parser.add_argument("-m", "--morphology", action="store_true", help="Adds a pre-processing morphology step to the mask (closing)")
    parser.add_argument("-r", "--removeNoise", action="store_true", help="Process the mask to remove noise (may be slow and remove small pieces)")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The input file {args.input} does not exist.")
    
    if not os.path.isdir(args.output):
        raise NotADirectoryError(f"The output directory {args.output} does not exist.")
    
    return (args.input, args.output, args.name, args.debug, args.morphology, args.removeNoise)

def saveMask(mask, input_path, outputDir, outputFilename):
    if outputFilename is None:
        outputFilename = input_path
    
    output_file = os.path.join(outputDir, os.path.basename(outputFilename))
    
    print(f"Saving mask to {output_file}")
    
    cv2.imwrite(output_file, mask)
    
def saveMasks(masks, outputPath, outputFilename):
    outputFolder = tmp = os.path.join(outputPath, outputFilename.split('.')[0])

    i = 0
    while os.path.exists(outputFolder) or i > 20:
        i = i + 1
        outputFolder = tmp + f"_{i}"
        
    os.mkdir(outputFolder)
    print(f"Saving debug masks to {outputFolder}")
    
    colors = ['red1', 'red2', 'green', 'blue', 'yellow']
    
    for i, color in enumerate(colors):
        output_file = os.path.join(outputFolder, f"{color}.jpg")
        print(f"Saving {color} mask to {output_file}")
        cv2.imwrite(output_file, masks[i])


# Try this : 
# python .\mask_pieces.py -i ..\data\gsm\small_images\im31.jpg -o ..\data\gsm\outputs -n test.jpg -d -m -r
if __name__ == "__main__":
    inputPath, outputPath, outputFilename, debug, morphology, rmNoise = argParsing()
    (mask, masks) = get_mask_pieces(inputPath, morphology, rmNoise)
    
    if debug:
        saveMasks(masks, outputPath, outputFilename)
    
    saveMask(mask, inputPath, outputPath, outputFilename)