import os
from sklearn.cluster import KMeans
from scipy import spatial
from skimage import io, color, img_as_float, img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt

def nearest(palette, colour):
    dist, i = palette.query(colour)
    return palette.data[i]

def OrderedDitheringColor(image, palette):
    # pure circle 8*8 matrix
    # matrix = [[ 8,12,12, 8, 8, 4, 4, 8],               
    #             [12,16,16,12, 4, 0, 0, 4],           
    #             [12,16,16,12, 4, 0, 0, 4],          
    #             [ 8,12,12, 8, 8, 4, 4, 8],
    #             [ 8, 4, 4, 8, 8,12,12, 8],               
    #             [ 4, 0, 0, 4,12,16,16,12],               
    #             [ 4, 0, 0, 4,12,16,16,12],               
    #             [ 8, 4, 4, 8, 8,12,12, 8]]
    # better 8*8 matrix
    # matrix =    [[ 8,12,12, 8, 8, 4, 4, 8],               
    #             [12,16,14,12, 4, 2, 2, 4],           
    #             [12,14,14,12, 4, 2, 0, 4],          
    #             [ 8,12,12, 8, 8, 4, 4, 8],
    #             [ 8, 4, 4, 8, 8,12,12, 8],               
    #             [ 4, 2, 2, 4,12,16,14,12],               
    #             [ 4, 2, 0, 4,12,14,14,12],               
    #             [ 8, 4, 4, 8, 8,12,12, 8]]
    # pure circle 16*16 matrix
    matrix =   [[ 8, 8, 8, 8, 8, 8, 8, 8,   8, 8, 8, 8, 8, 8, 8, 8],    
                [ 8,10,11,11,11,11,10, 8,   8, 6, 5, 5, 5, 5, 6, 8],         
                [ 8,11,12,13,13,12,11, 8,   8, 5, 4, 3, 3, 4, 5, 8],                               
                [ 8,11,13,16,16,13,11, 8,   8, 5, 3, 0, 0, 3, 5, 8],          
                [ 8,11,13,16,16,13,11, 8,   8, 5, 3, 0, 0, 3, 5, 8],        
                [ 8,11,12,13,13,12,11, 8,   8, 5, 4, 3, 3, 4, 5, 8],      
                [ 8,10,11,11,11,11,10, 8,   8, 6, 5, 5, 5, 5, 6, 8],        
                [ 8, 8, 8, 8, 8, 8, 8, 8,   8, 8, 8, 8, 8, 8, 8, 8],          

                [ 8, 8, 8, 8, 8, 8, 8, 8,   8, 8, 8, 8, 8, 8, 8, 8],              
                [ 8, 6, 5, 5, 5, 5, 6, 8,   8,10,11,11,11,11,10, 8],                      
                [ 8, 5, 4, 3, 3, 4, 5, 8,   8,11,12,13,13,12,11, 8],          
                [ 8, 5, 3, 0, 0, 3, 5, 8,   8,11,13,16,16,13,11, 8],                
                [ 8, 5, 3, 0, 0, 3, 5, 8,   8,11,13,16,16,13,11, 8],            
                [ 8, 5, 4, 3, 3, 4, 5, 8,   8,11,12,13,13,12,11, 8],                
                [ 8, 6, 5, 5, 5, 5, 6, 8,   8,10,11,11,11,11,10, 8],                                     
                [ 8, 8, 8, 8, 8, 8, 8, 8,   8, 8, 8, 8, 8, 8, 8, 8]]
    h, w, _ = image.shape
    for row in range(h-1):
        for col in range(1, w-1, 1):
            oldpixel = image[row, col].copy()
            spread = 0.8
            pixel = oldpixel + spread*((1/16)*matrix[row%16][col%16]-0.5)
            newpixel = nearest(palette, pixel)
            image[row, col] = newpixel
    # Ensure pixel values are clipped to the valid range [0, 1]
    image = np.clip(image, 0, 1)
    return image

def main(image):
    # read image
    # imgA = io.imread("in.png", as_gray=False).astype(np.uint8)
    image = img_as_float(image)
    image= image[:, :, :3] 

    palette = spatial.KDTree([[0.0,0.0,0.0],[1.0,1.0,1.0]])
    colours = palette.data
    colours = img_as_float([colours.astype(np.ubyte)])[0]

    # Call dithering function
    img = OrderedDitheringColor(image, palette)

    img = img_as_ubyte(img)

    #io.imsave('out.png', img)
    return img

if __name__ == "__main__":
    main()