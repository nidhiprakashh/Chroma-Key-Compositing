# -*- coding: utf-8 -*-
"""DIP_Assign2_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dW9k0a77DjzzZYROKwEwJxOwR-LxSZIP
"""

import numpy as np
import matplotlib.pyplot as plt
import skimage
from skimage import img_as_ubyte
from skimage import io
from skimage import filters
from skimage.morphology import disk

def remove_green(img):

    norm_factor = 255

    """get the ratio of the RGB channels based on
    the max brightness of the pixel"""
    red_ratio = img[:, :, 0] / norm_factor
    green_ratio = img[:, :, 1] / norm_factor
    blue_ratio = img[:, :, 2] / norm_factor

    """darker pixels have a value around 0. To prevent removing
    dark pixels.3 added to make small negative numbers positive"""

    red_vs_green = (red_ratio - green_ratio) + .3
    blue_vs_green = (blue_ratio - green_ratio) + .3

    """now, pixels with negative value will most likely be background green pixels."""
    red_vs_green[red_vs_green < 0] = 0
    blue_vs_green[blue_vs_green < 0] = 0

    """combine the red_vs_green and blue_vs_green ratios
    to create an aplha mask"""
    alpha = (red_vs_green + blue_vs_green) * 255
    alpha[alpha > 50] = 255

    img[:, :, 3] = alpha

    # rg_test=remove_green('/content/greenscreen images/reporter.jpg')
    # fig, ax = plt.subplots(1, 6)
    # ax[0].imshow(rg_test)

    return img

def draw(bg, green):
    fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
    # fig.suptitle("close this window to continue")
    ax[1].imshow(green)
    ax[0].imshow(bg)
    plt.show()

def rotate(bg,green):
    r_list = [0,90,180,-90,-180]
    r = 1
    while(r not in r_list):
        r = int(input("enter the amount of rotation (0,90,180,-90,-180)  "))
        if(r in r_list):
            green = skimage.transform.rotate(green, r, resize=True, mode='edge')
        else:
            print("\tinvalid value, try again")
    return green

def rescale(bg,green):
    h,w,_ = green.shape
    h1,w1,_ = bg.shape
    maxs = min(h1/h, w1/w) - 0.01
    s = 0.0
    maxs = round(maxs,2)
    while(s<0.1 or s>maxs):
        s = float(input("enter the amount of scaling (between 0.1 and " + str(maxs) + ")  "))
        if(s>=0.1 and s<=maxs):
            green = skimage.transform.rescale(green, s, multichannel=True)
        else:
            print("\tinvalid value, try again")
    return green

def blur(bg,green):
    b = 'x'
    while(b!='y' and b!='Y' and b!='n' and b!='N'):
        b = input("do you want to blur the background (y/n)  ")
        if(b=='y' or b=='Y'):
            bg = filters.gaussian(bg,sigma=5,multichannel=True)
        elif(b=='n' or b=='N'):
            break
        else:
            print("\tinvalid value, try again")
    return bg

def align(bg,green):
    h,w,_ = green.shape
    h1,w1,_ = bg.shape
    a = 0
    print("|1 2 3|")
    print("|4 5 6|")
    print("|7 8 9|")
    while(a<1 or a>9):
        a = int(input("enter the number corresponding to the required alignment...  "))
        if(a>=1 and a<=9):
            if(a==1):
                coord=(0,0)
            elif(a==2):
                coord=(0,int(w1/2-w/2))
            elif(a==3):
                coord=(0,w1-w)
            elif(a==4):
                coord=(int(h1/2-h/2),0)
            elif(a==5):
                coord=(int(h1/2-h/2),int(w1/2-w/2))
            elif(a==6):
                coord=(int(h1/2-h/2),w1-w)
            elif(a==7):
                coord=(h1-h,0)
            elif(a==8):
                coord=(h1-h,int(w1/2-w/2))
            elif(a==9):
                coord=(h1-h,w1-w)
        else:
            print("\tinvalid value, try again")
    return coord

def blend(bg, green):

    draw(bg,green)

    green = remove_green(green)
    green = rotate(bg,green)
    green = rescale(bg,green)
    bg = blur(bg,green)
    coord = align(bg,green)

    green = img_as_ubyte(green)
    bg = img_as_ubyte(bg)
    (x_size, y_size, _) = green.shape

    (x_ini, y_ini) = coord
    x_end = x_ini + x_size
    y_end = y_ini + y_size

    bg_crop = bg[x_ini:x_end,y_ini:y_end,:]

    """only the part of "green" with alpha values higher than 10 are taken
    "bg" pixels are replaced with corresponding "green" pixels for this part"""
    pixel_preserve = (green[:, :, -1] > 10)

    bg_crop[pixel_preserve] = green[pixel_preserve]

    bg[x_ini:x_end, y_ini:y_end, :] = bg_crop

    return bg

"""
"bg" is the background image and "green" is the image with the green background
"""

bg_path = input('enter name of background image...  ')
bg = skimage.io.imread('/content/background/' + bg_path + '.jpg', pilmode="RGBA")

green_path = input('enter name of green screen image...  ')
green = skimage.io.imread('/content/greenscreen images/' + green_path + '.jpg', pilmode="RGBA")

img = blend(bg,green)

plt.imshow(img)
plt.show()

plt.axis("off")
plt.imshow(img)

#instructions to run the code
"""
make new folders titled 'background' and 'greenscreen images'
upload the image(s) you want to use as the background to the 'background' folder in '<picture name>.jpg' format
images you want to overlay/composite should be with a green background and should be uploaded to the 'greenscreen images' folder in '<picture name>.jpg' format
run the code
enter the names of pictures as <picture name> (without .jpg extension)
"""