import numpy as np
import random
from skimage import io, transform, img_as_ubyte
import os
import matplotlib.pyplot as plt


def scaling(img, h_scale=1.1, w_scale=1.1):
    # Load target image
    # img = io.imread('in.png').astype(np.uint8)
    img = img[:, :, :3]  # Ensure image has 3 color channels (RGB)

    h, w, _ = img.shape  # Unpack height, width, and channels

    # Calculate new dimensions
    new_width = int(w * w_scale)
    new_height = int(h * h_scale)

    # Scale the image
    img2 = transform.resize(img, (new_height, new_width), anti_aliasing=True)

    # Convert the scaled images to uint8
    img2 = img_as_ubyte(img2)

    # Save the scaled image
    #io.imsave("out.png", img2)
    return img2

def flipping(img, direction="lr"):
    # Load target image
    #img = io.imread('in.png').astype(np.uint8)
    img = img[:, :, :3]
    
    if direction == "lr":
        img2 = np.fliplr(img)
    else:
        img2 = np.flipud(img)
    
    img2=img_as_ubyte(img2)
    # io.imsave("out.png",img2)
    return img2

def rotation(img,angle=90):
    # Load target image
    # img = io.imread('in.png').astype(np.uint8)
    img = img[:, :, :3]
    
    img2 = transform.rotate(img, -angle, resize=True)
    img2=img_as_ubyte(img2)
    # io.imsave("out.png",img2)
    return img2

if __name__ == "__main__":
    scaling()
