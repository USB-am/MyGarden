# -*- coding: utf-8 -*-

import pygame
import datetime
import os.path
from math import sin, cos, pi
# My modules
from .. import Settings
from ..Pattern import Entity

pygame.font.init()


class Clock(pygame.sprite.Sprite):
	'''
	Class to create a Clock
	'''
	def __init__(self, position, size):
		super().__init__()

		self.position = position
		self.size = size
		self.hour = Settings.HOUR - 3
		self.minute = Settings.MINUTE - 180
		self.scale_position = {}

		self.image = pygame.Surface(self.size)
		self.rect = self.image.get_rect(topleft=self.position)
		for h in range(1, 13):
			self.scale_position[h] = (
				self.__calc_position(self.rect, h),
				self.__calc_position(self.rect, h, .9)
			)

		self.hour_arrow = self.__calc_position(self.rect, self.hour, .5)
		self.minute_arrow = self.__calc_position(self.rect, self.minute / 60, .8)

		font = pygame.font.SysFont('Arial', 10)
		self.am_time = font.render('AM', False, (255, 255, 255))
		self.pm_time = font.render('PM', False, (255, 255, 255))
		self.time_status_position = (
			self.rect.x + self.rect.width - self.am_time.get_width(),
			self.rect.y + self.rect.height - self.am_time.get_height()
		)


	def draw(self, master):
		time_status = 'AM' if 0 < self.hour + 3 < 12 else 'PM'
		# === Main ellipse ===
		pygame.draw.ellipse(
			master, pygame.Color('#ffffff'),
			(self.rect.x, self.rect.y,
			*self.rect.size)
		)
		# === Scales ===
		for xy in self.scale_position.values():
			pygame.draw.line(
				master,
				pygame.Color('#000000'),
				*xy, 2
			)
		# === Center point ===
		pygame.draw.ellipse(
			master, pygame.Color('#000000'),
			(
				self.rect.center[0] - 1,
				self.rect.center[1] - 1,
				3, 3
			)
		)
		# === Arrows ===
		# Minute arrow
		pygame.draw.line(
			master, pygame.Color('#550000'),
			self.rect.center,
			(self.__calc_position(
				self.rect,
				self.minute / 60,
				.8)
			),
			3
		)
		# Hour arrow
		pygame.draw.line(
			master, pygame.Color('#000055'),
			self.rect.center,
			(self.__calc_position(
				self.rect,
				self.hour,
				.5)
			),
			3
		)
		# === Status (AM, PM) ===
		if time_status == 'AM':
			master.blit(self.am_time, self.time_status_position)
		else:
			master.blit(self.pm_time, self.time_status_position)

		self.hour += Settings.HOUR_ARROW_SPEED
		self.minute += Settings.MINUTE_ARROW_SPEED


	def __calc_position(self, rect, hour, l=1):
		rad = rect.width / 2 * l
		x = rect.center[0] + rad * cos(hour * 30 * pi / 180)
		y = rect.center[1] + rad * sin(hour * 30 * pi / 180)

		return (int(x), int(y))


