# -*- coding: utf-8 -*-

import pygame
import os
# My modules
from Settings import BLOCK_SIZE


class Pattern(pygame.sprite.Sprite):
	def __init__(self, master, x, y, file=None, size=None):
		super().__init__()
		self.master = master

		if size is None:
			size = BLOCK_SIZE

		if file is not None:
			self.image = pygame.image.load(os.path.dirname(__file__) + '\\images\\textures\\%(name)s' % {'name':file})
			self.image = pygame.transform.scale(self.image, size)
			self.rect = self.image.get_rect()
			self.rect.x = int(x * size[0])
			self.rect.y = int(y * size[1])


	def draw(self):
		self.master.blit(self.image, self.rect)


class Stone(Pattern):
	def __init__(self, master, x, y, file):
		super().__init__(master, x, y, file)


class MapBorder(Pattern):
	def __init__(self, master, x, y, file):
		super().__init__(master, x, y, file)