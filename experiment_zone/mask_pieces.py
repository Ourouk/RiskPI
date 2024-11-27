import cv2
from plotly_util import displayImages
import json
import numpy as np

def get_mask_pieces(filePath):
    im = cv2.imread(filePath)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    # Convert the image to HSV
    imHSV = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)

    # Open the config file with ranges
    color_range = json.load(open('HSV_color_range.json', 'r'))

    # Mask for red
    lowerR1 = np.array(color_range['red']['lower'])
    upperR1 = np.array(color_range['red']['upper'])

    maskR1 = cv2.inRange(imHSV, lowerR1, upperR1)
    cv2.morphologyEx(maskR1, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), maskR1)

    # Mask for saturated red
    lowerR2 = np.array(color_range['red2']['lower'])
    upperR2 = np.array(color_range['red2']['upper'])

    maskR2 = cv2.inRange(imHSV, lowerR2, upperR2)
    cv2.morphologyEx(maskR2, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), maskR2)

    # Mask for green
    lowerG = np.array(color_range['green']['lower'])
    upperG = np.array(color_range['green']['upper'])

    maskG = cv2.inRange(imHSV, lowerG, upperG)
    cv2.morphologyEx(maskG, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), maskG)

    # Mask for blue
    lowerB = np.array(color_range['blue']['lower'])
    upperB = np.array(color_range['blue']['upper'])

    maskB = cv2.inRange(imHSV, lowerB, upperB)
    cv2.morphologyEx(maskB, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), maskB)

    # Mask for yellow
    lowerY = np.array(color_range['yellow']['lower'])
    upperY = np.array(color_range['yellow']['upper'])

    maskY = cv2.inRange(imHSV, lowerY, upperY)
    cv2.morphologyEx(maskY, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), maskY)


    # Add the masks
    mask = np.zeros_like(maskR1)
    cv2.bitwise_or(maskR1, maskR2, mask)
    cv2.bitwise_or(mask, maskG, mask)
    cv2.bitwise_or(mask, maskB, mask)
    cv2.bitwise_or(mask, maskY, mask)

    return mask

if __name__ == "__main__":
    mask = get_mask_pieces('../21.jpg')
    cv2.imwrite('mask.jpg', mask)
    # displayImages([(mask, 'mask')], (1,2))