class TimePanel(pygame.sprite.Sprite):
	'''
	Class to create a timeline
	'''
	POSITION = (
		int(Settings.WIN_SIZE[0] * .75),
		0
	)
	SIZE = (
		int(Settings.WIN_SIZE[0] * .25),	# Width
		int(Settings.WIN_SIZE[1] * .2)		# Height
	)

	def __init__(self):
		super().__init__()

		# === Default values ===
		self.image = pygame.Surface(self.SIZE)
		self.image.fill(pygame.Color('#674633'))
		self.rect = self.image.get_rect(topleft=self.POSITION)

		self.clock = Clock(
			position=self.POSITION,
			size=(self.SIZE[1] / 1.5, self.SIZE[1] / 1.5)
		)

		self.initUI()


	def initUI(self):
		# === Date panel ===
		self.date_position = (self.POSITION[0] + self.SIZE[1]/1.5, self.POSITION[1])
		self.date_image = pygame.Surface((self.SIZE[0] - self.SIZE[1]/1.5, self.SIZE[1]/1.5))
		self.date_image.fill(pygame.Color('#ff0000'))
		self.date_rect = self.date_image.get_rect(topleft=self.date_position)

		# === Money panel ===
		self.money_position = (self.POSITION[0], self.POSITION[1] + self.SIZE[1] - self.SIZE[1]*.3)
		self.money_image = pygame.Surface((self.SIZE[0], self.SIZE[1]*.3))
		self.money_image.fill(pygame.Color('#ffe00e'))
		self.money_rect = self.money_image.get_rect(topleft=self.money_position)


	def draw(self, master):
		# hour, minute = now_time

		# === Main panel ===
		master.blit(self.image, self.POSITION)
		# === Clock ===
		self.clock.draw(master)
		# self.clock.hour += .01 / 12 / 10
		# self.clock.minute += .6 / 10
		# === Calendar panel ===
		master.blit(self.date_image, self.date_position)
		# === Money panel ===
		master.blit(self.money_image, self.money_position)


class Calendar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.number_mounths = ('spring', 'summer', 'autumn', 'winter')
		self._day = 1
		self._mounth = 0
		self._year = 1

		font = pygame.font.SysFont('Arial', 40)


	@property
	def day(self):
		return self._day
	@day.setter
	def day(self, val):
		if isinstance(val, int):
			if val < 29:
				self._day = val
			else:
				self._day = 1
				self.mounth += 1

	@property
	def mounth(self):
		return self._mounth
	@mounth.setter
	def mounth(self, val):
		if isinstance(mounth, int):
			if val < 4:
				self._mounth = val
			else:
				self._mounth = 0
				self._year += 1

	@property
	def year(self):
		return self._year


class Scale(Entity):
	def __init__(self, max_value, color, position, size):
		super().__init__(color=color, pos=position, size=size)

		self.size = size
		self.max_value = max_value
		self._value = max_value
		self.start_position = position


	def update_size(self):
		proc = self.max_value / 100 * self.value
		coord = self.start_position[1] + self.size[0] * proc / 100

		self.rect = pygame.Rect((
			self.rect.left,
			coord,
			self.rect.width,
			self.rect.height
		))
		# print(self.rect.y, self.value)


	def update(self, parent):
		parent.blit(self.image, self.rect.topleft)


	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, val:int):
		print(val)
		if self.value + val >= 0 and val < 0:
			# self.value - val <= self.max_value:
			self._value -= val
		elif self.value + val <= self.max_value and val > 0:
			self._value += val

		self.update_size()


class ScalePanel(pygame.sprite.Sprite):
	''' Class to create a strip characteristics '''

	# Размер полосок жизни/энергии
	SCALE_SIZE = (
		int(Settings.WIN_SIZE[0]*.03),
		int(Settings.WIN_SIZE[1]*.15)
	)
	# Позиция полосок жизни/энергии
	POSITIONS = {
		'health' : (
			int(Settings.WIN_SIZE[0] - SCALE_SIZE[0] * 2.2),
			int(Settings.WIN_SIZE[1] - SCALE_SIZE[1])
		),
		'energy' : (
			int(Settings.WIN_SIZE[0] - SCALE_SIZE[0] * 1.1),
			int(Settings.WIN_SIZE[1] - SCALE_SIZE[1])
		)
	}

	def __init__(self):
		super().__init__()

		bg_pos = (self.SCALE_SIZE[0] * 2.3, self.SCALE_SIZE[1] * 1.1)

		self.background = pygame.Surface(bg_pos)
		self.background.fill(pygame.Color('#cccccc'))
		self.background_rect = self.background.get_rect(topleft=(
			Settings.WIN_SIZE[0] - bg_pos[0],
			Settings.WIN_SIZE[1] - bg_pos[1]
		))

		self.health_scale = Scale(
			300,
			pygame.Color('#dd3333'),
			self.POSITIONS['health'],
			self.SCALE_SIZE
		)
		self.energy_scale = Scale(
			300,
			pygame.Color('#33dd33'),
			self.POSITIONS['energy'],
			self.SCALE_SIZE
		)


	def update(self, parent):
		parent.blit(self.background, self.background_rect.topleft)
		self.health_scale.update(parent)
		self.energy_scale.update(parent)


	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, change_value):
		if self.scroller_rect.y < Settings.WIN_SIZE[1]:
			percentage = 100 / change_value * self.max_value
			new_y = self.scroller_rect.y + (100 - percentage) * (self.scroller_rect.height / 100)
			if new_y < self.rect.bottom and 0 < percentage <= 100:
				self.scroller_rect.y = new_y
				self._value = change_value


