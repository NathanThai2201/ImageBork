# import statements
import numpy as np
import math
from matplotlib import pyplot as plt
from skimage import io, filters

# input: images from folder A, naming convention is 0001.png to xxxx.png
def part1():
    index = 2
    while index < 3:

        A = './A/'+'{:04d}'.format(index-1)+'.png'
        B = './A/'+'{:04d}'.format(index)+'.png'
        C = './A/'+'{:04d}'.format(index+1)+'.png'
        if A[2] == 4:  # Remove alpha channel if it exists
            A = A[:, :, :3]
            B = B[:, :, :3]
            C = C[:, :, :3]
        # read image
        imgA = io.imread(A, as_gray=False).astype(np.uint8)
        imgB = io.imread(B, as_gray=False).astype(np.uint8)
        imgBase = np.copy(imgB)
        imgC = io.imread(C, as_gray=False).astype(np.uint8)
        h, w = imgA[:,:,0].shape
        for i in np.arange(0,h,1):
            for j in np.arange(1,w,1):
                imgA[i,j,0]=0
                imgA[i,j,1]=0
                imgB[i,j,0]=0
                imgB[i,j,2]=0
                imgC[i,j,1]=0
                imgC[i,j,2]=0

        imgD = np.zeros_like(imgA)
        for i in np.arange(0,h,1):
            for j in np.arange(1,w,1):
                imgD[i,j,2]=imgA[i,j,2]
                imgD[i,j,1]=imgB[i,j,1]
                imgD[i,j,0]=imgC[i,j,0]
                imgD[i,j,2]=imgD[i,j,2]/2+imgBase[i,j,2]/2
                imgD[i,j,1]=imgD[i,j,1]/2+imgBase[i,j,2]/2
                imgD[i,j,0]=imgD[i,j,0]/2+imgBase[i,j,2]/2
        imgD = imgD.astype(np.uint8)
        io.imsave('./B/'+'{:04d}'.format(index)+'.png', imgD)
        index+=1
if __name__  == "__main__":
    part1()