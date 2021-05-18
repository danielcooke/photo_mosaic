from PIL import Image
import cv2
import os
import numpy

test = numpy.zeros((3,10), dtype = int)
test[1][3] = 5
print(test[1][3])
print(test)