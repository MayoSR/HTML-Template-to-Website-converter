import numpy as np
import cv2
import os
from PIL import Image
import random

abs_path = "C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\"

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def image_process(name,element_type,index,rotation_axes):
    
    name = abs_path + "\\" + element_type + "\\" + name

        
    hsv_image = cv2.imread(name,1) # pretend its HSV
    #noise_img = sp_noise(hsv_image,0.2)
    rgbimg = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
    image_gray = cv2.cvtColor(rgbimg, cv2.COLOR_BGR2GRAY)
    _,threshold = cv2.threshold(image_gray,127, 255,0)

    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    left_arr = []
    right_arr = []
    top_arr = []
    bottom_arr = []

    for cnt in contours:
        leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
        rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
        topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
        bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
        left_arr.append(leftmost)
        right_arr.append(rightmost)
        top_arr.append(topmost)
        bottom_arr.append(bottommost)
        

    left_arr.sort()
    right_arr.sort(reverse=True)
    top_arr.sort(key = lambda x: x[1])
    bottom_arr.sort(reverse=True,key = lambda x: x[1])

    left_arr.pop(0)
    right_arr.pop(0)
    top_arr.pop(0)
    bottom_arr.pop(0)

    advanced_coords = (left_arr[0][0]-10,top_arr[0][1]-10,right_arr[0][0]+10,bottom_arr[0][1]+10)
    im = Image.open(name)
    im1 = im.crop(advanced_coords) 
    newsize = (200, 200) 
    im1 = im1.resize(newsize)
    totpath = abs_path + "\\" + element_type + "\\" + element_type+"_"+str(index)+".jpg"
    im1.save(totpath)
    
    
    if rotation_axes[0]:
        im2 = im1.rotate(90)
        im2.save(abs_path + "\\" + element_type + "\\" + element_type+"_"+str(index+1)+".jpg")
    
    if rotation_axes[1]:
        im3 = im1.rotate(180)
        im3.save(abs_path + "\\" + element_type + "\\" + element_type+"_"+str(index+2)+".jpg")
    
    if rotation_axes[2]:
        im4 = im1.rotate(270)
        im4.save(abs_path + "\\" + element_type + "\\" + element_type+"_"+str(index+3)+".jpg")
    
    if rotation_axes[3]:
        im5 = im1.transpose(Image.FLIP_LEFT_RIGHT)
        im5.save(abs_path + "\\" + element_type + "\\" + element_type+"_"+str(index+4)+".jpg")
    
    if rotation_axes[4]:
        im6 = im1.transpose(Image.FLIP_TOP_BOTTOM)
        im6.save(abs_path + "\\" + element_type + "\\" + element_type+"_"+str(index+5)+".jpg")
    
    
    
    os.remove(name)
    




def process_images(dir,rotation_axes):
    cnt = 2233

    for i in os.listdir(abs_path+dir):
        col = Image.open(abs_path+dir+"\\"+i)
        gray = col.convert('L')
        bw = gray.point(lambda x: 0 if x<128 else 255, '1')
        bw.save(abs_path+dir+"\\"+i)


    for i in os.listdir(abs_path+dir):
        image_process(i,dir,cnt,rotation_axes)
        cnt+=10
        print(cnt)


elements = {"Input":[False,True,False,True,True],"Image":[True,True,True,True,True],"Checkbox":[False,False,False,False,False],"Button":[True,True,True,True,True],"Video":[False,True,False,True,True]}


for i in elements:
    if i in ["Button"]:
        process_images(i,elements[i])
    