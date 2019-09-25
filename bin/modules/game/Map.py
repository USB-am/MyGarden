# -*- coding: utf-8 -*-

import numpy as np
import pygame
import os


class Stone(pygame.sprite.Sprite):
	__slots__ = ('x', 'y', 'hp')

	def __init__(self, x, y, hp=10):
		self.x = x
		self.y = y
		self.hp = hp


class Tree(pygame.sprite.Sprite):
	__slots__ = ('x', 'y', 'hp', 'drop', 'use_drop')

	def __init__(self, x, y, hp=10, drop='wood', use_drop=None):
		self.x = x
		self.y = y
		self.hp = hp
		self.drop = drop
		self.use_drop = use_drop


class ChildrenTree(pygame.sprite.Sprite):
	__slots__ = ('x', 'y', 'hp')

	def __init__(self, x, y, hp=1):
			self.x = x
			self.y = y
			self.hp = hp


class Map(object):
	def __init__(self, name:str, size:tuple):
		self.name = name
		self.mmap = self._loadMap()


	def _loadMap(self):
		pass