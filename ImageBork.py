import numpy as np
import os
import re
from matplotlib import pyplot as plt
from skimage import io, util

from modules import kwhr, sort, od, gaus, fsd, chroma, asc, fm, haft, transforms, blend

def plotter(img, name):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap=plt.cm.gray if img.ndim == 2 else None)
    ax.set_axis_off()
    ax.set_title(name)
    plt.show()

def landing_page():
    os.system('cls' if os.name=='nt' else 'clear')
    print("")  
    print("_________________________________________________________")
    print("| .-..-.  .-.  .--.  .----..----.  _             _   _  |")
    print("| { |}  \/  { / {} \ | |--'} |__} | |__  ___ _ _| |_| | |")
    print("| | }| {  } |/  /\  \| }-`}} '__} | '_ \/ _ \ '_| / /_| |")
    print("| `-'`-'  `-'`-'  `-'`----'`----' |_.__/\___/_| |_\_(_) |")    
    print("|_______________________________________________________|")                      
    print("")
    print(" Welcome to ImageBork!!")
    print('************************')
    print('To start, press S')
    print('To see the Manual, press M')
    print('To exit, press X')
    print('************************') 
    print("") 
    landing_input = input('Input:').lower()
    os.system('cls' if os.name=='nt' else 'clear')
    output = 0
    if landing_input == "s":
        return selection_page()
    elif landing_input == "x":
        output = 0
    elif landing_input == "m":
        return manual()
    else:
        input('Unrecognized input, press any key to try again')
        return landing_page()
    return output

def selection_page():
    os.system('cls' if os.name=='nt' else 'clear')
    print(" --- Select a mode! --- ")
    print(" Place image files in the input folder, after processing the images will appear in the output folder.")
    print(" If selected image sequence mode, name the files with numerics only")
    print("")
    print('************************')
    print('To select single/batch images, press I')
    print('To select animated image sequence, press A')
    print('To return, press R')
    print('************************')  
    print("")
    selection_input = input('Input:').lower()
    os.system('cls' if os.name=='nt' else 'clear')
    if selection_input == "i":
        return image_page()
    elif selection_input == "a":
        return animation_page()
    else:
        return
    return

def image_page():
    os.system('cls' if os.name=='nt' else 'clear')
    print(" --- Chain together effects! --- ")
    print(" Be aware that chaining too many effects can be computationally expensive")
    print(" For peak performance limit dimensions of images to 500x500.")
    print(" Also be aware that there is no error checking, thus inputs must be precise")
    print("")
    print('************************')
    print("         I. Transforms")
    print("A. Use height and width scaling         --- a")
    print("B. Use left right or up down flip       --- b")
    print("C. Use clockwise rotation               --- c")
    print("         II. Filters")
    print("D. Use Frequency modulation             --- d")
    print("E. Use Kuwahara filter                  --- e")
    print("F. Use Gaussian Blur                    --- f")
    print("G. Use Threshold pixel sorter           --- g")
    print("H. Use Ordered dithering                --- h")
    print("I. Use Halftone dithering               --- i")
    print("J. Use Floyd-Steinberg dithering        --- j")
    print("K. Use Chromatic Aberration             --- k")
    print("L. Use Image to Ascii                   --- l")
    print("M. Use Threshold image blender (random) --- m")
    print("N. Use Invert image                     --- n")
    print('************************')  
    print("")
    print("EX: e f h g k")
    print("")
    image_input = input('Input:').lower()
    os.system('cls' if os.name=='nt' else 'clear')
    if image_input == "ret":
        return
    else:
        return image_processing_page(image_input)
    
