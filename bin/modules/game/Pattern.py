# -*- coding: utf-8 -*-

import pygame
import os.path
# My Modules
from . import Settings


class Entity(pygame.sprite.Sprite):
	def __init__(self, color, pos, *groups, size=Settings.BLOCK_SIZE):
		super().__init__(*groups)
		if isinstance(color, pygame.Color):
			self.image = pygame.Surface(size)
			self.image.fill(color)
		elif isinstance(color, str) and os.path.exists(os.path.dirname(__file__) + '\\images\\textures\\%s.png' % color):
			path = os.path.dirname(__file__) + '\\images\\textures\\%s.png' % color
			self.image = pygame.image.load(path)
			self.image = pygame.transform.scale(self.image, size)
		else:
			self.image = pygame.Surface(size)
			self.image.fill(pygame.Color('#FFFFFF'))
		self.rect = self.image.get_rect(topleft=pos)