import os


abs = "C:\\Users\\mayan\\Desktop\\Test\\8thSemProject\\HTMLelements\\"

cnt = 5000

for i in os.listdir(abs+"Image"):
    os.rename(abs+"Image\\"+i,abs+"Image\\"+"Image_"+str(cnt))
    cnt+=10