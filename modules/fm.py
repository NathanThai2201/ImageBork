import numpy as np
from matplotlib import pyplot as plt
from skimage import io, color
from skimage.util import img_as_ubyte, img_as_float


class LowpassFilter:
    def __init__(self, rate, hz):
        self.alpha = 0.0
        self.prev = 0.0
        self.set_filter(rate, hz)

    def set_filter(self, rate, hz):
        time_interval = 1.0 / rate
        tau = 1.0 / (hz * 2 * np.pi)
        self.alpha = time_interval / (tau + time_interval)

    def reset_filter(self, val=0):
        self.prev = val

    def lowpass(self, sample):
        stage1 = sample * self.alpha
        stage2 = self.prev - (self.prev * self.alpha)
        self.prev = (stage1 + stage2)
        return self.prev

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def process_image(img, omega, phase_mult, quantval=30, lowpass_cutoffs=(0.25, 0.1, 0.05), negate=False):
    if img.shape[2] == 4:
        img_rgb = img[:, :, :3]  # Exclude alpha channel
    else:
        img_rgb = img
    
    img_gray = color.rgb2gray(img_rgb)
    img_gray = img_as_float(img_gray)

    # Prepare filters
    rate = 100000.0
    lpf1 = LowpassFilter(rate, lowpass_cutoffs[0] * rate)
    lpf2 = LowpassFilter(rate, lowpass_cutoffs[1] * rate)
    lpf3 = LowpassFilter(rate, lowpass_cutoffs[2] * rate)

    # Initialize result
    result_img = np.zeros_like(img_gray)

    min_phase = -phase_mult * omega
    max_phase = phase_mult * omega

    for y in range(img.shape[0]):
        sig_int = 0  # integral of the signal
        pre_m = 0  # previous value of modulated signal

        for x in range(img.shape[1]):
            sig = np.interp(img_gray[y, x], [0, 1], [min_phase, max_phase])
            sig_int += sig

            m = np.cos(omega * x + sig_int)

            if quantval > 0:
                m = np.interp(np.round(np.interp(m, [-1, 1], [0, quantval])), [0, quantval], [-1, 1])

            dem = abs(m - pre_m)
            pre_m = m

            if lowpass_cutoffs[0] > 0:
                dem = lpf1.lowpass(dem)
            if lowpass_cutoffs[1] > 0:
                dem = lpf2.lowpass(dem)
            if lowpass_cutoffs[2] > 0:
                dem = lpf3.lowpass(dem)

            v = np.clip(np.interp(2 * (dem - omega), [min_phase, max_phase], [0, 1]), 0, 1)

            result_img[y, x] = 1 - v if negate else v

    return img_as_ubyte(result_img)
def multiply_blend(img1, img2):
    img1 = img_as_float(img1)
    img2 = img_as_float(img2)
    
    # Ensure the images are the same size
    if img1.shape != img2.shape:
        img2 = np.resize(img2, img1.shape)
    
    blended = img1 * img2
    blended = np.clip(blended, 0, 1)  # Ensure values are within [0, 1]
    
    return img_as_ubyte(blended)
def alpha_blend(img1, img2, alpha=0.5):
    img1 = img_as_float(img1)
    img2 = img_as_float(img2)
    
    # Ensure the images are the same size
    if img1.shape != img2.shape:
        img2 = np.resize(img2, img1.shape)

    blended = alpha * img1 + (1 - alpha) * img2
    blended = np.clip(blended, 0, 1)  # Ensure values are within [0, 1]
    
    return img_as_ubyte(blended)

def main(image):
    img_a = np.copy(image)
    image = img_as_float(image)
    omega = 0.15 # 0.0 - 1.0         init=0.5  AMOUNT OF WAVEs
    phase_mult = 3 # 0.05 - 50.0    init=1.0   BRIGHTNess OF INVERSION
    quant = 10 # 0 - 100            init=30
    img_f = process_image(image, omega, phase_mult, quantval=quant)
    img_f = color.gray2rgb(img_f)
    #blended_img = alpha_blend(img_a, img_f, alpha=0.5)
    #blended_img = multiply_blend(img_a, img_f)
    blended_img = multiply_blend(img_a, img_f)
    # io.imsave('out.png', processed_img)
    return blended_img

    # plt.show()
if __name__ == "__main__":
    main()
