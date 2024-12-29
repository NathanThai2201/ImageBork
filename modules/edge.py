
import numpy as np 
from skimage import io, img_as_ubyte
from scipy import signal, spatial
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import random

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def main(imgA,channel):
    
    # read image
    # imgA = io.imread("in.png", as_gray=False).astype(np.uint8)
    imgA = imgA[:, :, :3]

    img = img_as_ubyte(rgb2gray(imgA)).astype(int)

    sobel_h = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    sobel_v = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    img_sh = signal.convolve2d(img, sobel_h, mode='same')
    img_sv = signal.convolve2d(img, sobel_v, mode='same')
    # we combine both the negative and positive values of the combines sobel filter for the final image
    img_gm = -np.clip(img_sh+img_sv,-255,0)+np.clip(img_sh+img_sv,0,255)

    strength = random.randint(50,100)*0.01

    h, w = img.shape
    for i in np.arange(0,h,1):
        for j in np.arange(0,w,1):
            if channel =="r":
                imgA[i,j,0]= np.min([imgA[i,j,0]+img_gm[i,j]*strength,255])
            elif channel =="g":
                imgA[i,j,1]= np.min([imgA[i,j,1]+img_gm[i,j]*strength,255])
            elif channel =="b":
                imgA[i,j,2]= np.min([imgA[i,j,2]+img_gm[i,j]*strength,255])
            elif channel =="a":
                imgA[i,j,0]= np.min([imgA[i,j,0]+img_gm[i,j]*strength,255])
                imgA[i,j,1]= np.min([imgA[i,j,1]+img_gm[i,j]*strength,255])
                imgA[i,j,2]= np.min([imgA[i,j,2]+img_gm[i,j]*strength,255])
            else:
                imgA[i,j,0]= np.max([imgA[i,j,0]-img_gm[i,j]*strength,0])
                imgA[i,j,1]= np.max([imgA[i,j,1]-img_gm[i,j]*strength,0])
                imgA[i,j,2]= np.max([imgA[i,j,2]-img_gm[i,j]*strength,0])
    return imgA

if __name__ == '__main__':
    main()




