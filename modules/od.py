import os
from sklearn.cluster import KMeans
from scipy import spatial
from skimage import io, color, img_as_float, img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt

def nearest(palette, colour):
    dist, i = palette.query(colour)
    return palette.data[i]

def makePalette(colours):
    return spatial.KDTree(colours)

def findPalette(image, nColours):
    newres = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=nColours, n_init=10).fit(newres)
    colours = kmeans.cluster_centers_

    colours_img = np.zeros((50, int(nColours*50), 3), dtype=np.float32)
    start_id = 0
    for col_id in range(nColours):
        end_id = start_id + 50
        colours_img[:, start_id:end_id, :] = colours[col_id, :]
        start_id = end_id

    # print(f'colours:\n{colours}')
    #plt.figure(figsize=(10, 5))
    # plt.imshow(colours_img)
    # colours =[[0.91219912, 0.3257617,  0.21832768],
    #           [0.70676912 ,0.72203413 ,0.68072663],
    #           [0.41088001, 0.42779406, 0.31911404],
    #           [0.52587285 ,0.73030921, 0.87671832],
    #           [0.24926086, 0.24574098, 0.20012105],
    #           [0.47650788, 0.56045069, 0.53032372],
    #           [0.7265762 , 0.62201352, 0.36742985]]
    return makePalette(colours)

def OrderedDitheringColor(image, palette):
    matrix = [[0 ,8 ,2 ,10],
              [12,4 ,14,6 ],
              [3 ,11,1 ,9 ],
              [15,7 ,13,5 ]]
    h, w, _ = image.shape
    for row in range(h-1):
        for col in range(1, w-1, 1):
            oldpixel = image[row, col].copy()
            spread = 0.1
            row % 4
            pixel = oldpixel + spread*((1/16)*matrix[row%4][col%4]-0.5)
            newpixel = nearest(palette, pixel)
            image[row, col] = newpixel
    # Ensure pixel values are clipped to the valid range [0, 1]
    image = np.clip(image, 0, 1)
    return image

def main(image):
    # The number of colours: change to generate a dynamic palette
    nColours = 7

    orig = image.copy()

    # Convert the image from 8 bits per channel to floats in each channel for precision
    image = img_as_float(image)

    # Dynamically generate an N colour palette for the given image
    palette = findPalette(image, nColours)
    colours = palette.data
    colours = img_as_float([colours.astype(np.ubyte)])[0]

    # Call dithering function
    img = OrderedDitheringColor(image, palette)

    img = img_as_ubyte(img)

    # plt.show()
    # io.imsave('out.png', img)
    return img

if __name__ == "__main__":
    main()