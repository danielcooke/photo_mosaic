from PIL import Image
from random import randrange
import cv2
import os
import numpy

vid_in_name = 'test_vid.mp4' #input('Enter the video file name: ')
img_in_name = 'test_img.jpg' #input('Enter the base image file name: ')
x_photos = 48 #input('Enter number of desired photos wide: ')
y_photos = 27 #input('Enter number of desired photos tall: ')
img_out_name = 'output.jpg' #input('Enter the desired output image file name: ')

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

property_frame = Image.open('frames/0.jpg')
box = ((property_frame.width - property_frame.height)/2, 0, (property_frame.width - ((property_frame.width - property_frame.height)/2)), property_frame.height)
frame_index = []
for i in range(count):
    current_frame = Image.open('frames/' + str(i) + '.jpg')
    square_frame = current_frame.crop(box)
    single_pixel = square_frame.resize((1, 1))
    frame_index.append(numpy.array(single_pixel)[0,0])
frame_index_numpy = numpy.array(frame_index)

base_img = Image.open(img_in_name)
color_index = numpy.array(base_img.resize((int(x_photos), int(y_photos))))
photo_index = numpy.full((y_photos, x_photos), -1)
for i in range(y_photos):
    for j in range(x_photos):
        tolerance = 0
        while photo_index[i][j] == -1:
            start = randrange(count)
            for r in range(start, count):
                R_dif = abs(int(frame_index[r][0]) - int(color_index[i][j][0]))
                G_dif = abs(int(frame_index[r][1]) - int(color_index[i][j][1]))
                B_dif = abs(int(frame_index[r][2]) - int(color_index[i][j][2]))
                if (R_dif <= tolerance and G_dif <= tolerance and B_dif <= tolerance):
                    photo_index[i][j] = r
                    break
                else:
                    tolerance += 1
print(photo_index[0])

img_out = base_img.resize((int(x_photos), int(y_photos)))

img_out.save(img_out_name)