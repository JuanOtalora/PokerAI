import numpy as np
from PIL import ImageGrab, Image
from pynput.mouse import Button, Controller
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
import time
import math
import cv2
import random
import json

# GLOBAL VARIABLES --------------------------------------------------------------------------------

log_to_console = True

game_coords = [0, 0, 0, 0]
player_number = 1

player_coords = {
	0: [195*2, 143*2],
	1: [630*2, 143*2],
	2: [769*2, 332*2],
	3: [624*2, 522*2],
	4: [202*2, 523*2],
	5: [54*2, 331*2]
}

river_coords = [292*2,311*2]

# idle, on-turn, 
current_state = 'idle'


RAISE_BET_COORDS = [796*2, 775*2]
RAISE_BET_COORDS_BOX = [796*2, 775*2]
FOLD_COORDS = [480*2, 775*2]
CALL_COORDS = [635*2, 775*2]


# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# GLOBAL OBJECTS ----------------------------------------------------------------------------------

mouse = Controller()
keyboard = KeyboardController()

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# HELPER FUNCTIONS --------------------------------------------------------------------------------

def debug(string):
	if log_to_console:
		print(string)

def current_game_state():
	coords_red_button = [FOLD_COORDS[0], FOLD_COORDS[1], FOLD_COORDS[0] + 20, FOLD_COORDS[1] + 20]
	button_red_img = ImageGrab.grab(bbox=coords_red_button)	
	#button_red_img.save("testRed.png")

	pass_condition = True

	for pixel in button_red_img.getdata():
		if (pixel[0] >= 180 and pixel[0] < 215) and (pixel[1] >= 70 and pixel[1] < 100) and (pixel[2] >= 40 and pixel[2] < 100):
			continue
		else:
			pass_condition = False
			break

	if pass_condition:
		return 'on-turn'
	else:
		return 'idle'

# Will return current pot, current drawn cards, current bet
def get_game_info():
	game_cards = []
	my_cards = []

	y = 0
	bounding_box = [river_coords[0], river_coords[1], river_coords[0]+30, river_coords[1]+76]
	for x in range(0,5):
		card_image = ImageGrab.grab(bbox=bounding_box)	
		card = get_card_value(card_image)
		y += 132
		bounding_box = [river_coords[0]+y, river_coords[1], river_coords[0]+30+y, river_coords[1]+76]
		
		if card != '' and card not in game_cards:
			game_cards.append(card)

	my_cards_coords = player_coords[player_number]
	y = 0
	bounding_box = [my_cards_coords[0], my_cards_coords[1], my_cards_coords[0]+30, my_cards_coords[1]+76]
	for x in range(0,2):
		card_image = ImageGrab.grab(bbox=bounding_box)	
		card_image.save(f'my_card_{x}.png')
		card = get_card_value(card_image)
		y += 132
		bounding_box = [my_cards_coords[0]+y, my_cards_coords[1], my_cards_coords[0]+30+y, my_cards_coords[1]+76]
		
		if card != '' and card not in game_cards:
			my_cards.append(card)

	return {
		'my_cards' : my_cards,
		'game_cards': game_cards
	}


def suggestion_action(game_info):
	my_cards = game_info['my_cards']
	game_cards = game_info['game_cards']

	if len(game_cards) == 0:
		# My first turn
		debug('No river detected...')
	else:
		pass

	return random.choice(['raise', 'fold', 'check', 'call'])

def get_card_value(card_image):
	blackV = False
	white = 0
	red = 0
	black = 0
	otherPixel = 0

	for pixel in card_image.getdata():
		if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0 and pixel[3] == 255:
			blackV = True

	for pixel in card_image.getdata():
		if (pixel[0] >= 245 and pixel[0]) <= 255 and (pixel[1] >= 245 and pixel[1] and (pixel[2] >= 245 and pixel[2]) and (pixel[3] >= 245 and pixel[3])):
			white += 1
		else:
			otherPixel += 1
	if blackV:
		black = otherPixel
	else:
		red = otherPixel

	card_pixel_values_file = open('card_pixel_values.json','r+')
	card_pixel_values = {}
	str_json = card_pixel_values_file.read()
	if str_json != "":
		card_pixel_values = json.loads(str_json)

	for k,v in card_pixel_values.items():
		if k.find("D") != -1 or k.find("H") != -1:
			if red == v["red"]:
				return k	
		else:
			if black == v["black"]:
				return k	
	return ""	

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# GAME ACTIONS ------------------------------------------------------------------------------------

def raise_bet(bet):
	mouse.position = (0, 0)
	mouse.move(RAISE_BET_COORDS[0]/2, RAISE_BET_COORDS[1]/2)
	time.sleep(0.1)
	mouse.click(Button.left, 1)
	mouse.position = (0, 0)
	time.sleep(0.1)

	# Then click the bet box and raise X amount

	mouse.move(RAISE_BET_COORDS_BOX[0]/2, RAISE_BET_COORDS_BOX[1]/2)

	bet_string = str(bet)
	for l in bet_string:
		keyboard.press(l)
		keyboard.release(l)
		time.sleep(0.1)

	mouse.position = (0, 0)

def fold():
	mouse.position = (0, 0)
	mouse.move(FOLD_COORDS[0]/2, FOLD_COORDS[1]/2)
	time.sleep(0.1)
	mouse.click(Button.left, 1)
	mouse.position = (0, 0)

def check():
	mouse.position = (0, 0)
	mouse.move(CALL_COORDS[0]/2, CALL_COORDS[1]/2)
	time.sleep(0.1)
	mouse.click(Button.left, 1)
	mouse.position = (0, 0)

def call():
	mouse.position = (0, 0)
	mouse.move(CALL_COORDS[0]/2, CALL_COORDS[1]/2)
	time.sleep(0.1)
	mouse.click(Button.left, 1)
	mouse.position = (0, 0)

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def main():
	player_number_string = input('Please select player number (0-5):')
	player_number = int(player_number_string)

	while True:
		# Frame speed
		time.sleep(1)

		# Get frame
		current_screen_frame = ImageGrab.grab(bbox=game_coords)
		debug('Grabed new frame...')

		# Get current game state
		current_state = current_game_state()
		debug(current_state)

		if current_state == 'idle':
			game_info = get_game_info()
			pass
		elif current_state == 'on-turn':
			game_info = get_game_info()
			action = suggestion_action(game_info)

			debug(f'Suggested action: {action}')

			if action == 'raise':
				raise_bet(10)
			elif action == 'fold':
				fold()
			elif action == 'check':
				check()
			elif action == 'call':
				call()

			current_state = 'idle'

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

main()
