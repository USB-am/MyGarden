# -*- coding: utf-8 -*-

import pygame
# My modules
from .Map import Map
from .Camera import Camera
from .Hero import Hero
from .Settings import *


class Move(object):
	def __init__(self):
		self._map_name = 'farm'


	def teleport(self, from_, to, player, platforms):
		self._map_name = to
		# platforms = pygame.sprite.Group()
		# player = Hero(platforms, BLOCK_SIZE)
		current_map = Map(from_, to)
		player.current_map = to
		entities = Camera(
			player,
			pygame.Rect(
				0,
				0,
				current_map.width*BLOCK_SIZE[0],
				current_map.height*BLOCK_SIZE[1]
			)
		)
		current_map.render(platforms, entities)
		player.rect.x = current_map.hero_pos[0]
		player.rect.y = current_map.hero_pos[1]

		return (current_map, entities)