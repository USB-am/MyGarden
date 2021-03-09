# -*- coding: utf-8 -*-

import pygame
# My modules
from .. import config


pygame.Font.init()

class Button(pygame.sprite.Sprite):
	def __init__(self, master, text='', \
		font=pygame.font.SysFont('Arial', 32), \
		bg=pygame.Color('#d6d6d6')):

		super().__init__()
		self.master = master
		self.text = text
		self.font = font
		self.bg = bg


	def place(self, relx, rely, relwidth, relheight):
		print('Hello world!')