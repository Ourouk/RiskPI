import cv2
import numpy as np
import os
import sys
import argparse

TopLeft = (63, 933)
BottomRight = (376, 1481)

def findBottomLeftQuadrant(image):
    # Find the bottom left quadrant of the board
    (x1, y1) = TopLeft
    (x2, y2) = BottomRight
    
    return image[y1:y2, x1:x2]

# To do
def findPiecesOnQuadrant(image):
    return None
    
def parseArg():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        description="This script extracts the bottom left quadrant from the board RISK. !! The four point transform must have happenned before.\nExample: python findPiecesColors.py -i input.png -o output_dir -r outputImage.png\n",  
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    
    parser.add_argument("-i", "--input", type=str, help="Path to the input file", required=True)
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", required=True)
    parser.add_argument("-n", "--name", type=str, help="Name of the output file")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    
    return (args.input, args.output, args.name)
    
# Try this :
# findPiecesColors.py -i ../data/gsm/outputs/fourPointTransform.jpg -o ../data/gsm/outputs -n quadrant.png
if __name__ == "__main__":
    (inputPath, outputDir, name) = parseArg()
    
    # Load the image
    image = cv2.imread(inputPath)
    
    # Find the bottom left quadrant of the board
    bottomLeftQuadrant = findBottomLeftQuadrant(image)

    if name is not None:
        outputDir = f"{outputDir}/{name}"
    else:
        outputDir = f"{outputDir}/{os.path.basename(inputPath)}"
        
    cv2.imwrite(outputDir, bottomLeftQuadrant)
    
    # Save the bottom left quadrant    
    print(f"Bottom left quadrant saved to {outputDir}/bottom_left_quadrant.jpg")
    
    sys.exit(0)