import numpy as np
from matplotlib import pyplot as plt
from skimage import io
from skimage.color import rgb2hsv, hsv2rgb

#works in jpeg, 3 channels
#best is done in 400* 400 resolution.

def kuwahara(img, pad):
    # Padding each channel separately
    img_pad = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode='reflect')
    img_f = np.zeros_like(img_pad)
    h, w, c = img_pad.shape
    
    for i in np.arange(pad, h - pad, 1):
        for j in np.arange(pad, w - pad, 1):
            meanindex = 0
            for channel in range(2, -1, -1):
                sect1=[img_pad[i+1,j+1,channel],img_pad[i+2,j+2,channel],img_pad[i+3,j+3,channel],img_pad[i+1,j+2,channel],img_pad[i+2,j+1,channel],img_pad[i+1,j+3,channel],img_pad[i+2,j+3,channel],img_pad[i+3,j+1,channel],img_pad[i+3,j+2,channel]]
                sect2=[img_pad[i-1,j-1,channel],img_pad[i-2,j-2,channel],img_pad[i-3,j-3,channel],img_pad[i-1,j-2,channel],img_pad[i-2,j-1,channel],img_pad[i-1,j-3,channel],img_pad[i-2,j-3,channel],img_pad[i-3,j-1,channel],img_pad[i-3,j-2,channel]]
                sect3=[img_pad[i-1,j+1,channel],img_pad[i-2,j+2,channel],img_pad[i-3,j+3,channel],img_pad[i-1,j+2,channel],img_pad[i-2,j+1,channel],img_pad[i-1,j+3,channel],img_pad[i-2,j+3,channel],img_pad[i-3,j+1,channel],img_pad[i-3,j+2,channel]]
                sect4=[img_pad[i+1,j-1,channel],img_pad[i+2,j-2,channel],img_pad[i+3,j-3,channel],img_pad[i+1,j-2,channel],img_pad[i+2,j-1,channel],img_pad[i+1,j-3,channel],img_pad[i+2,j-3,channel],img_pad[i+3,j-1,channel],img_pad[i+3,j-2,channel]]
                # if brightness V value, store value of a as the mean index
                if channel == 2:
                    sect1std = np.std(sect1)
                    sect2std = np.std(sect2)
                    sect3std = np.std(sect3)
                    sect4std = np.std(sect4)
                    a = np.argmin([sect1std,sect2std,sect3std,sect4std])
                    meanindex = a
                means = [np.mean(sect1),np.mean(sect2),np.mean(sect3),np.mean(sect4)]
                img_f[i,j,channel]=means[meanindex]
    
    # Crop
    img_f = img_f[pad:h - pad, pad:w - pad]
    img_f2 = hsv2rgb(img_f)
    # plotter(img_f2,"erm")
    # print(img_f2)
    return img_f2
def plotter(img,name):
    fig = plt.figure()
    gs = plt.GridSpec(1, 2) #height, width
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_axis_off()
    ax1.imshow(img, cmap=plt.cm.gray)
    ax1.set_title(name)
    plt.show()

def main(img):
    # A = 'in.png'
    # # Read image
    # img = io.imread(A).astype(np.uint8)
    # # Strip the alpha channel if it exists
    # img = img[:, :, :3]
    h, w, _ = img.shape
    pad = 3
    # plotter(img,"erm")
    hsv_img = rgb2hsv(img)
    img2 = kuwahara(hsv_img, pad)
    img2 = (img2 * 255).astype(np.uint8)

    # io.imsave('out.png', img2)
    return img2

if __name__ == "__main__":
    main()
