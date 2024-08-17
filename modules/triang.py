# import statements
import numpy as np
import math
from matplotlib import pyplot as plt
from skimage import io, draw
from scipy.spatial import Delaunay
import random


def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def main(imgA, iterations = 6):
    
    # read image
    # imgA = io.imread("in.png", as_gray=False).astype(np.uint8)
    imgA = imgA[:, :, :3]
    imgA = np.pad(imgA, ((1, 1), (1, 1), (0, 0)), mode='wrap')

    imgB = imgA - np.mean(imgA, axis=(0, 1))

    h, w, c = imgA.shape
    vertices = np.array([[1,1],[h-2,w-2],[h-2,1],[1,w-2]])
    # error difference map
    avg = np.mean(np.mean(imgA, axis=(0, 1)))

    # finding cross error for vertices when it crosses, theres a line
    error_index = [0, 0]
    for i in range(1, h-1):
        for j in range(1, w-1):
            pre = np.mean(imgB[i, j-1])
            temp = np.mean(imgB[i, j+1])
            if (pre < avg < temp) or (temp < avg < pre):
                error_index = [i, j]
                if i == 1 or i == (h-2):
                    vertices = np.vstack([vertices, error_index])
    for x in range(iterations):
        #print(vertices)
        # Triangulate using Delaunay
        """
        iterate block
        """
        triangles = Delaunay(vertices)
        triangle_coords = []
        vertices2 = np.array(vertices.data)
        for i in triangles.simplices:
            rr, cc = draw.polygon(
                [vertices[i[0], 0], vertices[i[1], 0], vertices[i[2], 0]],
                [vertices[i[0], 1], vertices[i[1], 1], vertices[i[2], 1]]
            )
            # clamp
            rr = np.clip(rr, 0, h - 1)
            cc = np.clip(cc, 0, w - 1)
            triangle_coords.append((rr, cc))
            
            # Calculate mean color of the triangle
            mean_color = np.mean(imgA[rr, cc], axis=0)
            avg = np.mean(mean_color)
            imgB[rr, cc] = mean_color
            
            # Check for error indexes
            detected_vertices = []
            for r, c in zip(rr, cc):
                if 0 < c < w - 1:
                    pre = np.mean(imgA[r, c-1])
                    temp = np.mean(imgA[r, c+1])
                    if (pre < avg < temp) or (temp < avg < pre):
                        detected_vertices.append([r, c])
            
            # append detected vertice
            if detected_vertices:
                middle_idx = len(detected_vertices) // 2
                vertices2 = np.vstack([vertices2, detected_vertices[middle_idx]])
        vertices = vertices2
    imgB = imgB[1:h - 1, 1:w - 1].astype(np.uint8)
    #print("")
    #print(vertices)
    #print(triangles.simplices)   
    # plotter(imgB, "err")
    # plt.triplot(vertices[:, 0], vertices[:, 1], triangles.simplices)
    # plt.plot(vertices[:, 0], vertices[:, 1], 'o')
    # plt.show()
    # io.imsave('out.png', imgB)
    
    return imgB


if __name__  == "__main__":
    main()