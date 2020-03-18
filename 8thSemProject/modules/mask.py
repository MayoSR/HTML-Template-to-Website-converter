from PIL import Image
import os 

for i in os.listdir("C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\Image"):
    col = Image.open("C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\Image\\"+i)
    gray = col.convert('L')
    bw = gray.point(lambda x: 0 if x<128 else 255, '1')
    bw.save("C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\Image\\"+i)
    
for i in os.listdir("C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\Input"):
    col = Image.open("C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\Input\\"+i)
    gray = col.convert('L')
    bw = gray.point(lambda x: 0 if x<128 else 255, '1')
    bw.save("C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\Input\\"+i)