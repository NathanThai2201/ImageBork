import numpy as np
from matplotlib import pyplot as plt
from skimage import io
from skimage.color import rgb2hsv

class Span:
    def __init__(self, span):
        self.span = span
        self.start = span[0][:2]
        
    def sort_span(self):
        self.span = sorted(self.span, key=lambda x: x[2])  # Sort by hue
        
    def get_span(self):
        return self.span
    
    def get_start(self):
        return self.start

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def main(img):

    h, w, _ = img.shape
    # HSV conversion
    hsv_img = rgb2hsv(img)

    # Threshold calculation
    threshold = 80
    imgmask = np.zeros_like(img)
    
    for i in range(h):
        for j in range(w):
            if np.mean(img[i, j]) > threshold:
                imgmask[i, j] = [255, 255, 255]

    # Store spans
    spans = []
    for i in range(h):
        span = []
        for j in range(w):
            if imgmask[i, j, 0] == 255:
                span.append([i, j, hsv_img[i, j, 0]])
            elif span:
                spans.append(Span(span))
                span = []
        if span:
            spans.append(Span(span))

    # plotter(imgmask, "Mask")

    # Create output image
    img2 = img.copy()

    # Sort spans and replace
    for spano in spans:
        spano.sort_span()
        span = spano.get_span()
        start = spano.get_start()
        i = start[0]
        j = start[1]

        for b in range(len(span)):
            if j + b < w:
                img2[i, j + b] = img[span[b][0], span[b][1]]
            else:
                break  # Avoid out-of-bounds errors

    # io.imsave('out.png', img2)
    return img2

if __name__ == "__main__":
    main()
