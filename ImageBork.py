import numpy as np
import os
from matplotlib import pyplot as plt
from skimage import io, filters
from modules import kwhr, sort, od, gaus, fsd, chroma, asc, fm

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
    print('To exit, press X')
    print('************************')  
    landing_input = input('Input:').lower()
    os.system('cls' if os.name=='nt' else 'clear')
    output = 0
    if landing_input == "s":
        return selection_page()
    elif landing_input == "x":
        output = 0
    else:
        input('Unrecognized input, press any key to try again')
        return landing_page()
    return output

def selection_page():
    os.system('cls' if os.name=='nt' else 'clear')
    print(" --- Select a mode! --- ")
    print(" Place image files in the input folder, after processing the images will appear in the output folder.")
    print(" If selected image sequence mode, name the files from 0001 to xxxx")
    print('************************')
    print('To select single/batch images, press I')
    print('To select animated image sequence, press A')
    print('To return, press R')
    print('************************')  
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
    print("Use Frequency modulation                        --- a")
    print("Use Kuwahara filter                             --- b")
    print("Use Gaussian Blur                               --- c")
    print("Use Threshold pixel sorter                      --- d")
    print("Use Ordered dithering                           --- e")
    print("Use Floyd-Steinberg dithering                   --- f")
    print("Use Chromatic Aberration                        --- g")
    print("Use Image to Ascii                              --- h")
    print('************************')  
    print("")
    print("EX: b,c,e,d,g")
    print("")
    image_input = input('Input:').lower()
    os.system('cls' if os.name=='nt' else 'clear')
    if image_input == "r":
        return
    else:
        return image_processing_page(image_input)
    
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
        effects = effect_chain.split(',')
        for effect in effects:
            if effect == 'a':
                img = fm.main(img)
            if effect == 'b':
                img = kwhr.main(img)
            elif effect == 'c':
                img = gaus.main(img)
            elif effect == 'd':
                img = sort.main(img)
            elif effect == 'e':
                img = od.main(img)
            elif effect == 'f':
                img = fsd.main(img)
            elif effect == 'g':
                img = chroma.main(img)
            elif effect == 'h':
                img = asc.main(img)


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
