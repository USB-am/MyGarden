# -*- coding: utf-8 -*-

import pygame

# My Modules
from bin.modules.menu import MainMenu
from bin.modules.globals import Mouse
from bin.modules.globals import Manager
from bin.modules.game import main as gamePlay


def main():
	# === Variables ===
	load_objects = False                                # Boot window class object

	# === Create window ===
	pygame.init()

	master = pygame.display.set_mode((400, 250))        # Set window size
	pygame.display.set_caption('My Garden')             # Set window title

	mouse = Mouse.Mouse()                               # Init class cursor
	menu = MainMenu.MainMenu(master, mouse)             # Init class menu
	game = None                                         # Value for class "game"

	loading = False                                     # On/Off loading window
	RUN = True

	while RUN:
		pygame.time.delay(30)                           # FPS
		for event in pygame.event.get():                # Check player events
			if event.type == pygame.KEYDOWN:            # If user press button
				if event.key == pygame.K_ESCAPE:        # If button=Escape => 
					RUN = False                         # exit window

			if event.type == pygame.MOUSEMOTION:      # If user moving cursor
				mouse.x, mouse.y = event.pos

			if event.type == pygame.MOUSEBUTTONUP:    # If user press button
				if Manager.STATUS.get_value() == 0:     # If status=0 =>
					load_objects = menu.mouse_press(event.pos)  # Get new load window

			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	pass
			if event.type == pygame.QUIT:
				RUN = False

		if Manager.STATUS.get_value() == 0:             # Main menu
			menu.run()
		elif Manager.STATUS.get_value() == 1:           # Start a new game
			if load_objects:
				game = gamePlay.LoadFiles(master=master)
				if not loading:
					load_objects.run(master=master)
					loading = True
				print(game.name)
				# load_objects = False

		master.blit(mouse.images[mouse.status], (mouse.x, mouse.y)) # Show cursor
		pygame.display.update()                                     # Update window and draw new widgets


if __name__ == '__main__':
	main()
