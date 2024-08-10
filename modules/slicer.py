# import statements
import numpy as np
import math
from matplotlib import pyplot as plt
from skimage import io
import random

def main(imgA):
    
    # read image
    #imgA = io.imread("in.png", as_gray=False).astype(np.uint8)

    h, w, c = imgA.shape
    pad = random.randint(5,w/8)
    imgA = np.pad(imgA, ((pad, pad), (pad, pad), (0, 0)), mode='wrap')
    imgB = np.copy(imgA)
    h, w, c = imgB.shape

    slice_indices_a = random.randint(0,int(6*h/8))
    slice_indices_b = random.randint(slice_indices_a, h) 


    operator = random.randint(0,2)
    for i in np.arange(pad,h-pad,1):
        for j in np.arange(pad,w-pad,1):
            if slice_indices_a< i <slice_indices_b:
                if operator == 0:
                    imgB[i,j,0]=imgA[i,j+pad,0]
                else:
                    imgB[i,j,0]=imgA[i,j-pad,0]
                imgB[i,j,1]=imgA[i,j+pad,1]
                imgB[i,j,2]=imgA[i,j+pad,2]

    imgB = imgB[pad:h - pad, pad:w - pad]

    #io.imsave('out.png', imgB)
    return imgB

if __name__  == "__main__":
    main()