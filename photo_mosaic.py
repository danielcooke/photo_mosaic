from PIL import Image
import cv2
import os
import numpy

vid_in_name = input('Enter the video file name: ')
img_in_name = input('Enter the base image file name: ')
x_photos= input('Enter number of desired photos wide: ')
y_photos = input('Enter number of desired photos tall: ')
img_out_name = input('Enter the desired output image file name: ')

vid_in = cv2.VideoCapture(vid_in_name)
count = 0
while(vid_in.isOpened()):
    ret, frame = vid_in.read()
    if ret == False:
        break
    cv2.imwrite('frames/' + str(count) + '.jpg', frame)
    count += 1
vid_in.release()
cv2.destroyAllWindows()

frame_index = numpy.zeros((count + 1,3), dtype = int)

base_img = Image.open(img_in_name)
img_out = base_img.resize((int(x_photos), int(y_photos)))
img_out.save(img_out_name)