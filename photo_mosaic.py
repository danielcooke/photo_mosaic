from PIL import Image
from random import randrange
import cv2
import os
import numpy

vid_in_name = 'test_vid.mp4' #input('Enter the video file name: ')
img_in_name = 'test_img.jpg' #input('Enter the base image file name: ')
x_photos = 96 #input('Enter number of desired photos wide: ')
y_photos = 54 #input('Enter number of desired photos tall: ')
img_out_name = 'output.jpg' #input('Enter the desired output image file name: ')

vid_in = cv2.VideoCapture(vid_in_name)
os.mkdir('frames')
count = 0
while(vid_in.isOpened()):
    ret, frame = vid_in.read()
    if ret == False:
        break
    cv2.imwrite(f'frames/{count}.jpg', frame)
    count += 1
vid_in.release()
cv2.destroyAllWindows()

property_frame = Image.open('frames/0.jpg')
box = ((property_frame.width - property_frame.height)/2, 0, (property_frame.width - ((property_frame.width - property_frame.height)/2)), property_frame.height)
frame_index = []
for i in range(count):
    current_frame = Image.open(f'frames/{i}.jpg')
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

matrix_out = numpy.zeros((base_img.height, base_img.width, 3))
small_x = int(base_img.width/x_photos)
small_y = int(base_img.height/y_photos)
for i in range(y_photos):
    for j in range(x_photos):
        big_tile = Image.open(f'frames/{photo_index[i][j]}.jpg')
        square_tile = big_tile.crop(box)
        tile = square_tile.resize((small_x, small_y))
        tile_numpy = numpy.array(tile)
        for k in range(small_y):
            for l in range(small_x):
                for m in range(3):
                    matrix_out[k + (i*small_y)][l + (j*small_x)][m] = tile_numpy[k][l][m]

matrix_out = matrix_out.astype(numpy.uint8)
img_out = Image.fromarray(matrix_out)
img_out.save(img_out_name)

for f in os.listdir('frames'):
    os.remove(os.path.join('frames', f))
os.rmdir('frames')