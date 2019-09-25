# -*- coding: utf-8 -*-

import numpy as np
import pygame
import os

# My modules
import InteractiveBlocks as IB
import Settings


class _MapGenerator(object):
	def __init__(self, master, path, background=None):
		self.master = master
		self.path = path
		self.background = background
		self.background_rect = self.background.get_rect()


	def __enter__(self):
		self._file = open(self.path, mode='r', encoding='utf-8')
		text = self._file.read()
		map_rows = text.split('\n')

		width = len(map_rows[0])
		height = len(map_rows)

		new_map = np.full((width, height), ' ')

		interactives = pygame.sprite.Group()

		for y, row in enumerate(map_rows):
			for x, col in enumerate(row):
				if col == 'm':
					value = IB.MapBorder(master=self.master, x=x, y=y, file='map_border.png')
				elif col == 's':
					value = IB.Stone(master=self.master, x=x, y=y, file='stone.png')
				else:
					continue
				new_map[x, y] = value
				interactives.add(value)

		return (interactives, new_map, (width, height))


	def __exit__(self, exc_ty, exc_val, tb):
		self._file.close()


class Map(object):
	def __init__(self, master, name=None):
		if name is None:
			raise AttributeError('Invalid map name!')

		self.master = master
		self.name = name.lower()

		bg = pygame.image.load(os.path.dirname(__file__) + '\\images\\textures\\grass.png')
		bg = pygame.transform.scale(bg, Settings.BLOCK_SIZE)

		path_to_map = os.path.dirname(__file__) + '\\MapPatterns\\%s.txt' % self.name
		if os.path.exists(path_to_map):
			mMap = _MapGenerator(master, path_to_map, background=bg)
			with mMap as blocks:
				self.sprite_list, self.iter_map, self.map_size = blocks
		else:
			raise OSError('File "%s" not exists!' % path_to_map)


	def render(self):
		for sp in self.sprite_list.sprites():
			sp.draw()