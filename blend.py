import numpy as np
import random
from skimage import io, img_as_float, img_as_ubyte
from skimage.color import rgb2hsv, hsv2rgb
import os
import matplotlib.pyplot as plt

# Constants
BLEND_COLOR = 0
BLEND_VALUE = 1
RED, GREEN, BLUE, HUE, SATURATION, BRIGHTNESS = range(6)
NRED, NGREEN, NBLUE, NHUE, NSATURATION, NBRIGHTNESS = range(6, 12)

# Parameters
mode = BLEND_COLOR
VALUE_FOR_BLEND = BRIGHTNESS
random_source = False
max_display_size = 1000
do_blend = False
blend_mode = 'overlay'


def load_images():
    folder_path = "./blend"
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(folder_path, filename)
            image = io.imread(img_path).astype(np.uint8)
            # Strip the alpha channel if it exists
            image = image[:, :, :3]
            images.append(image)   
    return images

def get_vector(c):
    return np.array([c[0], c[1], c[2]])

def get_channel(c, channel):
    if channel in [HUE, SATURATION, BRIGHTNESS]:
        hsv_c = rgb2hsv(c[np.newaxis, np.newaxis, :])[0, 0, :]
        ch = channel - 3  # Adjust index for HSV channels
        cc = hsv_c[ch]
    else:
        ch = channel
        cc = c[ch]
    
    return 1.0 - cc if channel >= 6 else cc

def process_image(target, sources, mode, value_for_blend, random_source):
    target_height, target_width, _ = target.shape
    buffer = np.zeros_like(target)
    indices = list(range(len(sources)))
    if random_source:
        nidx = random.randint(2, len(sources))
        random.shuffle(indices)
    else:
        nidx = len(sources)
    
    print(f"Using {nidx} images.")
    
    for x in range(target_width):
        for y in range(target_height):
            c = target[y, x]
            cv = get_vector(c)
            cval = get_channel(c, value_for_blend)
            currd = float('inf')
            currc = c
            for i in indices[:nidx]:
                _img = sources[i]
                _x = int(x / target_width * _img.shape[1])
                _y = int(y / target_height * _img.shape[0])
                _c = _img[_y, _x]
                d = np.linalg.norm(cv - get_vector(_c)) if mode == BLEND_COLOR else abs(cval - get_channel(_c, value_for_blend))
                if d < currd:
                    currd = d
                    currc = _c
            buffer[y, x] = currc
    
    return buffer

def blend_images(base, overlay, mode):
    if mode == 'overlay':
        return np.where(overlay <= 0.5, 2 * base * overlay, 1 - 2 * (1 - base) * (1 - overlay))
    # Add more blending modes if needed
    return base

def main():
    # Load target image
    target = img_as_float(io.imread("in.png"))
    target = target[:, :, :3]
    
    # Load source images
    sources = load_images()
    
    # Process image
    buffer = process_image(target, sources, mode, VALUE_FOR_BLEND, random_source)
    
    # Ensure the values are within the range [0, 1]
    buffer = np.clip(buffer, 0, 1)
    
    if do_blend:
        buffer = blend_images(target, buffer, blend_mode)
    
    io.imsave("out.png", img_as_ubyte(buffer))
    
    # Display result
    plt.imshow(buffer)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
