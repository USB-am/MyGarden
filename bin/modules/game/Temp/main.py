# -*- coding: utf-8 -*-

import pygame

# My modules
from Camera import Camera
from Hero import Hero
from InteractiveBlocks import *
from Map import Map
import Settings


if __name__ == '__main__':
	# === Create window === #
	pygame.init()

	master = pygame.display.set_mode(Settings.WIN_SIZE)
	pygame.display.set_caption('Game play')

	# === Init modules === #
	# = Hero = #
	hero = Hero(master, 10, 5, Settings.BLOCK_SIZE)
	hero.width = Settings.BLOCK_SIZE[0]
	hero.height = Settings.BLOCK_SIZE[1]

	# = Map = #
	bg = pygame.image.load(os.path.dirname(__file__) + '\\images\\textures\\grass.png')
	bg = pygame.transform.scale(bg, Settings.BLOCK_SIZE)
	farm_map = Map(master=master, name='farm')

	# = Camera = #
	camera = Camera(hero, (farm_map.map_size[0], farm_map.map_size[1]))

	# === Main cycle === #
	RUN = True
	while RUN:
		pygame.time.delay(30)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					RUN = False

				if event.key == Settings.HERO_MANAGMENT['up']:
					hero.move_up = True
				if event.key == Settings.HERO_MANAGMENT['left']:
					hero.move_left = True
				if event.key == Settings.HERO_MANAGMENT['down']:
					hero.move_down = True
				if event.key == Settings.HERO_MANAGMENT['right']:
					hero.move_right = True

				if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
					Settings.MOVE_SPEED *= 2

			if event.type == pygame.KEYUP:
				if event.key == Settings.HERO_MANAGMENT['up']:
					hero.move_up = False
				if event.key == Settings.HERO_MANAGMENT['left']:
					hero.move_left = False
				if event.key == Settings.HERO_MANAGMENT['down']:
					hero.move_down = False
				if event.key == Settings.HERO_MANAGMENT['right']:
					hero.move_right = False

				if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
					Settings.MOVE_SPEED /= 2

			if event.type == pygame.QUIT:
				RUN = False

		master.fill(Settings.BG_COLOR)

		# for x in range(Settings.WIN_SIZE[0]//Settings.BLOCK_SIZE[0]+1):
		# 	for y in range(Settings.WIN_SIZE[1]//Settings.BLOCK_SIZE[1]+1):
		# 		master.blit(bg, (x*Settings.BLOCK_SIZE[0], y*Settings.BLOCK_SIZE[1]))

		camera.update()
		farm_map.render()
		camera.draw(master)
		# hero.draw()
		pygame.display.flip()