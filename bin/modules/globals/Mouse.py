# -*- coding: utf-8 -*-

import pygame
import os


class Mouse(object):
	"""
	A class that controls the position and state of the cursor
	"""
	def __init__(self):
		self.x = 0					# X position
		self.y = 0					# Y position
		self.status = 'default'		# Cursor status (default, pressed, guidanced)

		self.__w, self.__h = pygame.display.get_surface().get_size()	# Main win size

		""" All cursor state icons """
		self.images = {
			'default' : pygame.transform.scale(
				pygame.image.load(os.path.dirname(__file__) + '\\images\\Mouse\\cursor.png'),
				(int(self.__w*.03), int(self.__w*.03)))
		}
		pygame.mouse.set_visible(False)	# Don't show the system cursor