# -*- coding: utf-8 -*-

import pygame
# My Modules
from .Pattern import Entity
from . import Settings


class MapBorder(Entity):
	def __init__(self, pos, *groups):
		super().__init__('map_border', pos, *groups)


class Stone(Entity):
	def __init__(self, pos, *groups):
		super().__init__('stone', pos, *groups)
		self.hp = 10


class Home(Entity):
	def __init__(self, pos, *groups, portal=None):
		super().__init__('\\Home\\Home', (pos[0]-Settings.BLOCK_SIZE[0], pos[1]-Settings.BLOCK_SIZE[1]), *groups, size=(Settings.BLOCK_SIZE[0]*3, Settings.BLOCK_SIZE[1]*2))
		self.portal = portal


class HomeBorder(Entity):
	def __init__(self, pos, *groups):
		super().__init__('borderHome', pos, *groups)


class Container(Entity):
	def __init__(self, pos, *groups):
		super().__init__('box', pos, *groups)


class Door(Entity):
	def __init__(self, pos, *groups, portal=None):
		super().__init__('\\Home\\Door', pos, *groups)
		self.portal = portal


class PassPortal(Entity):
	def __init__(self, pos, *groups, portal=None):
		super().__init__(0, pos, *groups)
		self.portal = portal