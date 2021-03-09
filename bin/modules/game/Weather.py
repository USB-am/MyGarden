# -*- coding: utf-8 -*-

import pygame
import random
import os.path
# My modules
from . import Settings
from .Pattern import Entity


def CALC_ALPHA():
	hour = -Settings.HOUR if Settings.HOUR > 12 else 12-Settings.HOUR
	return hour**2 + 12 * hour


class Darkness(pygame.sprite.Sprite):
	POSITION = (0, 0)

	def __init__(self):
		super().__init__()

		self.image = pygame.Surface(Settings.WIN_SIZE)
		self.image.fill(pygame.Color('#000000'))
		self.image.set_alpha(CALC_ALPHA())
		self.rect = self.image.get_rect(topleft=self.POSITION)

		self.light = {}


	def draw(self, master):
		alpha = CALC_ALPHA()
		self.image.set_alpha(alpha)
		master.blit(self.image, self.POSITION)

		'''
		block_size = list(Settings.BLOCK_SIZE)
		# light_color = (255, 255, 255, 30)
		light_color = (249, 237, 102, int(alpha))
		for alpha in range(Settings.SHARPNESS):
			sur = pygame.Surface(block_size, pygame.SRCALPHA)
			center = (
				Settings.WIN_SIZE[0] // 2 - block_size[0] // 2,
				Settings.WIN_SIZE[1] // 2 - block_size[1] // 2
			)

			pygame.draw.circle(
				sur,
				pygame.Color(*light_color),
				tuple(map(lambda v: int(v // 2), block_size)),
				int(block_size[0] // 2)
			)

			master.blit(sur, center)
			block_size = list(map(lambda v: v * Settings.LIGHT_RANGE, block_size))
		'''


class Rain(pygame.sprite.LayeredUpdates):
	def __init__(self):
		super().__init__()

		self.speed = 5
		self.vec = pygame.Vector2(0, 5)
		for drop in range(30):
			self.add(
				Entity(
					color = 'drop',
					pos = (
						random.randint(0, Settings.WIN_SIZE[0]-300),
						-300	# TEMP
					),
					size = tuple(map(lambda side: int(side * .2), Settings.BLOCK_SIZE))
				)
			)


	def update(self, *args):
		super().update(*args)

		x = 0
		y = self.speed
		self.vec += (pygame.Vector2((x, y)) + self.vec)

		if self.vec.y >= Settings.WIN_SIZE[1]:
			self.vec.y = -300


	def move(self, master):
		spritedict = self.spritedict
		master_blit = master.blit
		dirty = self.lostsprites
		self.lostsprites = []
		dirty_append = dirty.append
		init_rect = self._init_rect

		for spr in self.sprites():
			rec = spritedict[spr]
			newrect = master_blit(spr.image, spr.rect.move(self.vec))

			if rec is init_rect:
				dirty_append(newrect)
			else:
				if newrect.colliderect(rec):
					dirty_append(newrect.union(rec))
				else:
					dirty_append(newrect)
					dirty_append(rec)
			spritedict[spr] = newrect
		return dirty