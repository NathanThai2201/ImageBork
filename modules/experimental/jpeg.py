
"""
Code refactored from 

"""


import io
import os
import random
import numpy as np
from skimage import io as skio, img_as_ubyte
from skimage.io import imsave, imread
import matplotlib.pyplot as plt

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

class Jpeg(object):

    def __init__(self, image_bytes, amount, seed, iterations):
        self.bytes = image_bytes
        self.new_bytes = None
        try:
            self.header_length = self.get_header_length()
        except ValueError as e:
            raise ValueError(e)

        self.parameters = {
            'amount': amount,
            'seed': seed,
            'iterations': iterations
        }

        self.glitch_bytes()

    def get_header_length(self):

        for i in range(len(self.bytes) - 1):
            if self.bytes[i] == 255 and self.bytes[i + 1] == 218:
                result = i + 2
                return result

        raise ValueError('Not a valid jpg!')

    def glitch_bytes(self):


        amount = self.parameters['amount'] / 100
        seed = self.parameters['seed'] / 100
        iterations = self.parameters['iterations']

        # work with a copy of the original bytes. We might need the original
        # bytes around if we glitch it so much we break the file.
        new_bytes = np.copy(self.bytes)

        for i in (range(iterations)):
            max_index = len(self.bytes) - self.header_length - 4

            px_min = int((max_index / iterations) * i)
            px_max = int((max_index / iterations) * (i + 1))
            delta = (px_max - px_min)
            px_i = int(px_min + (delta * seed))

            if (px_i > max_index):
                px_i = max_index

            byte_index = self.header_length + px_i
            new_bytes[byte_index] = int(amount * 256)

        self.new_bytes = new_bytes

    def save_image(self, name):

        while True:
            try:
                stream = io.BytesIO(self.new_bytes)
                image = skio.imread(stream, plugin='imageio')
                return img_as_ubyte(image)
            except Exception:
                if self.parameters['iterations'] == 1:
                    raise ValueError('This image is beyond repair, maybe try again?')

                self.parameters['iterations'] -= 1
                self.glitch_bytes()


def main(img):
    # Load target image and convert to jpg
    # img = imread('in.png').astype(np.uint8)
    img = img[:, :, :3]
    imsave('in.jpg', img)

    # take data stream
    with open('in.jpg', 'rb') as image:
        image_bytes = bytearray(image.read())

    # delete jpeg converted
    os.remove("in.jpg")

    # amount seed and iterations
    jpeg = Jpeg(image_bytes, random.randint(0, 99),
                random.randint(0, 99),
                random.randint(0, 115))

    result = jpeg.save_image('out.png')
    #plotter(result, "o")
    #imsave('out.png', result)
    return result

if __name__ == '__main__':
    main()
