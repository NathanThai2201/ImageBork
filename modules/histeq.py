from skimage import io, color
import matplotlib.pyplot as plt
import numpy as np

def plotter(img, name):
    fig = plt.figure()
    gs = plt.GridSpec(1, 2)  # height, width
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_axis_off()
    ax1.imshow(img)
    ax1.set_title(name)
    plt.show()

def histogram_equalization(channel):
    h, w = channel.shape
    hist = np.zeros(256, dtype=int)

    for i in np.arange(0, h, 1):
        for j in np.arange(0, w, 1):
            hist[int(channel[i, j] * 255)] += 1

    # Cumulative histogram computation
    H = np.zeros(256, dtype=int)
    H[0] = hist[0]
    for n in np.arange(1, 256, 1):
        H[n] = H[n - 1] + hist[n]

    # Histogram equalization
    J = np.zeros((h, w))
    for i in np.arange(0, h, 1):
        for j in np.arange(0, w, 1):
            ind = int(channel[i, j] * 255)
            J[i, j] = np.floor((255.0 / (h * w)) * H[ind] + 0.5) / 255.0

    return J

def main(I):
    # Read image
    # I = io.imread("in.png").astype(np.uint8)
    I = I[:, :, :3]


    I_hsv = color.rgb2hsv(I)

    V_eq = histogram_equalization(I_hsv[:, :, 2])
    I_hsv[:, :, 2] = V_eq

    I_eq = color.hsv2rgb(I_hsv)

    # rescale
    I_eq = (I_eq * 255).astype(np.uint8)

    # plotter(I, "original")
    # plotter(I_eq, "Equalized Image")
    # io.imsave('out.png', I_eq)
    return I_eq

if __name__ == "__main__":
    main()
