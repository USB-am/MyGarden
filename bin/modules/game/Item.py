# -*- coding: utf-8 -*-

import pygame
from os.path import dirname
# My modules
from .Pattern import Entity


class ItemStats:
	__slots__ = 'coord', 'money', 'stack'

	def __init__(self, coord, money, stack=2):
		self.coord = coord
		self.money = money
		self.stack = stack


TEXTURE_FILE = '%s\\images\\textures\\Products.png' % (dirname(__file__))
ALL_SPRITES = pygame.image.load(TEXTURE_FILE)
SPRITE_SIZE = (28, 28)
SPRITE_STATS = {
	'pila' : ItemStats((0, 373, *SPRITE_SIZE), 150),
	'x' : ItemStats((0, 456, *SPRITE_SIZE), 150),
}


class Products(Entity):
	def __init__(self, sprite_name, **stats):
		self.sprite_name = sprite_name
		self.stats = SPRITE_STATS[self.sprite_name]

		self.sprite = ALL_SPRITES.copy()
		self.sprite.set_clip(
			pygame.Rect(self.stats.coord)
		)

		# self.image = self.sprite.subsurface(self.sprite.get_clip())
		# self.image = pygame.transform.scale()

		super().__init__(self.sprite, (0, 0))