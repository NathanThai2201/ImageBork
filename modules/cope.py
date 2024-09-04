import numpy as np
from matplotlib import pyplot as plt
from scipy import spatial
from skimage import io, img_as_float, img_as_ubyte
from skimage.color import rgb2gray, gray2rgb
import os

global_palette = [ [0.69,0.137,0.22],
                    [0.941,0.424,0.624],
                     [0.929,0.325,0.369],
                     [0.831,0.408,0.459],
                     [0.71,0.42,0.541]]

def plotter(img):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def main(mode="in"):
    if mode =="in":
        thresholds = [0.0,0.1,0.16]
    else:
        thresholds = [0.8,0.9,0.96]
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
    index = 0

    """
    MAIN LOOP
    """
    while index < len(images):
        img_out = img_as_float(images[index][0])
        img_g = rgb2gray(images[index][0])

        # padding
        pad=32
        img_pad_g = np.pad(img_g, ((pad, pad), (pad, pad)), mode='reflect')
        img_pad = np.pad(images[index][0], ((pad, pad), (pad, pad), (0, 0)), mode='reflect')
        img_out_pad = np.pad(img_out, ((pad, pad), (pad, pad), (0, 0)), mode='reflect')

        h, w = img_pad_g.shape

        # blue glitch smallest squares
        for i in np.arange(pad,h-pad,4):
            for j in np.arange(pad,w-pad,6):
                # intentionally fuzzy, mean is only top left pixel
                mean = img_pad_g[i,j]
                if thresholds[1] < mean < thresholds[2]:
                    for a in np.arange(0,4,1):
                        for b in np.arange(0,6,1):
                            img_out_pad[i+a,j+b,0]=0
                            img_out_pad[i+a,j+b,1]=0
                            img_out_pad[i+a,j+b,2]=0
                        for a in np.arange(1,4,1):
                            for b in np.arange(1,6,1):
                                factor = (thresholds[2]-thresholds[1])/6
                                if thresholds[1]+1*factor < mean < thresholds[1]+2*factor:
                                    img_out_pad[i+a,j+b] = global_palette[4]
                                if thresholds[1]+2*factor < mean < thresholds[1]+3*factor:
                                    img_out_pad[i+a,j+b] = global_palette[3]
                                if thresholds[1]+3*factor < mean < thresholds[1]+4*factor:
                                    img_out_pad[i+a,j+b] = global_palette[2]
                                if thresholds[1]+4*factor < mean < thresholds[1]+5*factor:
                                    img_out_pad[i+a,j+b] = global_palette[1]
                                if thresholds[1]+5*factor < mean < thresholds[1]+6*factor:
                                    img_out_pad[i+a,j+b] = global_palette[0]
        #combine squares 1
        for i in np.arange(pad,h-pad,8):
            for j in np.arange(pad,w-pad,12):
                mean = img_pad_g[i,j]
                if thresholds[1] < mean < thresholds[2]:
                    # method: check top left of each cell to detect white
                    if np.all(img_out_pad[i,j] ==[0,0,0]) \
                    and np.all(img_out_pad[i+4,j+0] == [0,0,0]) \
                    and np.all(img_out_pad[i+0,j+6] == [0,0,0]) \
                    and np.all(img_out_pad[i+4,j+6] == [0,0,0]):
                        
                        for a in np.arange(0,8,1): # pure white
                            for b in np.arange(0,12,1):
                                img_out_pad[i+a,j+b,0]=0
                                img_out_pad[i+a,j+b,1]=0
                                img_out_pad[i+a,j+b,2]=0
                        for a in np.arange(1,8,1):
                            for b in np.arange(1,12,1):
                                factor = (thresholds[2]-thresholds[1])/6
                                if thresholds[1]+1*factor < mean < thresholds[1]+2*factor:
                                    img_out_pad[i+a,j+b] = global_palette[4]
                                if thresholds[1]+2*factor < mean < thresholds[1]+3*factor:
                                    img_out_pad[i+a,j+b] = global_palette[3]
                                if thresholds[1]+3*factor < mean < thresholds[1]+4*factor:
                                    img_out_pad[i+a,j+b] = global_palette[2]
                                if thresholds[1]+4*factor < mean < thresholds[1]+5*factor:
                                    img_out_pad[i+a,j+b] = global_palette[1]
                                if thresholds[1]+5*factor < mean < thresholds[1]+6*factor:
                                    img_out_pad[i+a,j+b] = global_palette[0]
        #combine squares 2
        for i in np.arange(pad,h-pad,16):
            for j in np.arange(pad,w-pad,24):
                mean = img_pad_g[i,j]
                if thresholds[1] < mean < thresholds[2]:
                    # method: check top left of each cell to detect white
                    if np.all(img_out_pad[i,j] == [0,0,0]) \
                    and np.all(img_out_pad[i+8,j+0] == [0,0,0]) \
                    and np.all(img_out_pad[i+0,j+12] == [0,0,0]) \
                    and np.all(img_out_pad[i+8,j+12] == [0,0,0]) \
                    and np.all(img_out_pad[i+8,j+23] == [0,0,0]) \
                    and np.all(img_out_pad[i+0,j+23] == [0,0,0]) \
                    and np.all(img_out_pad[i+15,j+0] == [0,0,0]) \
                    and np.all(img_out_pad[i+15,j+12] == [0,0,0]):
                        
                        for a in np.arange(0,16,1): # pure white
                            for b in np.arange(0,24,1):
                                img_out_pad[i+a,j+b,0]=0
                                img_out_pad[i+a,j+b,1]=0
                                img_out_pad[i+a,j+b,2]=0
                        for a in np.arange(1,16,1):
                            for b in np.arange(1,24,1):
                                factor = (thresholds[2]-thresholds[1])/6
                                if thresholds[1]+1*factor < mean < thresholds[1]+2*factor:
                                    img_out_pad[i+a,j+b] = global_palette[4]
                                if thresholds[1]+2*factor < mean < thresholds[1]+3*factor:
                                    img_out_pad[i+a,j+b] = global_palette[3]
                                if thresholds[1]+3*factor < mean < thresholds[1]+4*factor:
                                    img_out_pad[i+a,j+b] = global_palette[2]
                                if thresholds[1]+4*factor < mean < thresholds[1]+5*factor:
                                    img_out_pad[i+a,j+b] = global_palette[1]
                                if thresholds[1]+5*factor < mean < thresholds[1]+6*factor:
                                    img_out_pad[i+a,j+b] = global_palette[0]
        #combine squares 3
        for i in np.arange(pad,h-pad,32):
            for j in np.arange(pad,w-pad,48):
                mean = img_pad_g[i,j]
                if thresholds[1] < mean < thresholds[2]:
                    # method: check top left of each cell to detect white
                    if np.all(img_out_pad[i,j] == [0,0,0]) \
                    and np.all(img_out_pad[i+16,j+0] == [0,0,0]) \
                    and np.all(img_out_pad[i+0,j+24] == [0,0,0]) \
                    and np.all(img_out_pad[i+16,j+24] == [0,0,0]) \
                    and np.all(img_out_pad[i+16,j+47] == [0,0,0]) \
                    and np.all(img_out_pad[i+0,j+47] == [0,0,0]) \
                    and np.all(img_out_pad[i+31,j+0] == [0,0,0]) \
                    and np.all(img_out_pad[i+31,j+24] == [0,0,0]):
                        
                        for a in np.arange(0,32,1): # pure black
                            for b in np.arange(0,48,1):
                                img_out_pad[i+a,j+b,0]=0
                                img_out_pad[i+a,j+b,1]=0
                                img_out_pad[i+a,j+b,2]=0
                        for a in np.arange(1,32,1):
                            for b in np.arange(1,48,1):
                                factor = (thresholds[2]-thresholds[1])/6
                                if thresholds[1]+1*factor < mean < thresholds[1]+2*factor:
                                    img_out_pad[i+a,j+b] = global_palette[4]
                                if thresholds[1]+2*factor < mean < thresholds[1]+3*factor:
                                    img_out_pad[i+a,j+b] = global_palette[3]
                                if thresholds[1]+3*factor < mean < thresholds[1]+4*factor:
                                    img_out_pad[i+a,j+b] = global_palette[2]
                                if thresholds[1]+4*factor < mean < thresholds[1]+5*factor:
                                    img_out_pad[i+a,j+b] = global_palette[1]
                                if thresholds[1]+5*factor < mean < thresholds[1]+6*factor:
                                    img_out_pad[i+a,j+b] = global_palette[0]
        # pure white and red squares
        for i in np.arange(pad,h-pad,8):
            for j in np.arange(pad,w-pad,8):
                # intentionally fuzzy, mean is only top left pixel
                mean = img_pad_g[i,j]
                if mean < thresholds[1]: # pure white
                    for a in np.arange(0,8,1):
                        for b in np.arange(0,8,1):
                            img_out_pad[i+a,j+b,0]=0
                            img_out_pad[i+a,j+b,1]=0
                            img_out_pad[i+a,j+b,2]=0
                if mean < thresholds[0]: # red square
                    for a in np.arange(1,7,1):
                        for b in np.arange(1,7,1):
                            img_out_pad[i+a,j+b,0]=1

        # clip             
        img_f = np.clip(img_out_pad, 0, 1)
        # unpad
        img_f = img_f[pad:h - pad, pad:w - pad]
        h, w, _ = img_f.shape
        # convert
        img_f = img_as_ubyte(img_f)


        if mode =="in":
            thresholds = [x + 0.01 for x in thresholds]
        else:
            thresholds = [x - 0.01 for x in thresholds]
        img_path = os.path.join(folder_path, str(index))
        io.imsave(img_path+".png", img_f)
        index+=1


if __name__ == "__main__":
    main()
