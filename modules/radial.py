import numpy as np
import random
from skimage import io, transform, img_as_ubyte
import os
import matplotlib.pyplot as plt


def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def main(img):
    # Load target image
    #img = io.imread('b.png').astype(np.uint8)
    img = img[:, :, :3]  # Ensure image has 3 color channels (RGB)
    h, w, _ = img.shape  # Unpack height, width, and channels

    # get a list of scales and rates (set from 3/4 half of the image to outer)
    # plotter(img,"a")
    resolution = 100
    scales = []
    rate = []
    division_factor = 1/(resolution*4)
    for i in range(resolution):
        temp = 0.75+(i+1)*division_factor
        scales.append(temp)
        rate.append(-temp)
    # print(scales)
    # create scaled images
    images = []
    for i in range(resolution):
        # Calculate new dimensions
        new_width = int(w * scales[i])
        new_height = int(h * scales[i])
        # Scale the image
        img2 = transform.resize(img, (new_height, new_width), anti_aliasing=True)
        # Pad image back to original dimensions
        pad_h = (h-new_height)//2
        pad_h2 = h-pad_h-new_height
        pad_w = (w-new_width)//2
        pad_w2 = w-pad_w-new_width
        img2 = np.pad(img2, ((pad_h, pad_h2), (pad_w, pad_w2), (0, 0)), mode='edge')
        # Convert the scaled images to uint8
        img2 = img_as_ubyte(img2)
        images.append(img2)
    
    # combine images to radial blur
    for i in np.arange(0, h, 1):
        for j in np.arange(0, w, 1):
            # get r value
            amounts_r = []
            amounts_g = []
            amounts_b = []
            for a in range(resolution):
                amounts_r.append(int(images[a][i,j,0]))
                amounts_g.append(int(images[a][i,j,1]))
                amounts_b.append(int(images[a][i,j,2]))
            img[i,j,0] = np.average(amounts_r,weights=rate)
            img[i,j,1] = np.average(amounts_g,weights=rate)
            img[i,j,2] = np.average(amounts_b,weights=rate)

    # plotter(img,"a")
    # Save the scaled image
    # io.imsave("out.png", img)
    return img

if __name__ == "__main__":
    main()
