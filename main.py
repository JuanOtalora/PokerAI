import numpy as np
from PIL import ImageGrab, Image
from pynput.mouse import Button, Controller
import time
import math
import cv2

ImageGrab.grab().save("test.png")
mouse = Controller()

im = Image.open('testCards/3H.png')

black = 0
red = 0
white = 0

for pixel in im.getdata():
	print(pixel)
	if pixel == (0, 0, 0, 255): # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
		black += 1
	elif (pixel[0] >= 245 and pixel[0]) <= 255 and (pixel[1] >= 245 and pixel[1] and (pixel[2] >= 245 and pixel[2]) and (pixel[3] >= 245 and pixel[3])):
		white += 1
	else:
		red += 1
print('black=' + str(black)+', red='+str(red) +', white='+str(white)  )

# Read pointer position
# print('The current pointer position is {0}'.format(mouse.position))

# Set pointer position
# mouse.position = (10, 20)
# print('Now we have moved it to {0}'.format(mouse.position))

# Move pointer relative to current position
# mouse.move(5, -5)

# Press and release
# mouse.press(Button.left)
# mouse.release(Button.left)

# Double click; this is different from pressing and releasing
# twice on Mac OSX
# mouse.click(Button.left, 2)

# Scroll two steps down
# mouse.scroll(0, 2)

while True:
	time.sleep(3)
	print('The current pointer position is {0}'.format(mouse.position))