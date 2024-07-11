#Dependencies
#from PIL import Image , ImageDraw , ImageOps
import pytesseract
import pyautogui
import os
import pathlib
from pytesseract import Output
import cv2
import numpy as np
from UnitClass import *

def get_bless_color(color):
    blessdict = {0: "Fire", 1: "Water", 2: "Wind", 3: "Earth", 4: "Light", 5: "Dark", 6: "Astra", 7: "Anima"}
    if color[0] >= 55 and color[0] < 75 and color[1] >= 25 and color[1] < 80 and color[2] >= 200 and color[2] < 240: 
        blessing = blessdict[0] #fire
    elif color[0] >= 170 and color[0] < 180 and color[1] >= 110 and color[1] < 130 and color[2] >= 60 and color[2] < 85: 
        blessing = blessdict[1] #water
    elif color[0] >= 75 and color[0] < 95 and color[1] >= 145 and color[1] < 170 and color[2] >= 80 and color[2] < 110: 
        blessing = blessdict[2] #wind
    elif color[0] >= 30 and color[0] < 60 and color[1] >= 95 and color[1] < 125 and color[2] >= 190 and color[2] < 210: 
        blessing = blessdict[3] #earth
    elif color[0] >= 0 and color[0] < 60 and color[1] >= 95 and color[1] < 175 and color[2] >= 180 and color[2] < 210: 
        blessing = blessdict[4] #light
    elif color[0] >= 170 and color[0] < 200 and color[1] >= 40 and color[1] < 75 and color[2] >= 105 and color[2] < 130: 
        blessing = blessdict[5] #dark
    elif color[0] >= 140 and color[0] < 170 and color[1] >= 80 and color[1] < 140 and color[2] >= 170 and color[2] < 220: 
        blessing = blessdict[6] #astra
    elif color[0] >= 120 and color[0] < 130 and color[1] >= 140 and color[1] < 175 and color[2] >= 150 and color[2] < 200: 
        blessing = blessdict[7] #anima
    else:
        blessing = "Unknown"
    return blessing

def to_none(variable):
    if variable == "":
        return "None"
    return variable

def image_to_text(image, slices, thresh, grayscale, psm, mask, maskslice):
    image = image[slices] #get name
    if mask == True:
        image = cv2.bitwise_and(image, image, mask=maskslice) #go and make a mask based on points, fill everything else black
    if grayscale == True:
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    image = cv2.threshold(image,thresh,255,cv2.THRESH_BINARY)[1]
    if psm == True:
        str_image = pytesseract.image_to_string(image, config = '--psm 6').strip("\n")
    else:
        str_image = pytesseract.image_to_string(image).strip("\n")
    return image, str_image
def makemask(baseimage, points):
    x,y,w,h = cv2.boundingRect(points)
    slices = np.s_[y:y+h, x:x+w]
    cropped = baseimage[slices].copy()
    points = points - points.min(axis=0)
    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA) #weapon mask
    return slices, mask
def replace_Il(string):
    words = string.split(" ")
    for l in range(0, len(words)):
        if "Il" == words[l]: #only Il, ones like, illness don't count
            words[l] = "II"
    string = " ".join(words)
    return string
#######

path = pathlib.Path("/Users/Volt/Desktop/Feh_image_to_arena_score")  # path directory
os.chdir(path) #directory here

try: 
    # creating a folder named text
    if not os.path.exists('test'): 
        os.makedirs('test') 
except OSError: 
    print ('Error: Creating directory of data') 

classsize = 32, 32 #icon ration for weapon class type for iphone 10 lmao


#okay so its only drames of videos that have very varied color values, images when downscaled has its coloes exacted lmao, should still be in the same range
#except screenshots have a, lower saturation? idk lets have alot of values

baseimage = cv2.imread("data/" + os.listdir("data")[0]) #get width and height of the cropped image so we can parse all images
weapon_slice, weapon_mask = makemask(baseimage, np.array([[510,370],[790,370],[805,390],[790,410],[510,410]]))
assist_slice, assist_mask = makemask(baseimage, np.array([[510,430],[790,430],[805,447],[790,472],[510,472]]))
special_slice, special_mask = makemask(baseimage, np.array([[510,490],[790,490],[805,512],[790,534],[510,534]]))
a_slice, a_mask = makemask(baseimage, np.array([[510,555],[790,555],[805,575],[790,595],[510,595]]))
b_slice, b_mask = makemask(baseimage, np.array([[510,615],[790,615],[805,635],[790,655],[510,655]]))
c_slice, c_mask = makemask(baseimage, np.array([[510,675],[790,675],[805,595],[790,715],[510,715]]))
s_slice, s_mask = makemask(baseimage, np.array([[510,735],[790,735],[805,755],[790,775],[510,775]]))

