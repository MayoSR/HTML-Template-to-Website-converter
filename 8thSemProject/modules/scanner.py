import numpy as np
import cv2
import os
from PIL import Image
import random


class Preprocessor:
    

    def sp_noise(self,image,prob):
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

    def image_process(self,name,element_type,index):
        
        name = os.path.join('HTMLelements',element_type,name)
        try:
            
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
            im1.save(os.path.join('HTMLelements',element_type,element_type+"_"+str(index)+".jpg"))
                                
            im1 = im1.rotate(90)
            im1.save(os.path.join('HTMLelements',element_type,element_type+"_"+str(index+1)+".jpg"))
            
            im1 = im1.rotate(180)
            im1.save(os.path.join('HTMLelements',element_type,element_type+"_"+str(index+2)+".jpg"))
            
            im1 = im1.rotate(270)
            im1.save(os.path.join('HTMLelements',element_type,element_type+"_"+str(index+3)+".jpg"))
            
            os.remove(name)
        except:
                img = Image.open(name)
                print("Exception occured",i,img.size)

    
    def process_images(self):
        cnt = 1

        for i in os.listdir("HTMLelements\\Image"):
            self.image_process(i,"Image",cnt)
            cnt+=4
            print(cnt)

        cnt = 1
        for i in os.listdir("HTMLelements\\Input"):
            self.image_process(i,"Input",cnt)
            cnt+=4
            print(cnt)
