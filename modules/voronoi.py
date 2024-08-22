# import statements
import numpy as np
import math
from matplotlib import pyplot as plt
from skimage import io, draw
from scipy.spatial import Voronoi, voronoi_plot_2d
import random

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

class LCG():
    def __init__(self,seed):
        # ZX81 linear congruential generator parameters
        self.m = 2**16 + 1
        self.a = 75
        self.c = 74
        self.X = seed # seed
    
    def next(self):
        # Update the internal state using the LCG formula
        self.X = (self.a * self.X + self.c) % self.m
    
    def out(self):
        # Return the normalized output value
        return self.X / self.m


def main(imgA):
    
    # read image
    # imgA = io.imread("in.png", as_gray=False).astype(np.uint8)
    imgA = imgA[:, :, :3]
    pad = 30
    imgA = np.pad(imgA, ((pad, pad), (pad, pad), (0, 0)), mode='reflect')

    h, w, c = imgA.shape
    avg = np.mean(imgA, axis=(0, 1)).astype(np.uint8)
    imgB = np.full((h, w, c), avg, dtype=np.uint8)

    vertices = np.array([0,0])

    #random vertices
    lcg = LCG(random.randint(0,1000))
    for i in range(600):
        lcg.next()
        idx1 = int(lcg.out()*h)
        lcg.next()
        idx2 = int(lcg.out()*w)
        vertices = np.vstack([vertices, [idx1,idx2]])

    vor = Voronoi(vertices)

    regions = []
    out_point = -1
    for i in range(len(vor.regions)):
        if out_point not in vor.regions[i]:
            #creating singular region
            region = []
            for j in vor.regions[i]:
                region.append([int(vor.vertices[j][0]),int(vor.vertices[j][1])])
            regions.append(region)
    vertices = vor.vertices

    #delete empty
    regions.pop(0)

    for i in regions:
        if len(i)>2:
            rows = [point[0] for point in i]
            cols = [point[1] for point in i]
            
            # draw polygon
            rr, cc = draw.polygon(rows, cols)
        
            rr = np.clip(rr, 0, imgA.shape[0] - 1)
            cc = np.clip(cc, 0, imgA.shape[1] - 1)

            mean_color = np.mean(imgA[rr, cc], axis=0)
            imgB[rr, cc] = mean_color

    # unpad
    imgB = imgB[1:h - pad, 1:w - pad].astype(np.uint8)
    # plotter(imgB,"um")
    # plt.show()
    # io.imsave('out.png', imgB)
    
    return imgB

if __name__  == "__main__":
    main()