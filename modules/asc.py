import numpy as np
from matplotlib import pyplot as plt
from skimage import io
from skimage.color import rgb2gray, gray2rgb

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def main(img):
    A = 'in.png'
    # Read image
    img = rgb2gray(img)

    chars=" .:coᛟᛝឱஇ▓█"
    pad=8
    img_pad = np.pad(img, ((pad, pad), (pad, pad)), mode='reflect')
    h, w = img_pad.shape
    img_out = np.zeros_like(img_pad)
    for i in np.arange(pad,h-pad,8):
        for j in np.arange(pad,w-pad,8):
            mean = int(np.mean([img_pad[i,j],img_pad[i+1,j+1],img_pad[i+1,j+1],img_pad[i+1,j+2],img_pad[i+2,j+1],img_pad[i+2,j+2]])*10)
            if mean == 1: # .
                img_out[i+6,j+4]=255
            if mean == 2: # :
                img_out[i+6,j+4]=255
                img_out[i+5,j+4]=255
                img_out[i+3,j+4]=255
            if mean == 3 or mean == 4: # c o
                img_out[i+6,j+3]=255
                img_out[i+6,j+4]=255
                img_out[i+5,j+5]=255
                img_out[i+3,j+5]=255
                img_out[i+2,j+4]=255
                img_out[i+2,j+3]=255
                img_out[i+5,j+2]=255
                img_out[i+4,j+2]=255
                img_out[i+3,j+2]=255
                if mean == 4:
                    img_out[i+4,j+5]=255
            if mean == 5: # P
                img_out[i+1,j+2]=255
                img_out[i+1,j+3]=255
                img_out[i+1,j+4]=255
                img_out[i+2,j+2]=255
                img_out[i+2,j+5]=255
                img_out[i+3,j+2]=255
                img_out[i+3,j+5]=255
                img_out[i+4,j+2]=255
                img_out[i+4,j+3]=255
                img_out[i+4,j+4]=255
                img_out[i+5,j+2]=255
                img_out[i+6,j+2]=255
            # if mean == 6: #B
            #     img_out[i+1,j+2]=255
            #     img_out[i+1,j+3]=255
            #     img_out[i+2,j+2]=255
            #     img_out[i+2,j+4]=255
            #     img_out[i+3,j+2]=255
            #     img_out[i+3,j+3]=255
            #     img_out[i+3,j+4]=255
            #     img_out[i+4,j+2]=255
            #     img_out[i+4,j+5]=255
            #     img_out[i+5,j+2]=255
            #     img_out[i+5,j+5]=255
            #     img_out[i+6,j+2]=255
            #     img_out[i+6,j+3]=255
            #     img_out[i+6,j+4]=255
            if mean == 6: # O
                img_out[i+1,j+3]=255
                img_out[i+1,j+4]=255
                img_out[i+2,j+2]=255
                img_out[i+2,j+5]=255
                img_out[i+3,j+2]=255
                img_out[i+3,j+5]=255
                img_out[i+4,j+2]=255
                img_out[i+4,j+5]=255
                img_out[i+5,j+2]=255
                img_out[i+5,j+5]=255
                img_out[i+6,j+3]=255
                img_out[i+6,j+4]=255
            if mean == 7: # ?
                img_out[i+1,j+4]=255 
                img_out[i+1,j+5]=255
                img_out[i+2,j+3]=255
                img_out[i+2,j+6]=255
                img_out[i+3,j+5]=255
                img_out[i+3,j+6]=255
                img_out[i+4,j+4]=255
                img_out[i+6,j+4]=255
            if mean == 8: # @
                img_out[i+1,j+3]=255
                img_out[i+1,j+4]=255
                img_out[i+1,j+5]=255
                img_out[i+2,j+2]=255
                img_out[i+2,j+6]=255               
                img_out[i+3,j+2]=255
                img_out[i+3,j+4]=255
                img_out[i+3,j+5]=255
                img_out[i+3,j+6]=255               
                img_out[i+4,j+2]=255
                img_out[i+4,j+5]=255
                img_out[i+5,j+3]=255
                img_out[i+6,j+4]=255
                img_out[i+6,j+5]=255
                img_out[i+6,j+6]=255
            if mean == 9: # █
                for a in np.arange(1,7,1):
                    for b in np.arange(1,7,1):
                        img_out[i+a,j+b]=255
 
    strings = []
    for i in np.arange(pad,h-pad,8):
        string= []
        for j in np.arange(pad,w-pad,4):
            mean = int(np.mean([img_pad[i,j],img_pad[i+1,j+1],img_pad[i+1,j+1]])*10)
            string.append(chars[mean])
        strings.append("".join(string))
    # for i in strings:
    #     print(i)
    with open('./ascii.txt', 'w') as file:
        for string in strings:
            file.write(string + '\n')

    img_f = img_out[pad:h - pad, pad:w - pad]
    h, w = img_f.shape
    # plotter(img_f,"A")

    #convert to rgb
    img_f = gray2rgb(img_f)
    img_f = (img_f * 255).astype(np.uint8)
    for i in np.arange(0,h,1):
        for j in np.arange(0,w,1):
            img_f[i,j,0]=img_f[i,j,0]*255
            img_f[i,j,1]=img_f[i,j,1]*255
            img_f[i,j,2]=img_f[i,j,2]*255
    # plotter(img_f,"A")
    return img_f
if __name__ == "__main__":
    main()
