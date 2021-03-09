# -*- coding: utf-8 -*-

import pygame
import os.path
import json

# My Modules
from .Settings import *
from . import InteractiveBlocks as IB


class Map(object):
	def __init__(self, current, name):
		self.current = current
		self.name = name
		print(self.current, self.name, sep=' - ')
		path = os.path.dirname(__file__) + '\\Maps\\%s.json' % name
		self.hero_pos = BLOCK_SIZE

		if os.path.exists(path):
			file = open(path, mode='r', encoding='utf-8')

			self.new_map = json.load(file)
			self.width = len(self.new_map[0])
			self.height = len(self.new_map)

			file.close()
		else:	raise OSError('Not found file to "%s"' % path)


	def render(self, platforms, entities):
		for y, row in enumerate(self.new_map):
			for x, col in enumerate(row):
				if isinstance(col, str):
					if col == 'm':
						IB.MapBorder((x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]), platforms, entities)
					elif col == 's':
						IB.Stone((x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]), platforms, entities)
					elif col == 'b':
						IB.HomeBorder((x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]), platforms, entities)
					elif col == 'c':	# Containers
						IB.Container((x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]), platforms, entities)
				elif isinstance(col, list):
					if col[0] == 'H':
						IB.Home((x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]), platforms, entities, portal=col[1])
						col.append('down')
						self.hero_movement(col, x, y)
					elif col[0] == 'D':
						IB.Door((x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]), platforms, entities, portal=col[1])
						col.append('up')
						self.hero_movement(col, x, y)
					elif col[0] == 'P':
						IB.PassPortal((x*BLOCK_SIZE[0], y*BLOCK_SIZE[1]), platforms, entities, portal=col[1])
						self.hero_movement(col, x, y)


	def hero_movement(self, col, x, y):
		if col[1] == self.current:
			if col[2] == 'up':
				self.hero_pos = (x*BLOCK_SIZE[0], (y-1)*BLOCK_SIZE[1])
			elif col[2] == 'left':
				self.hero_pos = ((x-1)*BLOCK_SIZE[0], y*BLOCK_SIZE[1])
			elif col[2] == 'down':
				self.hero_pos = (x*BLOCK_SIZE[0], (y+1)*BLOCK_SIZE[1])
			elif col[2] == 'right':
				self.hero_pos = ((x+1)*BLOCK_SIZE[0], y*BLOCK_SIZE[1])