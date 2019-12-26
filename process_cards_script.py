import sys
from PIL import ImageGrab, Image
import json
from os import listdir

elems = listdir('./testCards')

card_pixel_values_file = open('card_pixel_values.json','w+')
card_pixel_values = {}

str_json = card_pixel_values_file.read()

if str_json != "":
	card_pixel_values = json.loads(str_json)

for elem in elems:
	if elem == '.DS_Store':
		continue

	print(f'Processing: {elem}')

	im = Image.open(f'./testCards/{elem}')

	black = 0
	red = 0
	white = 0

	for pixel in im.getdata():
		if pixel == (0, 0, 0, 255): # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
			black += 1
		elif (pixel[0] >= 245 and pixel[0]) <= 255 and (pixel[1] >= 245 and pixel[1] and (pixel[2] >= 245 and pixel[2]) and (pixel[3] >= 245 and pixel[3])):
			white += 1
		else:
			print(pixel)
			red += 1

	print('black=' + str(black)+', red='+str(red) +', white='+str(white))

	card = elem.replace('.png','')
	if card not in card_pixel_values:
		card_pixel_values[card] = {
			'black': black,
			'red': red,
			'white': white
		}

print("Persisting final values ...")
card_pixel_values_file.write(json.dumps(card_pixel_values))
card_pixel_values_file.close()
print("Saved! Goodbye...")
