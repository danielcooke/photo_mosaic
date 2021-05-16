from PIL import Image
import cv2
import numpy

vid_in = input('Enter the video file name: ')
img_in = input('ENter the base image file name: ')

image = Image.open(img_in)
img_out = image.resize((192, 108))
img_out.save('output.jpg')

cap = cv2.VideoCapture(vid_in)
i = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    cv2.imwrite('frames/' + str(i) + '.jpg',frame)
    i += 1
cap.release()
cv2.destroyAllWindows()