unitlist = {} #storing our units

numfiles = len(os.listdir("data")) #number of image files
print("Number of Units:", numfiles)
for i in range(1, numfiles): #every file in the data folder (numbers)
    image = cv2.imread("data/unit" + str(i) + ".png") #image of stats, og, not cropped yet
    #pil_image = Image.open("data/unit" + str(i) + ".png")
    #width, height = image.size
    
    im_name, str_name = image_to_text(image, np.s_[160:230, 95:445], 210, False, False, False, None) #cant get notts correct name... or any letter not in the english aplhabet... unless you're french (chloe)
    im_ephlet, str_ephlet = image_to_text(image, np.s_[65:135, 30:445], 210, False, False, False, None)
    #print(str_ephlet)
    im_lvl_merge, str_lvl_merge = image_to_text(image, np.s_[290:330, 150:275], 200, False, True, False, None)
    int_lvl = int(str_lvl_merge.split("+")[0])
    try: #sometimes no merges
        int_merge = int(str_lvl_merge.split("+")[1])
    except:
        int_merge = int(0)
    #print(str_lvl_merge)
    #print(int_lvl)
    #print(int_merge)
    im_weapon, str_weapon = image_to_text(image, weapon_slice, 190, False, False, True, weapon_mask)
    #print(str_weapon)
    im_assist, str_assist = image_to_text(image, assist_slice, 200, False, False, True, assist_mask)
    str_assist = replace_Il(str_assist)
    #print(str_assist)
    im_special, str_special = image_to_text(image, special_slice, 200, False, False, True, special_mask)
    str_special = replace_Il(str_special)
    #print(str_special)
    im_a, str_a = image_to_text(image, a_slice, 200, False, False, True, a_mask) #sometimes no assist, so no string
    str_a = replace_Il(str_a)
    #print(str_a)
    im_b, str_b = image_to_text(image, b_slice, 200, False, False, True, b_mask)
    str_b = replace_Il(str_b)
    #print(str_b)
    im_c, str_c = image_to_text(image, c_slice, 200, False, False, True, c_mask)
    str_c = replace_Il(str_c)
    #print(str_c)
    im_s, str_s = image_to_text(image, s_slice, 200, False, False, True, s_mask)
    str_s = replace_Il(str_s)
    #print(str_s)
    color = image[38, 100] #y, x get color value of rarity star, b,g,r
    #print(color)
    if color[0] < 130 and color[1] >= 120 and color[2] >= 150: #goldish
        rarity = int(5) 
    elif color[0] >= 130 and color[1] >= 120 and color[2] < 160: #silverish
        rarity = int(4)
    elif color[0] < 130 and color[1] < 120 and color[2] < 150: #brownish
        rarity = int(3)
    else:
        print(color)
        print("Uhhhh color not found")
        exit()
    #print(rarity)
    
    statdict = {0: "HP", 1: "ATK", 2: "SPD", 3: "DEF", 4: "RES"}
    index = 0
    asset = "" #intitialize in case, there is none
    asset2 = ""
    flaw = ""
    for k in [(389, 149), (453, 181), (510, 196), (575, 146), (635, 145)]: #position of stat colors, hp, atk, spd, def, res
        colorstat = image[k]
        #print(colorstat)
        if colorstat[2] < 200: #is blue asset
            if asset == "": #if no asset yet
                asset = statdict[index]
            else: #an asset has already been made.... an ascendednt floral
                asset2 = statdict[index]
        elif colorstat[0] < 200: #is red flaw
            flaw = statdict[index]
        index += 1
    #print(asset + ", " + flaw)
    
    blessdict = {0: "Fire", 1: "Water", 2: "Wind", 3: "Earth", 4: "Light", 5: "Dark", 6: "Astra", 7: "Anima"}
    blessing = "" #none as defult, tho, i guess if the hero name and ephlet is a mythic or legendary, we don't need to do this since they have fixed blessings
    for l in blessdict: #check for any blessing, blessing is always in the same place, rightmost
        im_bless = cv2.imread("icons/icon_Legend"+ blessdict[l]+".png")
        im_bless_smol = cv2.resize(im_bless, (144, 158))#some blessings are smoller because of 3 icons (our alear)
        im_bless_smol = im_bless_smol[48:67, 29:108]
        im_bless = cv2.resize(im_bless, (182, 197)) #regular blessing size (2 icons or less)
        im_bless = im_bless[48: 83, 37:147]

        iconlocation = pyautogui.locate(im_bless, image, confidence=0.9) #find just a blessing, don't care about color now because all blessings have the same shape
        #fire and light are too similar apparently
        if iconlocation is not None: #if ONE is found, since they all have the same shape, colors are harder to do this so we need to check the colors, then break
            color = image[128, 801] #y, x get color value of blessing, b,g,r, get the upper close pixel of badge
            blessing = get_bless_color(color)
            #print(blessing)
            #print(i, color, blessing)
            break

        iconsmalllocation = pyautogui.locate(im_bless_smol, image, confidence=0.9) #find just a blessing, don't care about color now because all blessings have the same shape
        if iconsmalllocation is not None: #find the color (smol)
            color = image[140, 806] #y, x get color value of smol blessing, b,g,r, change later
            blessing = get_bless_color(color)
            #print(blessing)
            #print(i, color, blessing, "smol")
            break

        #
        '''        
        w, h, _ = im_bless.shape
        res = cv2.matchTemplate(image, imageicon, cv2.TM_CCOEFF_NORMED)
        #print(res)
        threshold = 0.8
        loc = np.where( res >= threshold)
        print(loc)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            cv2.imwrite('res' + str(i) + '.png',image)
            #cv2.imshow("Display window", imageicon)
            #cv2.waitKey(0)
        '''

    unitlist[i] = Unit(str_name, str_ephlet, "None", "None", "None", rarity, to_none(str_weapon), to_none(str_assist), to_none(str_special), to_none(str_a), to_none(str_b), to_none(str_c), to_none(str_s), to_none(asset), to_none(asset2), to_none(flaw), int_lvl, int_merge, "None", "None", to_none(blessing))
    #print(unitlist[i])
    #print()
    print("Done with Unit", str_name +": "+ str_ephlet, i)
    #if i == 29:
    #    print(unitlist[i])
    #    exit()
    #break
    

    '''
    testimage = im_lvl_merge.copy()
    height, width, _ = testimage.shape
    text = pytesseract.image_to_boxes(testimage, output_type=Output.DICT)
    #print(text)
    n_boxes = len(text['char'])
    for i in range(n_boxes):
        (l, t, r, b) = (text['left'][i], text['top'][i], text['right'][i], text['bottom'][i])
        #print(l, t, r, b)
        cv2.rectangle(testimage, (l, height - t), (r, height - b), (255, 0, 0), 2) #make a box,deleet later
    
    cv2.imshow("Display window", testimage)
    cv2.waitKey(0)'''
    
