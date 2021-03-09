# -*- coding: utf-8 -*-

import pygame
# My modules
from .Pattern import Entity


class Citizen(Entity):
	def __init__(self, name, platforms, pos, *groups):
		super().__init__(platforms, pos, *groups)

		self.name = name
		self.vel = pygame.Vector2((0, 0))
		self.platforms = platforms
		self.speed = 5
		self.direction = 'right'


	def update(self):
		if up:
			self.vel.y = -self.speed
			self.direction = 'up'
		if left:
			self.vel.x = -self.speed
			self.direction = 'left'
		if right:
			self.vel.x = self.speed
			self.direction = 'right'
		if down:
			self.vel.y = self.speed
			self.direction = 'down'

		if not(left or right):
			self.vel.x = 0
		if not(up or down):
			self.vel.y = 0

		self.rect.left += self.vel.x
		self.collide(self.vel.x, 0, self.platforms)
		self.rect.top += self.vel.y
		self.collide(0, self.vel.y, self.platforms)


	def collide(self, xvel, yvel, blocks):
		for b in blocks:
			if pygame.sprite.collide_rect(self, b):
				if xvel > 0:
					self.rect.right = b.rect.left
				if xvel < 0:
					self.rect.left = b.rect.right
				if yvel > 0:
					self.rect.bottom = b.rect.top
				if yvel < 0:
					self.rect.top = b.rect.bottom


class Mayor(Citizen):
	def __init__(self, name, platforms, pos, *groups):
		super().__init__(name, platforms, pos, *groups)

		