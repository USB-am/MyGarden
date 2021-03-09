# -*- coding: utf-8 -*-

import pygame
# My modules
from .. import Settings


class Sight(pygame.sprite.Sprite):
	''' Прицел '''
	def __init__(self):
		super().__init__()

		self.position = {
			'up' : lambda x, y: (
				x // Settings.BLOCK_SIZE[0] * \
					Settings.BLOCK_SIZE[0],
				y // Settings.BLOCK_SIZE[1] * \
					Settings.BLOCK_SIZE[1] - Settings.BLOCK_SIZE[1]
			),
			'left' : lambda x, y: (
				x // Settings.BLOCK_SIZE[0] * \
					Settings.BLOCK_SIZE[0] - Settings.BLOCK_SIZE[1],
				y // Settings.BLOCK_SIZE[1] * \
					Settings.BLOCK_SIZE[1]
			),
			'down' : lambda x, y: (
				x // Settings.BLOCK_SIZE[0] * \
					Settings.BLOCK_SIZE[0],
				y // Settings.BLOCK_SIZE[1] * \
					Settings.BLOCK_SIZE[1] + Settings.BLOCK_SIZE[1]
			),
			'right' : lambda x, y: (
				x // Settings.BLOCK_SIZE[0] * \
					Settings.BLOCK_SIZE[0] + Settings.BLOCK_SIZE[0],
				y // Settings.BLOCK_SIZE[1] * \
					Settings.BLOCK_SIZE[1]
			)
		}

		self.image = pygame.Surface(Settings.BLOCK_SIZE)
		self.image.fill(pygame.Color('#aa1111'))
		self.rect = self.image.get_rect(topleft=self._position['right'](1, 1))


	def update(self, hero_pos, direction):
		self.rect.x, self.rect.y = self.position[direction].hero_pos