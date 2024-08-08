import numpy as np
import random
from skimage import io, transform
import os
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte, img_as_float

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def load_images():
    folder_path = "./modules/blend"
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(folder_path, filename)
            image = io.imread(img_path).astype(np.uint8)
            # Strip the alpha channel if it exists
            image = image[:, :, :3]
            images.append(image)   
    return images

def process_image(img, sources):
    h, w, _ = img.shape
    sources2 =[]
    for source in sources:
        sources2.append(transform.resize(source, (h, w), anti_aliasing=True))
    indices=[]
    if len(sources2)==0:
        return img
    else:
        # indices.append(random.randint(0, len(sources2)-1))
        # indices.append(random.randint(0, len(sources2)-1))
        # indices.append(random.randint(0, len(sources2)-1))
        indices = random.sample(range(0,len(sources2)-1), 4)
    
    h, w, _ = img.shape
    threshold_a = random.randint(0,50)
    threshold_b = random.randint(50,100)
    threshold_c = random.randint(150,200)
    imgmask = np.zeros_like(img)
    img2 = np.copy(img)
    for i in range(h):
        for j in range(w):
            imgmask[i,j] = [100,100,100]
            img2[i, j,0] = sources2[indices[0]][i,j,0]*255 + random.randint(-3,0)
            img2[i, j,1] = sources2[indices[0]][i,j,1]*255 + random.randint(-3,0)
            img2[i, j,2] = sources2[indices[0]][i,j,2]*255 + random.randint(-3,0)
            if np.mean(img[i, j]) > threshold_a:
                imgmask[i,j] = [150,150,150]
                img2[i, j,0] = sources2[indices[1]][i,j,0]*255 + random.randint(-3,0)
                img2[i, j,1] = sources2[indices[1]][i,j,1]*255 + random.randint(-3,0)
                img2[i, j,2] = sources2[indices[1]][i,j,2]*255 + random.randint(-3,0)
            if np.mean(img[i, j]) > threshold_b:
                imgmask[i,j] = [200,200,200]
                img2[i, j,0] = sources2[indices[2]][i,j,0]*255 + random.randint(-3,0)
                img2[i, j,1] = sources2[indices[2]][i,j,1]*255 + random.randint(-3,0)
                img2[i, j,2] = sources2[indices[2]][i,j,2]*255 + random.randint(-3,0)
            if np.mean(img[i, j]) > threshold_c:
                imgmask[i,j] = [255,255,255]
                img2[i, j,0] = sources2[indices[3]][i,j,0]*255 + random.randint(-3,0)
                img2[i, j,1] = sources2[indices[3]][i,j,1]*255 + random.randint(-3,0)
                img2[i, j,1] = sources2[indices[3]][i,j,2]*255 + random.randint(-3,0)
    img2 = multiply_blend(imgmask,img2)
    #plotter(img2,"s")
    return img2

def alpha_blend(img1, img2, alpha=0.5):
    img1 = img_as_float(img1)
    img2 = img_as_float(img2)
    
    # Ensure the images are the same size
    if img1.shape != img2.shape:
        img2 = np.resize(img2, img1.shape)

    blended = alpha * img1 + (1 - alpha) * img2
    blended = np.clip(blended, 0, 1)  # Ensure values are within [0, 1]
    
    return img_as_ubyte(blended)
def multiply_blend(img1, img2):
    img1 = img_as_float(img1)
    img2 = img_as_float(img2)
    
    # Ensure the images are the same size
    if img1.shape != img2.shape:
        img2 = np.resize(img2, img1.shape)
    
    blended = img1 * img2
    blended = np.clip(blended, 0, 1)  # Ensure values are within [0, 1]
    
    return img_as_ubyte(blended)
def main(target):
    # Load target image
    # target = io.imread("in.png", as_gray=False).astype(np.uint8)
    target = target[:, :, :3]
    
    # Load source images
    sources = load_images()
    
    # Process image

    img2 = process_image(target, sources)
    img2 = np.clip(img2, 0, 255)
    
    #io.imsave("out.png", img2)
    return img2

if __name__ == "__main__":
    main()
