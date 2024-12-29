
"""
Code refactored from jpglitch by Kareeeeem 
Repository at https://github.com/Kareeeeem/jpglitch.git
Made to work with ImageBork effect chaining
All rights reserved
"""

import io
import os
import random
import numpy as np
from skimage import io as skio, img_as_ubyte
from skimage.io import imsave, imread
import matplotlib.pyplot as plt

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()


def main(img):
    return img

if __name__ == '__main__':
    main()