#write it in a file
string = ""

for i in unitlist:
    string += str(unitlist[i])
    string += "\n\n"

f = open("demo.txt", "w")
f.write(string)
f.close()

exit()

imageicon = Image.open("icon/Icon_Class_Blue_Beast.png") #get class icon image
imageicon = imageicon.crop(imageicon.getbbox()) #crop transparency
imageicon.thumbnail(size, Image.Resampling.LANCZOS) #scale it down
#imageicon.show() #show it works

'''
text = pytesseract.image_to_data(image, output_type=Output.DICT)
#print(text)

n_boxes = len(text['level'])
for i in range(n_boxes):
    (x, y, w, h) = (text['left'][i], text['top'][i], text['width'][i], text['height'][i])
    image2 = ImageDraw.Draw(image)   
    image2.rectangle([(x, y), (x + w, y + h)], outline ="red") #make a box,deleet later

image.show()


text = pytesseract.image_to_boxes(image, output_type=Output.DICT)
#print(text)

n_boxes = len(text["char"])

for i in range(n_boxes):
    (l, t, r, b) = (text['left'][i], text['top'][i], text['right'][i], text['bottom'][i])
    #print(l, t, r, b)
    image2 = ImageDraw.Draw(image)   
    image2.rectangle([(l, height - t), (r, height - b)], outline ="red") #make a box,deleet later
image.show()


image = cv2.imread("data/frame0.png")
text = pytesseract.image_to_boxes(image)

for box in text.splitlines():
    box = box.split()
    print(box)
    print(box[1])
    image3 = cv2.rectangle(image, [int(box[1]), height - int(box[2])], [(int(box[3])), (height - int(box[4]))], (0, 255, 0), 2) #make a box,deleet later
    
cv2.imshow("image", image3)
cv2.waitKey(0)
'''

#strings = pytesseract.image_to_string(image)
#print(strings)

#image.show()



#get iconsssss
iconlocation = pyautogui.locate(imageicon, image, confidence=0.8)

if iconlocation is not None:
    print(iconlocation)
    shape = [(iconlocation.left, iconlocation.top), (iconlocation.left + iconlocation.width, iconlocation.top + iconlocation.height)]  # boxshape
    image1 = ImageDraw.Draw(image)   
    image1.rectangle(shape, outline ="red") #make a box,deleet later
    image.show()