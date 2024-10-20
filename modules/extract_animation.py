# import statements
import numpy as np
import math
import os
from matplotlib import pyplot as plt
from skimage import io, filters


def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

# input: images from folder A, naming convention is 0001.png to xxxx.png
def main(mode = 1):
    folder_path = "./input"
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(folder_path, filename)
            image = io.imread(img_path).astype(np.uint8)
            # Strip the alpha channel if it exists
            image = image[:, :, :3]
            images.append([image,int(filename.rsplit('.', 1)[0])])   
    # sort
    images.sort(key=lambda x: x[1])

    folder_path = "./output"
    index = mode

    while index < len(images):
        # read image
        #print(fade)
        imgA = np.copy(images[index][0])
        imgB = np.copy(images[index-mode][0])
        imgBase = np.zeros_like(imgB)
        h, w = imgBase[:,:,0].shape
        for i in np.arange(0,h,1):
            for j in np.arange(0,w,1):
                imgBase[i,j,0]= 0.5*imgA[i,j,0]+0.5*(255-imgB[i,j,0])
                imgBase[i,j,1]= 0.5*imgA[i,j,1]+0.5*(255-imgB[i,j,1])
                imgBase[i,j,2]= 0.5*imgA[i,j,2]+0.5*(255-imgB[i,j,2])

        imgD = imgBase.astype(np.uint8)
        img_path = os.path.join(folder_path, str(index))
        io.imsave(img_path+".png", imgD)
        index+=1

if __name__  == "__main__":
    main()

