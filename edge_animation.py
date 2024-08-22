import numpy as np
import os
from scipy import signal
from skimage.color import rgb2gray, gray2rgb
from skimage import io, img_as_ubyte

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def main(mode="NO"):
    folder_path = "./input"
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(folder_path, filename)
            image = io.imread(img_path).astype(np.uint8)
            # Strip the alpha channel if it exists
            if image.ndim == 4:
                image = image[:, :, :3]
            images.append([image, int(filename.rsplit('.', 1)[0])])
    # Sort images based on their numeric names
    images.sort(key=lambda x: x[1])
    
    images2 = []
    output_folder = "./output"
    os.makedirs(output_folder, exist_ok=True)

    # Sobel pass 1: edges
    index = 0
    while index < len(images):
        imgA = np.copy(images[index][0])

        img_gray = rgb2gray(imgA)
        img_byte = img_as_ubyte(img_gray)

        sobel_h = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_v = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        img_sh = signal.convolve2d(img_byte, sobel_h, mode='same')
        img_sv = signal.convolve2d(img_byte, sobel_v, mode='same')

        imgD = -np.clip(img_sh + img_sv, -255, 0) + np.clip(img_sh + img_sv, 0, 255)

        images2.append(imgD)
        index += 1
    
    # Sobel pass 2: overlay and mix
    index = 2 
    while index < len(images):
        imgA = np.copy(images2[index-2])
        imgB = np.copy(images2[index-1])
        imgC = np.copy(images2[index])
        imgbase = np.copy(images[index][0])
        h, w = imgA.shape
        imgD = np.zeros_like(imgA)

        for i in np.arange(0, h, 1):
            for j in np.arange(0, w, 1):
                imgD[i, j] = imgC[i, j] + imgB[i, j] * 0.6 + imgA[i, j] * 0.3

        imgD = np.clip(imgD, 0, 255)
        imgD = img_as_ubyte(imgD)
        imgD = gray2rgb(imgD)

        imgE = np.zeros_like(imgbase)
        # mix red only
        for i in np.arange(0, h, 1):
            for j in np.arange(0, w, 1):
                imgE[i,j,0] = np.min([int(imgbase[i,j,0]) + int(imgD[i,j,0]), 255])
                imgE[i,j,1] = imgbase[i,j,1]
                imgE[i,j,2] = imgbase[i,j,2]
        img_path = os.path.join(output_folder, f"{index-2}")
        io.imsave(img_path + ".png", imgE)
        index += 1

if __name__ == "__main__":
    main()
