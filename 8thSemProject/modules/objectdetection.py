import cv2
from PIL import Image
import os 

def create_crops(img,page,coords=None):
    if page:
        image = cv2.imread(img)
    else:
        image = cv2.imread(img)
        image = image[coords[1]:coords[3], coords[0]:coords[2]]
    blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        if len(approx) == 4:
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(image,(x,y),(x+w,y+h),(36,255,12),2)
            advanced_coords = [x,y,x+w,y+h]
            if page:
                im = Image.open(os.path.join(os.path.join(os.path.dirname( __file__ ), '..', 'sketches','newimage.jpg')))
                im1 = im.crop(advanced_coords)
                im1.save(os.path.join(os.path.join(os.path.dirname( __file__ ), '..', 'samples','content.jpg')))
                return advanced_coords
            else:
                im = Image.open(os.path.join(os.path.join(os.path.dirname( __file__ ), '..', 'samples','content.jpg')))
                im1 = im.crop([advanced_coords[0],advanced_coords[1],advanced_coords[2]+40,advanced_coords[3]+40])
                newsize = (200, 200) 
                im1 = im1.resize(newsize)
                im1.save(os.path.join(os.path.join(os.path.dirname( __file__ ), '..', 'samples',str(x)+str(y)+'.jpg')))
                


def split_images():
    coords = create_crops(os.path.join(os.path.join(os.path.dirname( __file__ ), '..', 'sketches','newimage.jpg')),True)
    coords = [coords[0]+20,coords[1]+20,coords[2]-20,coords[3]-20]
    create_crops(os.path.join(os.path.join(os.path.dirname( __file__ ), '..', 'sketches','newimage.jpg')),False,coords)