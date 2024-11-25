import cv2
import numpy as np
import os
import sys
import argparse

# Try this syntax :
# python fourPointTransform.py -i input.png -o output_dir -tl 10,10 -bl 10,100 -tr 100,10 -br 100,100
def fourPointTransform(imagePath, topLeft, bottomLeft, topRight, bottomRight):
    # Ouverture de l'image
    image = cv2.imread(imagePath)
    rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)


    # calculating the distance between points ( Pythagorean theorem ) 
    height_1 = np.sqrt(((topLeft[0] - bottomLeft[0]) ** 2) + ((topLeft[1] - bottomLeft[1]) ** 2))
    height_2 = np.sqrt(((topRight[0] - bottomRight[0]) ** 2) + ((topRight[1] - bottomRight[1]) ** 2))

    width_1 = np.sqrt(((topLeft[0] - topRight[0]) ** 2) + ((topLeft[1] - topRight[1]) ** 2))
    width_2 = np.sqrt(((bottomLeft[0] - bottomRight[0]) ** 2) + ((bottomLeft[1] - bottomRight[1]) ** 2))

    max_height=max(int(height_1), int(height_2))
    max_width = max(int(width_1), int(width_2))

    # four input point 
    input_pts=np.float32([topLeft,bottomLeft,topRight,bottomRight])

    # output points for new transformed image
    output_pts = np.float32([[0, 0],
                            [0, max_width],
                            [max_height , 0],
                            [max_height , max_width]])


    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(input_pts,output_pts)

    out = cv2.warpPerspective(rgb_image,M,(max_height, max_width),flags=cv2.INTER_LINEAR)
    out = cv2.resize(out, image.shape[1::-1])

    return out

def saveFourPointTransform(imagePath, outputDir, topLeft, bottomLeft, topRight, bottomRight, outputName=None):
    out = fourPointTransform(imagePath, topLeft, bottomLeft, topRight, bottomRight)
    
    if outputName is not None:
        outputDir = f"{outputDir}/{outputName}"
    else:
        outputDir = f"{outputDir}/{os.path.basename(imagePath)}"
        
    cv2.imwrite(outputDir, cv2.cvtColor(out, cv2.COLOR_RGB2BGR))

def argParsing():
    parser = argparse.ArgumentParser(
        description="This script applies a four point transform on a image given the four points you want to crop it with.\nExample: python fourPointTransform.py -i input.png -o output_dir -tl 10,10 -bl 10,100 -tr 100,10 -br 100,100\nThis crops the image 'input.png' with top right coordinate (10,10) bottom left coordinate (10,100) top right coordinate (100,10) and bottom right coordinate (100,100).",  
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )

    parser.add_argument("-i", "--input", type=str, help="Path to the input file", required=True)
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", required=True)
    parser.add_argument("-n", "--name", type=str, help="Name of the output file")
    parser.add_argument("-tl", "--topLeft", type=point, help="Top left point of the crop", required=True)
    parser.add_argument("-bl", "--bottomLeft", type=point, help="Bottom left point of the crop", required=True)
    parser.add_argument("-tr", "--topRight", type=point, help="Top right point of the crop", required=True)
    parser.add_argument("-br", "--bottomRight", type=point, help="Bottom right point of the crop", required=True)
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.reference):
        raise FileNotFoundError(f"The reference file {args.reference} does not exist.")
    
    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The input file {args.input} does not exist.")
    
    if not os.path.isdir(args.output):
        raise NotADirectoryError(f"The output directory {args.output} does not exist.")
    
    return (args.input, args.output, args.name, args.topLeft, args.bottomLeft, args.topRight, args.bottomRight)
    
def point(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Point must be x,y")
    
    
# Try this syntax :
# python fourPointTransform.py -i ../data/gsm/ref/1.jpg -o ../data/gsm/outputs -tl 180, 210 -bl 130,1400 -tr 2020,210 -br 2300,1415 -n fourPointTransform.jpg
if __name__ == "__main__":
    (filePath, outputPath, outputName, topLeft, bottomLeft, topRight, bottomRight) = argParsing()
    saveFourPointTransform(filePath, outputPath, topLeft, bottomLeft, topRight, bottomRight, outputName)