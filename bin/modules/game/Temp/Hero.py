# -*- coding: utf-8 -*-

import pygame
import os

# My modules
import Settings


def backdir(path, step):
	step = abs(step) * -1
	return '\\'.join(path.split('\\')[:step])


class Hero(pygame.sprite.Sprite):
	def __init__(self, master, x, y, size):
		super().__init__()
		self.master = master
		self.master_rect = self.master.get_rect()

		self.image = pygame.image.load(os.path.dirname(__file__) + '\\images\\textures\\hero.png')
		self.image = pygame.transform.scale(self.image, (Settings.BLOCK_SIZE[0], int(Settings.BLOCK_SIZE[1]*1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = int(x * Settings.BLOCK_SIZE[0])
		self.rect.y = int(y * Settings.BLOCK_SIZE[1])

		self.move_up = False
		self.move_left = False
		self.move_down = False
		self.move_right = False


	def draw(self):
		if self.move_up:
			self.rect.y -= Settings.MOVE_SPEED
			if self.rect.top <= 0:
				self.rect.y = 0
		if self.move_left:
			self.rect.x -= Settings.MOVE_SPEED
			if self.rect.left <= 0:
				self.rect.x = 0
		if self.move_down:
			self.rect.y += Settings.MOVE_SPEED
			if self.rect.bottom >= self.master_rect.bottom:
				self.rect.bottom = self.master_rect.bottom
		if self.move_right:
			self.rect.x += Settings.MOVE_SPEED
			if self.rect.right >= self.master_rect.right:
				self.rect.right = self.master_rect.right

		self.master.blit(self.image, self.rect)