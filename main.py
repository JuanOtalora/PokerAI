import numpy as np
from PIL import ImageGrab, Image
from pynput.mouse import Button, Controller
import time
import math
import cv2
import random

# GLOBAL VARIABLES --------------------------------------------------------------------------------

log_to_console = False

game_coords = [0, 0, 0, 0]
player_number = 1

player_coords = {
	0: [195, 143],
	1: [630, 143],
	2: [769, 332],
	3: [624, 522],
	4: [202, 523],
	5: [54, 331]
}

# idle, on-turn, 
current_state = 'idle'

RAISE_BET_COORDS = [0, 0]
FOLD_COORDS = [480, 775]
CALL_COORDS = [0, 0]

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# GLOBAL OBJECTS ----------------------------------------------------------------------------------

mouse = Controller()

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

	pass_condition = True

	for pixel in button_red_img.getdata():
		if (pixel[0] > 200 and pixel[0] < 215) and (pixel[1] > 90 and pixel[1] < 100) and (pixel[2] > 90 and pixel[2] < 100):
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
	pass

def suggestion_action(game_info):
	return random.choice(['raise', 'fold', 'check', 'call'])

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# GAME ACTIONS ------------------------------------------------------------------------------------

def raise_bet(bet):
	pass

def fold():
	pass

def check():
	pass

def call():
	pass

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

def main():
	while True:
		# Frame speed
		time.sleep(1)

		# Get frame
		current_screen_frame = ImageGrab.grab(bbox=game_coords)
		debug('Grabed new frame...')

		# Get current game state
		current_state = current_game_state()

		if current_state == 'idle':
			pass
		elif current_state == 'on-turn':
			game_info = get_game_info()
			action = suggestion_action(game_info)

			debug(f'Suggested action: {action}')

			if action == 'raise':
				raise_bet()
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
