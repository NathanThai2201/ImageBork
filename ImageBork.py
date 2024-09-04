import numpy as np
import os
import re
from matplotlib import pyplot as plt
from skimage import io, util

from modules import kwhr, sort, od, gaus, fsd, chroma, asc, fm, haft, transforms, blend, slicer, triang, edge, histeq, voronoi, chroma_animation, edge_animation, belle, cope

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
    print("I. Use Dot Halftone dithering           --- i")
    print("J. Use Line Halftone dithering          --- j")
    print("K. Use Floyd-Steinberg dithering        --- k")
    print("l. Use Chromatic Aberration             --- l")
    print("M. Use Image to Ascii                   --- m")
    print("N. Use Threshold image blender (random) --- n")
    print("O. Use Invert image                     --- o")
    print("P. Use Image slicing (random)           --- p")
    print("Q. Use Delauney triangulation           --- q")
    print("R. Use Sobel edge outliner (random)     --- r")
    print("S. Use Histogram Equalization           --- s")
    print("T. Use Voronoi cell fracture            --- t")
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
        print("         I. Transforms")
        print("A. Scaling --- a(height scale number, width scale number)")
        print("     - Scale numbers are a float between 0 and 100")
        print("     - Leave field empty for default settings")
        print("     - EX: a(2,4)")
        print("B. Flipping --- b(direction string)")
        print("     - Direction is either \"ud\" or \"lr\"")
        print("     - Leave field empty for default settings")
        print("     - EX: b(lr)")
        print("C. Rotation --- c(rotation angle number)")
        print("     - Angle number is between 0 and 360")
        print("     - Leave field empty for default settings")
        print("     - EX: c(90)")
        print("         II. Filters")
        print("H. Ordered dithering --- h(palette number,spread float)")
        print("     - Palette number is between 1 and 10, -1 for auto generate")
        print("     - Spread float is between 0.0 and 1.0")
        print("     - Leave field empty for default settings")
        print("     - EX: h(2,0.1)")
        print("K. Floyd-Steinberg dithering --- k(palette number)")
        print("     - Palette number is between 1 and 10, -1 for auto generate")
        print("     - Leave field empty for default settings")
        print("     - EX: k(2)")
        print("Q. Delauney triangulation --- q(iteration number)")
        print("     - Iteration number is an int between 1 and 100")
        print("     - Leave field empty for default settings")
        print("     - EX: q(7)")
        print("R. Sobel edge outliner --- r(channel)")
        print("     - Channel is either \"r\", \"g\" or \"b\"")
        print("     - Leave channel \"a\" for all channels")
        print("     - Leave field empty for default settings")
        print("     - EX: r(g)")
        print("T. Voronoi cell fracture --- t(cell number)")
        print("     - Cell number is an int between 1 and 999")
        print("     - Leave field empty for default settings")
        print("     - EX: t(500)")
        print("         III. Animation")
        print("A. Animation temporal chromatic abberation --- a(mode)")
        print("     - Mode is either \"fi\", \"fo\" or \"fifo\"")
        print("     - Leave field empty for default no eases")
        print("     - EX: a(fi)")
        print("B. Animation temporal sobel edge outliner --- b(mode)")
        print("     - Mode is either \"fi\", \"fo\" or \"fifo\"")
        print("     - Leave field empty for default no eases")
        print("     - EX: b(fi)")
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

                h_scale=1.1
                w_scale=1.1
                match = re.search(r'a\(([\d.]+),([\d.]+)\)', effect)
                if match:
                    h_scale = float(match.group(1))
                    w_scale = float(match.group(2))
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
                img = haft.main2(img)
            elif effect[0] == 'k':
                cset = -1
                match = re.search(r'\((\d+)\)', effect)
                if match:
                    cset = int(match.group(1))   
                img = fsd.main(img,cset)
            elif effect[0] == 'l':
                img = chroma.main(img)
            elif effect[0] == 'm':
                img = asc.main(img)
            elif effect[0] == 'n':
                img = blend.main(img)
            elif effect[0] == 'o':
                img = util.invert(img)
            elif effect[0] == 'p':
                img = slicer.main(img)
            elif effect[0] == 'q':
                iterations = 6
                if len(effect)>=3:
                    if effect[2].isnumeric():
                        iterations = int(effect[2])
                if len(effect)>=4:
                    if effect[2:4].isnumeric():
                        iterations = int(effect[2:4])
                if len(effect)>=5:
                    if effect[2:5].isnumeric():
                        iterations = int(effect[2:5])
                img = triang.main(img, iterations)
            elif effect[0] == 'r':
                if len(effect)>=3:
                    if effect[2]=="r":
                        img = edge.main(img,"r")
                    elif effect[2]=="g":
                        img = edge.main(img,"g")
                    elif effect[2]=="b":
                        img = edge.main(img,"b")
                    elif effect[2]=="a":
                        img = edge.main(img,"a")
                    else:
                        img = edge.main(img,"none")
                else:
                    img = edge.main(img,"none")
            elif effect[0] == 's':
                img = histeq.main(img)
            elif effect[0] == 't':
                cell_number = 600
                if len(effect)>=3:
                    if effect[2].isnumeric():
                        cell_number = int(effect[2])
                if len(effect)>=4:
                    if effect[2:4].isnumeric():
                        cell_number = int(effect[2:4])
                if len(effect)>=5:
                    if effect[2:5].isnumeric():
                        cell_number = int(effect[2:5])
                img = voronoi.main(img, cell_number)
        img_path = os.path.join(folder_path, filenames[i])
        io.imsave(img_path+".png", img)
    os.system('cls' if os.name=='nt' else 'clear')
    input(' Images borked! Press any key to continue')
    return

def animation_page():
    os.system('cls' if os.name=='nt' else 'clear')
    print(" --- Add an effect! --- ")
    print(" Also be aware that there is no error checking, thus inputs must be precise")
    print("")
    print('************************')
    print("A. Use temporal chromatic aberration    --- a")
    print("B. Use temporal sobel edge outliner     --- b")
    print('************************')  
    print("")
    print("EX: a")
    print("")
    animation_input = input('Input:').lower()
    os.system('cls' if os.name=='nt' else 'clear')
    if animation_input == "ret":
        return
    else:
        return animation_processing_page(animation_input)
    
def animation_processing_page(animation_input):
    os.system('cls' if os.name=='nt' else 'clear')
    print(' Please wait while we cook!')

    if animation_input[0] == 'a':
        if len(animation_input)>=6 and animation_input[2:6]=="fifo":
            chroma_animation.main(mode ="fifo")
        elif len(animation_input)>=4 and animation_input[2:4]=="fi":
            chroma_animation.main(mode ="fi")
        elif len(animation_input)>=4 and animation_input[2:4]=="fo":
            chroma_animation.main(mode ="fo")
        else:
            chroma_animation.main()
    if animation_input[0] == 'b':
        if len(animation_input)>=6 and animation_input[2:6]=="fifo":
            edge_animation.main(mode ="fifo")
        elif len(animation_input)>=4 and animation_input[2:4]=="fi":
            edge_animation.main(mode ="fi")
        elif len(animation_input)>=4 and animation_input[2:4]=="fo":
            chroma_animation.main(mode ="fo")
        else:
            edge_animation.main()
    if animation_input == '*belle(in)':
        belle.main(mode="in")
    if animation_input == '*belle(out)':
        belle.main(mode="out")
    if animation_input == '*cope(in)':
        cope.main(mode="in")
    if animation_input == '*cope(out)':
        cope.main(mode="out")
    os.system('cls' if os.name=='nt' else 'clear')
    input(' Animation borked! Press any key to continue')
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
