# import statements
import numpy as np
import math
from matplotlib import pyplot as plt
from skimage import io

# input: images from folder A, naming convention is 0001.png to xxxx.png
def main(imgA):
    
    amount=3
    # read image
    # imgA = io.imread("in.png", as_gray=False).astype(np.uint8)
    h, w = imgA[:,:,0].shape
    for i in np.arange(0,h,1):
        for j in np.arange(1,w,1):
            if j<w-3:
                imgA[i,j,0]=imgA[i,j+amount,0]
            if j>3:
                imgA[i,j,2]=imgA[i,j-amount,1]

    # io.imsave('out.png', imgA)
    return imgA

if __name__  == "__main__":
    main()