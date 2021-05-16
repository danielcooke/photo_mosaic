from PIL import Image
import numpy

image = Image.open('test_img.jpg')
new_image = image.resize((192, 108))
new_image.save('small.jpg')

I = numpy.asarray(Image.open('small.jpg'))