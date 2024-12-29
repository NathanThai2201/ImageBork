import os
from sklearn.cluster import KMeans
from scipy import spatial
from skimage import io, color, img_as_float, img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt

def main(image):
    
    # image = io.imread('in.png').astype(np.uint8)
    image = image[:, :, :3]
    matrix = [[10],
              [200],
              [255],
              [200],
              [10]]

    h, w, _ = image.shape
    # create scanlines
    scanlines = np.copy(image)
    for row in range(0,h,1):
        for col in range(0, w, 1):
            newpixel = matrix[row%5]
            scanlines[row, col] = newpixel

    # overlay
    img_f = color.gray2rgb(scanlines)
    img1 = img_as_float(image)
    img2 = img_as_float(scanlines)
    
    # Ensure the images are the same size
    if img1.shape != img2.shape:
        img2 = np.resize(img2, img1.shape)
    
    blended = img1 * img2
    blended = img_as_ubyte(np.clip(blended, 0, 1))

    # io.imsave('out.png', blended)
    return blended

if __name__ == "__main__":
    main()
