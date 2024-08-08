import os
from sklearn.cluster import KMeans
from scipy import spatial
from skimage import io, color, img_as_float, img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt

global_palettes = [
    [[0.17464145, 0.14643086, 0.23291974],
    [0.6904149,  0.69036573, 0.6903731 ]],
    [[1.92868298e-02, 9.38096478e-04, 5.84233472e-02],
    [8.06076926e-01, 7.21792226e-01, 9.80064284e-01],
    [3.55221890e-01, 4.32460307e-01, 8.15861964e-01],
    [7.84039603e-01, 3.65803449e-01, 3.51357714e-01]],
    [[0.99959041, 0.99959477, 0.99955701],
    [0.55222725, 0.58357969, 0.44346764],
    [0.30651727, 0.32467859, 0.24456654],
    [0.19033398, 0.19956762, 0.16431803],
    [0.12160319, 0.12160168, 0.12152956]],
    [[0.95902267, 0.99872472, 0.49496017],
    [0.67966629, 0.93308258, 0.58057315],
    [0.4302319,  0.83550905, 0.58056938],
    [0.33467006, 0.73453243, 0.57967572],
    [0.26582014, 0.59533748, 0.59182315],
    [0.14388763, 0.32808635, 0.37764329],
    [0.02731523, 0.11132541, 0.15976621]],
    [[0.10592865, 0.08715959, 0.17053649],
    [0.3658415 , 0.08273693, 0.36780501],
    [0.8875   ,  0.12321771, 0.1869805 ],
    [0.93358115, 0.4828622 , 0.46875   ],
    [0.97184836, 0.82279412, 0.63890132],
    [0.9889951 , 0.93554466, 0.90212691],
    [0.98162854, 0.90906863, 0.4664488 ],
    [0.95900202, 0.72963555, 0.25331682],
    [0.90659858, 0.49070261, 0.23089869],
    [0.67616954, 0.33441496, 0.24873988],
    [0.47726852, 0.17040577, 0.09812364],
    [0.25167756, 0.288878  , 0.41681645],
    [0.36977035, 0.4368393 , 0.52432065],
    [0.59775871, 0.6375    , 0.68509804],
    [0.41162884, 0.88451087, 0.64724265],
    [0.26408769, 0.59139978, 0.83654684],
    [0.1444281 , 0.30137255, 0.51986111],
    [0.20463289, 0.47111839, 0.30328485],
    [0.40573802, 0.73160131, 0.29415033],
    [0.73207321, 0.99141624, 0.32781863]],
    [[0.18108102, 0.16530406, 0.20468679],
    [0.26210463, 0.24025143, 0.22201666],
    [0.37674253, 0.33879589, 0.3273477 ],
    [0.5712874 , 0.37580337, 0.27244277],
    [0.63892503, 0.51200019, 0.30174784],
    [0.23611979, 0.25776399, 0.3748606 ],
    [0.44081463, 0.46558485, 0.46603957],
    [0.59973698, 0.61541582, 0.62573167],
    [0.75417456, 0.72325376, 0.66886447],
    [0.85267461, 0.85904114, 0.74239662]],
    [[0.98011248, 0.88255054, 0.96353853],
    [0.93359477, 0.79432099, 0.9130167 ],
    [0.92969594, 0.76443308, 0.88948849],
    [0.93262745, 0.59285984, 0.95859695],
    [0.91693663, 0.45698494, 0.97226485],
    [0.93655483, 0.51783878, 0.78315759],
    [0.9247785 , 0.34741031 ,0.64534786],
    [0.99731742, 0.99959932, 0.77273657],
    [0.97185185, 0.82279158, 0.57921859],
    [0.93849984, 0.53897603, 0.46334578],
    [0.83649858, 0.99435193 ,0.90761199],
    [0.59931185, 0.86202389, 0.82318984],
    [0.48021577, 0.7178793 , 0.74986918],
    [0.73208925, 0.90707535, 0.98997521],
    [0.61834965, 0.76293618, 0.98008349],
    [0.55760198, 0.54923898, 0.92565547],
    [0.60165577, 0.34172339, 0.92770791],
    [0.43947732, 0.312579  , 0.65661875],
    [0.38102622, 0.1088964 , 0.49524153],
    [0.2628932 , 0.14084484, 0.31875141]]
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

    #plt.figure(figsize=(10, 5))
    # plt.imshow(colours_img)
    # plt.imshow(colours_img)
    return makePalette(colours)

def ModifiedFloydSteinbergDitherColor(image, palette):
    h, w, _ = image.shape
    for row in range(h-1):
        for col in range(1, w-1, 1):
            oldpixel = image[row, col].copy()
            newpixel = nearest(palette, oldpixel)
            image[row, col] = newpixel
            quant_error = oldpixel - newpixel

            image[row, col+1] += quant_error * 11 / 26
            image[row+1, col-1] += quant_error * 5 / 26
            image[row+1, col] += quant_error * 7 / 26
            image[row+1, col+1] += quant_error * 3 / 26

    # Ensure pixel values are clipped to the valid range [0, 1]
    image = np.clip(image, 0, 1)
    return image

def main(image,cset=-1):
    # The number of colours: change to generate a dynamic palette
    nColours = 7
    # Convert the image from 8 bits per channel to floats in each channel for precision
    image = img_as_float(image)

    # Dynamically generate an N colour palette for the given image
    if cset==-1:
        palette = findPalette(image, nColours)
    # SELECT COLOR PALETTES
    if cset==0: 
        palette = makePalette(global_palettes[0])
    if cset==1: 
        palette = makePalette(global_palettes[1])
    if cset==2: 
        palette = makePalette(global_palettes[2])
    if cset==3: 
        palette = makePalette(global_palettes[3])
    if cset==4: 
        palette = makePalette(global_palettes[4])
    if cset==5: 
        palette = makePalette(global_palettes[5])
    if cset==6: 
        palette = makePalette(global_palettes[6])
    colours = palette.data
    colours = img_as_float([colours.astype(np.ubyte)])[0]

    # Call dithering function
    img = ModifiedFloydSteinbergDitherColor(image, palette)

    img = img_as_ubyte(img)

    # plt.show()
    # io.imsave('out.png', img)
    return img

if __name__ == "__main__":
    main()
    main()