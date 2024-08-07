import numpy as np
from matplotlib import pyplot as plt
from skimage import io, filters


def apply_gaussian_filter(image, sigma):
    # Separate the color channels
    red_channel = image[:, :, 0]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 2]

    # Apply Gaussian filter to each channel
    red_filtered = filters.gaussian(red_channel, sigma=sigma)
    green_filtered = filters.gaussian(green_channel, sigma=sigma)
    blue_filtered = filters.gaussian(blue_channel, sigma=sigma)

    # Combine the filtered channels back into a color image
    filtered_image = np.stack((red_filtered, green_filtered, blue_filtered), axis=-1)
    
    return filtered_image

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
    # plotter(img,"erm")
    sigma = 2
    img2 = apply_gaussian_filter(img,sigma)
    img2 = (img2 * 255).astype(np.uint8)
    # io.imsave('out.png', img2)
    return img2

if __name__ == "__main__":
    main()
