# -*- coding: utf-8 -*-

import pygame
# My modules
from .MoveToMap import Move
from .Hero import Hero
from . import Weather
from . import Settings
# TEMP IMPORT
from . import Item


class Events:
	CLOSE_EVENT = False

	def __init__(self, parent):
		self.parent = parent

		self.teleporter = Move()
		self.platforms = pygame.sprite.Group()
		self.player = Hero(self.platforms, Settings.BLOCK_SIZE)
		# Стартовый телепорт на ферму
		self.current_map, self.entities = \
			self.teleporter.teleport(
				'home', 'farm', self.player, self.platforms
		)
		self.weather = Weather.Darkness()
		self.rain = Weather.Rain()


	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.CLOSE_EVENT = True
			elif event.type == pygame.KEYDOWN and \
				event.key == pygame.K_ESCAPE:
				self.CLOSE_EVENT = True

			if event.type == pygame.KEYDOWN:
				if event.key == Settings.PLAYER_MANAGMENT['inventory']:
					self.player.inventory.open()

				# Временная обработка события для добавления
				#	предмета в инвентарь игрока
				if event.key == Settings.PLAYER_MANAGMENT['add']:
					self.player.inventory.add_item(Item.Products(
						'pila', coord=(0, 0), money=1000
					))
				if event.key == Settings.PLAYER_MANAGMENT['add_x']:
					self.player.inventory.add_item(Item.Products(
						'x', coord=(0, 0), money=1000, stack=5
					))
				if event.key in Settings.PLAYER_MANAGMENT['nums']:
					self.player.hud.active_panel.select_item = event.key
					print('I\'m find collide in %s element!' % \
						Settings.PLAYER_MANAGMENT['nums'].index(event.key))

			if event.type == pygame.MOUSEMOTION:
				if not self.player.inventory.CLOSE:
					self.player.inventory.check_hover(*event.pos)

			if event.type == pygame.MOUSEBUTTONDOWN:
				if not self.player.inventory.CLOSE and event.button == 3:
					self.player.inventory.del_item(*event.pos)

		# Если игрок зашел на блок телепорта, то:
		if self.player.status:
			# Телепорт игрока в новую локацию
			self.platforms = pygame.sprite.Group()
			self.player.platforms = self.platforms
			self.current_map, self.entities = \
				self.teleporter.teleport(
					self.player.current_map,
					self.player.where,
					self.player,
					self.platforms
				)
			self.player.status = 0


	def update(self):
		# Обновление камеры
		self.entities.update()

		# Прорисовка окружения относительно смещения персонажа
		self.entities.draw(self.parent)

		# Отрисовка HUD персонажа
		self.player.hud.update(self.parent)

		# Отрисовка инвентаря (если включен)
		if not self.player.inventory.CLOSE:
			self.player.inventory.update(self.parent)

		# Изменение времени
		Settings.HOUR += Settings.HOUR_ARROW_SPEED
		Settings.MINUTE += Settings.MINUTE_ARROW_SPEED

		# Затемнение/погода
		# 	День/ночь
		self.weather.draw(self.parent)
		# 	Дождь
		# self.rain.update()
		# self.rain.draw(self.parent)