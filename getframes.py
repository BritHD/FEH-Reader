#main

# Importing all necessary libraries 
import cv2
import os
import numpy as np
from alive_progress import alive_bar

#box = [0: 172, 886: 418] #box size

os.chdir(os.path.dirname(os.path.abspath(__file__))) #path directory of this script to get stuff
# Read the video from specified path 

while True:
    enter = input("Pls enter an existing image file name: ")
    if os.path.isfile(enter):
        break
cam = cv2.VideoCapture(enter) 
baseimage = cv2.imread("basestatusscreen.png")
baseimage = baseimage[790:1580, 0:886] #crop to be the same as our frames
assist_special = baseimage[425:535, 455:510] #crop again for just the skils

try: 
    # creating a folder named data 
    if not os.path.exists('data'): 
        os.makedirs('data') 
  
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of data') 

length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
print("Approximate Frame Count:", length)

#allframes = []
statusframes = []
# frame 
#currentframe = 0
print("Framing Video...")
with alive_bar(length) as bar:
    while(True): 
        # reading from frame 
        ret,frame = cam.read() 
        if ret: 
            # if video is still left continue creating images 
            #name = './data/frame' + str(currentframe) + '.png' #file name
            #print('Creating frame', currentframe) #creating......
            
            #scale in case the frame is a different size lmao

            frame = frame[790:1580, 0:886] #crop size y, x

            image = frame[425:535, 455:510]
            res = cv2.matchTemplate(image, assist_special, cv2.TM_CCOEFF_NORMED) #same rate (.99 is pretty same!!!!, lower means its different)
            #print(i, res)
            if res > .99: #find the status screen, append to new frames
                statusframes.append(frame)
            # writing the extracted images 
            #cv2.imwrite(name, frame) 
            # increasing counter so that it will 
            # show how many frames are created 

            #statusframes.append(frame)

            #currentframe += 1
            bar()
        else: 
            break

'''
index = 0

print("Exact Number of Frames:", len(allframes))
statusframes = []
with alive_bar(len(allframes)) as bar:
    for i in allframes: #for all files in here, get the status screen only
        #image = cv2.imread("data/frame" + str(i) + ".png")
        image = i[425:535, 455:510]
        res = cv2.matchTemplate(image, assist_special, cv2.TM_CCOEFF_NORMED) #same rate (.99 is pretty same!!!!, lower means its different)
        #print(i, res)
        if res > .99: #find the status screen, append to new frames
            #print(index)
            statusframes.append(i)
        index += 1
        bar()
'''
print("Status Frames:", len(statusframes))

index = 0
brightframe = []
with alive_bar(len(statusframes)) as bar:
    for i in statusframes: #for all files in here, we need to delete duplicates, by matching the colors, in grayscale
        #image = cv2.imread("data/frame" + str(i) + ".png", cv2.IMREAD_GRAYSCALE)
        #cv2.imwrite("testing/testing" + str(i) + ".png", image) 
        image = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        colorvalue = image[310, 93] #310, 93 y, x
        if colorvalue > 240: #when screen is bright, not dar
            #print(index)
            brightframe.append(i)
        index += 1
        bar()

print("Bright Frames:", len(brightframe))

lastindex = 0
uniqueframe = []

with alive_bar(len(brightframe)) as bar:
    for i in range(0, len(brightframe)-1): #for all files in here, we need to delete duplicates, by templating eachother
        #image = cv2.imread("data/frame" + str(i) + ".png")
        #image2 = cv2.imread("data/frame" + str(i + 1) + ".png")
        image = brightframe[i]
        image2 = brightframe[i + 1] #frame after this one
        res = cv2.matchTemplate(image2, image, cv2.TM_CCOEFF_NORMED) #same rate (.95 is pretty same!!!!, lower means its different)
        if res < .95:
            #print("Last one:", i, res)

            uniqueframe.append(brightframe[i])
            #for l in range(lastindex, i): #anything from last pic non duplicate pic
            #    os.remove("data/frame" + str(l) + ".png") #remove screenshot
            lastindex = i + 1 #last index + 1 to save out latest pic
        if i == len(brightframe) - 2: #last images, delete those dups:
            #print("Last one:", i + 1)
            uniqueframe.append(brightframe[i + 1])
            #for l in range(lastindex, i + 1): #anything from last pic non duplicate pic
            #    os.remove("data/frame" + str(l) + ".png") #remove screenshot
        bar()

print("Print Unique Units", len(uniqueframe))

index = 1
with alive_bar(len(uniqueframe)) as bar:
    for i in uniqueframe:
        cv2.imwrite("data/unit" + str(index) + ".png", i) 
        index += 1
        bar()

cam.release() 
cv2.destroyAllWindows() 

print("Done")