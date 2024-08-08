import os
from sklearn.cluster import KMeans
from scipy import spatial
from skimage import io, color, img_as_float, img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt

global_palettes = [
    [[1.92868298e-02, 9.38096478e-04, 5.84233472e-02],
    [3.55221890e-01, 4.32460307e-01, 8.15861964e-01],
    [8.06076926e-01, 7.21792226e-01, 9.80064284e-01],
    [7.84039603e-01, 3.65803449e-01, 3.51357714e-01]],
    [[0.14388763, 0.32808635, 0.37764329],
    [0.67966629, 0.93308258, 0.58057315],
    [0.26582014, 0.59533748, 0.59182315],
    [0.02731523, 0.11132541, 0.15976621],
    [0.95902267, 0.99872472, 0.49496017],
    [0.4302319,  0.83550905, 0.58056938],
    [0.33467006, 0.73453243, 0.57967572]],
    [[0.20463289, 0.47111839, 0.30328485],
    [0.90659858, 0.49070261, 0.23089869],
    [0.97184836, 0.82279412, 0.63890132],
    [0.26408769, 0.59139978, 0.83654684],
    [0.3658415 , 0.08273693, 0.36780501],
    [0.73207321, 0.99141624, 0.32781863],
    [0.67616954, 0.33441496, 0.24873988],
    [0.40573802, 0.73160131, 0.29415033],
    [0.59775871, 0.6375    , 0.68509804],
    [0.25167756, 0.288878  , 0.41681645],
    [0.41162884, 0.88451087, 0.64724265],
    [0.10592865, 0.08715959, 0.17053649],
    [0.9889951 , 0.93554466, 0.90212691],
    [0.36977035, 0.4368393 , 0.52432065],
    [0.47726852, 0.17040577, 0.09812364],
    [0.93358115, 0.4828622 , 0.46875   ],
    [0.95900202, 0.72963555, 0.25331682],
    [0.98162854, 0.90906863, 0.4664488 ],
    [0.1444281 , 0.30137255, 0.51986111],
    [0.7875    , 0.22321771, 0.1869805 ]]
]
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

    print(f'colours:\n{colours}')
    #plt.figure(figsize=(10, 5))
    # plt.imshow(colours_img)
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

def main(image,cset=-1):
    # The number of colours: change to generate a dynamic palette
    nColours = 20

    # Convert the image from 8 bits per channel to floats in each channel for precision
    image = img_as_float(image)

    # Dynamically generate an N colour palette for the given image
    if cset==-1:
        palette = findPalette(image, nColours)
    # SELECT COLOR PALETTES
    if cset==0: # 1 bit error 4
        palette = makePalette(global_palettes[0])
    if cset==1: #deep maze 7
        palette = makePalette(global_palettes[1])
    if cset==2: #vibe 20
        palette = makePalette(global_palettes[2])
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
