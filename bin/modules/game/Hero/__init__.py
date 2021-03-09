# -*- coding: utf-8 -*-

import pygame
import os, time
# My modules
from . import HUD
from . import Sight
from .Inventory import Inventory
from .. import Settings


class Hero(pygame.sprite.Sprite):
	''' Персонаж '''

	# Размер персонажа
	SIZE = (int(Settings.BLOCK_SIZE[0]*.7), Settings.BLOCK_SIZE[1])
	# Отображаемый размер персонажа
	SPRITE_SIZE = (48, 98)
	# Координаты изображения для анимации
	SPRITE_POSITIONS = {
		'up' : (
			(26,  195, *SPRITE_SIZE),
			(118, 195, *SPRITE_SIZE),
			(208, 195, *SPRITE_SIZE),
			(297, 195, *SPRITE_SIZE),
			(390, 195, *SPRITE_SIZE)
		),
		'left' : (
			(21,   16, *SPRITE_SIZE),
			(114,  12, *SPRITE_SIZE),
			(200,  12, *SPRITE_SIZE),
			(295,  12, *SPRITE_SIZE),
			(383,  12, *SPRITE_SIZE)
		),
		'down' : (
			(22,  283, *SPRITE_SIZE),
			(114, 280, *SPRITE_SIZE),
			(204, 280, *SPRITE_SIZE),
			(293, 280, *SPRITE_SIZE),
			(284, 280, *SPRITE_SIZE)
		),
		'right' : (
			(384, 106, *SPRITE_SIZE),
			(292, 105, *SPRITE_SIZE),
			(209, 105, *SPRITE_SIZE),
			(115, 105, *SPRITE_SIZE),
			(27,  105, *SPRITE_SIZE),
		)
	}

	def __init__(self, platforms, pos, *groups):
		super().__init__()

		# Загрузка изображения с анимацией персонажа
		self.sprites = pygame.image.load(
			os.path.dirname(os.path.dirname(__file__)) \
			+ '\\images\\hero\\move.png')

		# Установка прозрачного цвета
		self.sprites.set_colorkey((0, 0, 0))
		# Стартовоое направление персонажа
		self.direction = 'right'
		# Индекс отрисовки спрайта при движении
		self._MOVE = 0
		# Время последнего обновления спрайта
		self.last_update = time.time()

		self.get_image()
		self.rect = self.image.get_rect(topleft=pos)

		self.vel = pygame.Vector2((0, 0))
		self.platforms = platforms
		self.speed = 5
		self.current_map = 'home'
		self.status = self.where = 0

		self.inventory = Inventory()
		# self.inventory.CLOSE = False
		self.hud = HUD.HUD()
		self.hud.active_panel.set_rects(
			[r for n, r in enumerate(self.inventory.rects) if n < 10])
		# self.sight = Sight.Sight()
		# self.platforms.add(self.sight)


	def update(self):
		# Получение события нажатия клавиши
		pressed = pygame.key.get_pressed()
		managment = Settings.PLAYER_MANAGMENT \
			if self.inventory.CLOSE else {}

		up      = pressed[managment.get('up',    False)]
		left    = pressed[managment.get('left',  False)]
		down    = pressed[managment.get('down',  False)]
		right   = pressed[managment.get('right', False)]
		running = pressed[managment.get('run',   False)]
		event   = pressed[managment.get('event', False)]
		eat     = pressed[managment.get('eat',   False)]

		if up:
			self.vel.y = -self.speed
			self.event_move('up')	# Событие движения вверх
		if down:
			self.vel.y = self.speed
			self.event_move('down')	# Событие движения вниз
		if left:
			self.vel.x = -self.speed
			self.event_move('left')	# Событие движения влево
		if right:
			self.vel.x = self.speed
			self.event_move('right')	# Событие движения вправо
		if running:	# Бег (ускорение персонажа в 3 раза)
			self.vel.x *= 3
			self.vel.y *= 3
			self.hud.scale_panel.energy_scale.value -= 1
		if event:
			self.hud.scale_panel.energy_scale.value -= 2
			# self.sight.update((self.rect.x, self.rect.y), self.direction)
		if eat:
			self.hud.scale_panel.energy_scale.value += 5

		if not(left or right):	self.vel.x = 0
		if not(up or down):	self.vel.y = 0

		# If hero_speed == 0
		if not any((up, down, left, right)):
			self._MOVE = 0

		self.rect.left += self.vel.x
		self.collide(self.vel.x, 0, self.platforms)
		self.rect.top += self.vel.y
		self.collide(0, self.vel.y, self.platforms)

		self.draw(self.get_image())


	def event_move(self, direction:str, many_events=False):
		if self.direction == direction:
			now_time = time.time()
			if self.last_update + Settings.ANIMATION_SPEED < now_time:
				self.MOVE += 1
				self.last_update = now_time
		elif many_events:
			# TODO: Обработка большого количества зажатий
			pass
		else:
			self._MOVE = 0
			self.direction = direction


	def get_image(self):
		sprite = self.sprites.copy()
		sprite.set_clip(
			pygame.Rect(self.SPRITE_POSITIONS[self.direction][self.MOVE])
		)
		self.image = sprite.subsurface(sprite.get_clip())
		self.image = pygame.transform.scale(self.image, self.SIZE)

		return sprite


	def draw(self, sprite):
		self.image.blit(
			sprite, (0, 0),
			self.SPRITE_POSITIONS[self.direction][self.MOVE]
		)


	def collide(self, xvel, yvel, blocks):
		for b in blocks:
			if pygame.sprite.collide_rect(self, b):
				try:
					self.where = b.portal
					self.status = 1
				except AttributeError:
					if xvel > 0:
						self.rect.right = b.rect.left
					if xvel < 0:
						self.rect.left = b.rect.right
					if yvel > 0:
						self.rect.bottom = b.rect.top
					if yvel < 0:
						self.rect.top = b.rect.bottom


	@property
	def MOVE(self):
		return self._MOVE

	@MOVE.setter
	def MOVE(self, val):
		if self._MOVE + val > len(self.SPRITE_POSITIONS['up']):
			self._MOVE = 0
		else:
			self._MOVE += 1


	def sleep(self):
		self.hud.calendar.day += 1
		Settings.HOUR = 8
		Settings.MINUTE = 0
		self.hud.health_scale.value = self.hud.health_scale.max_value
		self.hud.energy_scale.value = self.hud.energy_scale.max_value