def manual(): 
    os.system('cls' if os.name=='nt' else 'clear')
    image_input = ""
    while image_input != "r":
        print(" --- Manual --- ")
        print("")
        print('************************')
        print("A. Scaling --- a(height scale number, width scale number)")
        print("     - Scale numbers are between 1 and 9")
        print("     - Leave field empty for default settings")
        print("     - EX: a(2,4)")
        print("B. Flipping --- b(direction string)")
        print("     - direction is either \"ud\" or \"lr\"")
        print("     - Leave field empty for default settings")
        print("     - EX: b(lr)")
        print("C. Rotation --- c(rotation angle number)")
        print("     - Angle number is between 0 and 360")
        print("     - Leave field empty for default settings")
        print("     - EX: c(90)")
        print("H. Ordered dithering --- h(palette number,spread float)")
        print("     - Palette number is between 1 and 10, -1 for auto generate")
        print("     - Spread float is between 0.0 and 1.0")
        print("     - Leave field empty for default settings")
        print("     - EX: h(2,0.1)")
        print("J. Floyd-Steinberg dithering --- j(palette number)")
        print("     - Palette number is between 1 and 10, -1 for auto generate")
        print("     - Leave field empty for default settings")
        print("     - EX: j(2)")
        print('************************')  
        print("")
        print("Press 1 to view palettes")
        print('To return, press R')
        print("")
        image_input = input('Input:').lower()
        os.system('cls' if os.name=='nt' else 'clear')
        if image_input == "1":
            od.show_palettes()
    return

def image_processing_page(effect_chain):
    folder_path = "./input"
    images = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(folder_path, filename)
            image = io.imread(img_path).astype(np.uint8)
            # Strip the alpha channel if it exists
            image = image[:, :, :3]
            images.append(image)   
            filenames.append(filename.rsplit('.', 1)[0])
    os.system('cls' if os.name=='nt' else 'clear')

    print(' Please wait while we cook!')
    folder_path = "./output"
    for i in range(len(images)):
        img = images[i]

        """
        effect chain
        """
        effects = effect_chain.split(' ')
        for effect in effects:
            if effect[0] == 'a':
                h_scale=1
                w_scale=1
                if len(effect)>=3:
                    if effect[2].isnumeric():
                        h_scale = int(effect[2])
                if len(effect)>=5:
                    if effect[4].isnumeric():
                        w_scale = int(effect[4])
                img = transforms.scaling(img,h_scale,w_scale)
            elif effect[0] == 'b':
                if len(effect)>=4 and effect[2:4]=="ud":
                    img = transforms.flipping(img,"ud")
                else:
                    img = transforms.flipping(img)
            elif effect[0] == 'c':
                angle=90
                if len(effect)>=3:
                    if effect[2].isnumeric():
                        angle = int(effect[2])
                if len(effect)>=4:
                    if effect[2:4].isnumeric():
                        angle = int(effect[2:4])
                if len(effect)>=5:
                    if effect[2:5].isnumeric():
                        angle = int(effect[2:5])
                img = transforms.rotation(img,angle)
            elif effect[0] == 'd':
                img = fm.main(img)
            elif effect[0] == 'e':
                img = kwhr.main(img)
            elif effect[0] == 'f':
                img = gaus.main(img)
            elif effect[0] == 'g':
                img = sort.main(img)
            elif effect[0] == 'h':
                spread = 0.1
                cset = -1
                match = re.search(r'h\((\d+),([\d.]+)\)', effect)
                if match:
                    cset = int(match.group(1))
                    spread = float(match.group(2))
                img = od.main(img,cset,spread)
            elif effect[0] == 'i':
                img = haft.main(img)
            elif effect[0] == 'j':
                cset = -1
                match = re.search(r'\((\d+)\)', effect)
                if match:
                    cset = int(match.group(1))   
                img = fsd.main(img,cset)
            elif effect[0] == 'k':
                img = chroma.main(img)
            elif effect[0] == 'l':
                img = asc.main(img)
            elif effect[0] == 'm':
                img = blend.main(img)
            elif effect[0] == 'n':
                img = util.invert(img)


        img_path = os.path.join(folder_path, filenames[i])
        io.imsave(img_path+".png", img)
    os.system('cls' if os.name=='nt' else 'clear')
    input(' Images borked! Press any key to continue')
    return

def animation_page():
    return





def main():
    # Run the landing page in a loop
    i= True
    while i:
        ans = landing_page()
        if ans == 0:
           i=False
    return

if __name__ == "__main__":
    main()