class ActiveInstruments(pygame.sprite.Sprite):
	FONT = pygame.font.SysFont('arial', int(Settings.WIN_SIZE[1] * .05))

	def __init__(self):
		super().__init__()

		self._select_item = 49

		self.background = pygame.Surface((
			int(Settings.WIN_SIZE[0] * .6),
			int(Settings.WIN_SIZE[1] * .1)
		))
		self.background.fill(pygame.Color('#dcac26'))
		self.background_rect = self.background.get_rect(topleft=(
				int(Settings.WIN_SIZE[0] * .2),
				int(Settings.WIN_SIZE[1] * .9)
			)
		)

		self.rects = pygame.sprite.Group()
		self.HUD_ITEM_WIDTH = self.background_rect.width // Settings.INVENTORY_SIZE[0]
		self.__item_x_position = []

		self.select_sight = pygame.image.load(Settings.PATH_TO_TEXTURES + 'SelectBlock.png')
		self.select_sight = pygame.transform.scale(self.select_sight, (self.HUD_ITEM_WIDTH,)*2)


	@property
	def select_item(self):
		return self._select_item

	@select_item.setter
	def select_item(self, val:int):
		self._select_item = val


	def set_rects(self, rects):
		for rect in rects:
			self.rects.add(rect)


	def update(self, parent):
		parent.blit(self.background, self.background_rect.topleft)

		for num, rect in enumerate(self.rects):
			self.__item_x_position.append(
				int(self.background_rect.left + (num * self.HUD_ITEM_WIDTH))
			)

			block_position = (
				self.__item_x_position[-1],
				self.background_rect.top
			)
			parent.blit(rect.image, block_position)

			if self.select_item == 48:
				parent.blit(self.select_sight, (
					self.background_rect.right - self.HUD_ITEM_WIDTH,
					self.background_rect.top
				))
			elif num+48 == self.select_item:
				parent.blit(self.select_sight, (
					block_position[0] - self.HUD_ITEM_WIDTH,
					block_position[1]
				))

			if rect.has_item is not None:
				count_text = self.FONT.render(
					str(rect.count),
					True,
					(0, 0, 0)
				)
				parent.blit(rect.has_item.sprite,
					block_position,
					rect.has_item.sprite.get_clip()
				)

				parent.blit(
					count_text, (
					self.__item_x_position[-1] + self.HUD_ITEM_WIDTH - \
						count_text.get_size()[0],
					self.background_rect.bottom - count_text.get_size()[1]
				))


class HUD(pygame.sprite.Group):
	def __init__(self):
		super().__init__()

		self.health = 300
		self.energy = 300

		self.scale_panel = ScalePanel()

		#self.health_scale = Scale(self.health, 'health', pygame.Color('#dd3333'))
		#self.add(self.health_scale)
		#self.energy_scale = Scale(self.energy, 'energy', pygame.Color('#33dd33'))
		#self.add(self.energy_scale)
		self.timePanel = TimePanel()
		self.calendar = Calendar()
		self.active_panel = ActiveInstruments()


	def update(self, parent):
		for spr in self.sprites():
			parent.blit(spr.image, (spr.rect.x, spr.rect.y))
			parent.blit(spr.scroller, (spr.scroller_rect.x, spr.scroller_rect.y))

		self.timePanel.draw(parent)
		self.active_panel.update(parent)
		self.scale_panel.update(parent)