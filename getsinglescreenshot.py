#convert to our iphone 10 size lmao

# Importing all necessary libraries 
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(os.path.abspath(__file__))) #path directory of this script to get stuff
# Read the video from specified path 
again = True
while again == True:
    while True:
        enter = input("Pls enter an existing image file name: ")
        if enter == "/": #end program
            exit()
        if os.path.isfile(enter):
            image = cv2.imread(enter)
            break
    image = cv2.resize(image, (886, 1920))#scale to iphone size
    image = image[790:1580, 0:886] #cropped status page
    cv2.imwrite("Cropped"+ enter.split(".")[0] + ".png",image)
    print("Done")


