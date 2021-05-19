from PIL import Image
from random import randrange
import cv2
import os
import numpy

def main():

    vid_in_name = input('Enter the video file name: ') #input and check of video file name
    while(os.path.exists(vid_in_name) == False):
        vid_in_name = input('NAME INVALID, please enter a valid video file name: ')

    img_in_name = input('Enter the base image file name: ') #input and check of base image file name
    while(os.path.exists(img_in_name) == False):
        img_in_name = input('NAME INVALID, Please enter a valid base image file name: ')

    base_img = Image.open(img_in_name) #opening of base image and storing or image properties
    b_width = base_img.width
    b_height = base_img.height

    x_photos = input('Enter number of desired photos wide, please mantain the aspect ratio: ') #input and check of desired photos wide
    while((b_width % int(x_photos)) != 0):
        x_photos = input('DOES NOT MATCH ASPECT RATIO, please enter a valid number: ')
    x_photos = int(x_photos)

    y_photos = input('Enter number of desired photos tall, please mantain the aspect ratio: ') #input and check of desired photos tall
    while((b_height % int(y_photos)) != 0):
        y_photos = input('DOES NOT MATCH ASPECT RATIO, please enter a valid number: ')
    y_photos = int(y_photos)

    img_out_name = input('Enter the desired output image file name with file extention: ') #input of output file name

    vid_in = cv2.VideoCapture(vid_in_name) #code to extract frames from video files
    os.mkdir('frames')
    frame_number = 0
    while(vid_in.isOpened()):
        ret, frame = vid_in.read()
        if ret == False:
            break
        cv2.imwrite(f'frames/{frame_number}.jpg', frame) #frames are saved to a folder to be processed later
        frame_number += 1
    vid_in.release()
    cv2.destroyAllWindows()

    property_frame = Image.open('frames/0.jpg') #storing of video frames properties
    f_width = property_frame.width
    f_height = property_frame.height
    box = ((f_width - f_height)/2, 0, (f_width - ((f_width - f_height)/2)), f_height) #creation of crop box
    frame_index = []
    for i in range(frame_number):
        current_frame = Image.open(f'frames/{i}.jpg')
        square_frame = current_frame.crop(box) #squaring off of frame
        single_pixel = square_frame.resize((1, 1)) #reduced to singel pixel to get avg color for entire image
        frame_index.append(numpy.array(single_pixel)[0, 0]) #storing of avg color into a frame index to referance later

    color_index = numpy.array(base_img.resize((x_photos, y_photos))) #basically a map of desired colors for each region that a fram will fill
    photo_map = numpy.full((y_photos, x_photos), -1) #map of where each respective froma will go to make the photo mosaic
    for i in range(y_photos):
        for j in range(x_photos):
            tolerance = 0
            while photo_map[i][j] == -1:
                start = randrange(frame_number) #random start to reduce repetition
                for k in range(start, frame_number):
                    R_dif = abs(int(frame_index[k][0]) - int(color_index[i][j][0]))
                    G_dif = abs(int(frame_index[k][1]) - int(color_index[i][j][1]))
                    B_dif = abs(int(frame_index[k][2]) - int(color_index[i][j][2]))
                    if (R_dif <= tolerance and G_dif <= tolerance and B_dif <= tolerance):
                        photo_map[i][j] = k
                        break
                    else:
                        tolerance += 1 #if a frame is not found that matches the acceptiable tolerance is incread by 1 for each RGB value

    out_array = numpy.zeros((b_height, b_width, 3)) #output numpy array that will become the output image
    tile_width = int(b_width/x_photos) #calulation of the tile width
    tile_height = int(b_height/y_photos) #calulation of the tile height
    for i in range(y_photos):
        for j in range(x_photos):
            tile_frame = Image.open(f'frames/{photo_map[i][j]}.jpg')
            tile_square = tile_frame.crop(box) #squaring off of frames
            tile = tile_square.resize((tile_width, tile_height)) #turning frame into approperiate tile size
            tile_numpy = numpy.array(tile) #converting to numpy array
            for k in range(tile_height):
                for l in range(tile_width):
                    out_array[k + (i * tile_height)][l + (j * tile_width)][0] = tile_numpy[k][l][0]
                    out_array[k + (i * tile_height)][l + (j * tile_width)][1] = tile_numpy[k][l][1]
                    out_array[k + (i * tile_height)][l + (j * tile_width)][2] = tile_numpy[k][l][2]

    out_array = out_array.astype(numpy.uint8)
    img_out = Image.fromarray(out_array)
    img_out.save(img_out_name) #output image is saved

    for f in os.listdir('frames'): #removal of frames and frame folder
        os.remove(os.path.join('frames', f))
    os.rmdir('frames')

if __name__ == '__main__':
    main()