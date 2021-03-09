# -*- coding: utf-8 -*-

import pygame
# My modules
from ..Settings import *
from ..Pattern import Entity


# Инициализация шрифта
FONT = pygame.font.SysFont('arial', ITEM_SIZE[0] // 2)


class Equip(pygame.sprite.Sprite):
	''' Внешний вид персонажа '''

	def __init__(self):
		super().__init__()

		self.equip_rects = pygame.sprite.Group()

		self.equip_rects.add(Grid((
			POSITION[0] + ITEM_SIZE[0] * .11,
			POSITION[1] + ITEM_SIZE[1] * INVENTORY_SIZE[1]
		)))
		self.equip_rects.add(Grid((
			POSITION[0] + ITEM_SIZE[0] * 1.11,
			POSITION[1] + ITEM_SIZE[1] * INVENTORY_SIZE[1]
		)))
		self.equip_rects.add(Grid((
			POSITION[0] + ITEM_SIZE[0] * 2.11,
			POSITION[1] + ITEM_SIZE[1] * INVENTORY_SIZE[1]
		)))
		self.equip_rects.add(Grid((
			POSITION[0] + ITEM_SIZE[0] * .11,
			POSITION[1] + ITEM_SIZE[1] * INVENTORY_SIZE[1] + \
				ITEM_SIZE[1]
		)))
		self.equip_rects.add(Grid((
			POSITION[0] + ITEM_SIZE[0] * 1.11,
			POSITION[1] + ITEM_SIZE[1] * INVENTORY_SIZE[1] + \
				ITEM_SIZE[1]
		)))
		self.equip_rects.add(Grid((
			POSITION[0] + ITEM_SIZE[0] * 2.11,
			POSITION[1] + ITEM_SIZE[1] * INVENTORY_SIZE[1] + \
				ITEM_SIZE[1]
		)))


	def update(self, parent):
		self.equip_rects.update(parent)


class Grid(Entity):
	''' Ячейка инвентаря '''

	width = height = int(ITEM_SIZE[0] * .8)	# Размер
	# Наведен ли курсор на ячейку
	_hover = False

	def __init__(self, position, item=None, color=pygame.Color('#fdf2df')):
		super().__init__(
			color, position,
			size=(self.width, self.height)
		)

		# Координаты для отрисовки
		self.position = position
		# Хранимый предмет инвентаря
		self.has_item = item
		# Количество предметов данного типа в ячейке
		self._count = 0

		#	C	D	E	F	G	A	B
		#	do	re	mi	fa	sol	la	si

		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(pygame.Color('#fdf2df'))
		# self.image = pygame.image.load(PATH_TO_TEXTURES + 'grid.jpg')
		# self.image.convert_alpha()
		self.image = pygame.transform.scale(self.image, (
			self.width, self.height
		))
		self.rect = self.image.get_rect(topleft=self.position)


	@property
	def count(self):
		return self._count

	@count.setter
	def count(self, val:int):
		if val > 0:
			self._count = val
		else:
			self._count = 0
			self.has_item = None


	@property
	def hover(self):
		return self._hover

	@hover.setter
	def hover(self, value:bool):
		if value:
			self.image.fill(pygame.Color('#ffffff'))
		else:	self.image.fill(pygame.Color('#fdf2df'))


	def update(self, parent):
		# Отрисовка ячейки
		parent.blit(self.image, self.rect.topleft)

		# Если в клетке находится предмет, то:
		if self.has_item is not None:
			# Создание объекта текста
			count_text = FONT.render(
				str(self.count),
				True,
				(0, 0, 0)
			)
			# Отрисовка предмета
			parent.blit(
				self.has_item.sprite, self.rect.topleft,
				self.has_item.sprite.get_clip()
			)
			# Отрисовка текста
			parent.blit(
				count_text,
				tuple(map(lambda r, t: r - t,
					self.rect.bottomright,
					count_text.get_size()
				))
			)


class Inventory(pygame.sprite.Sprite):
	''' Инвентарь персонажа '''

	CLOSE = True	# Статус закрытия

	def __init__(self):
		super().__init__()

		self.background = pygame.Surface(SIZE)
		self.background.fill(pygame.Color('#c5872b'))
		# self.background = pygame.image.load(PATH_TO_TEXTURES +
		# 	'inventory_background.png')
		self.background = pygame.transform.scale(self.background, SIZE)
		self.background_rect = self.background.get_rect(
			topleft=(WIN_SIZE[0] * .1, WIN_SIZE[1] * .1)
		)

		''' Ячейки инвентаря '''
		# Группа для спрайтов ячеек инвентаря
		self.rects = pygame.sprite.Group()

		self.draw_grid()

		''' Снаряжение персонажа '''
		self.equip = Equip()


	def open(self):
		# Открытие инвентаря
		if self.CLOSE:
			print('Inventory is open!')
			self.CLOSE = False
		else:
			print('Inventory is closed!')
			self.CLOSE = True


	def draw_grid(self):
		# Создание объектов ячеек инвентаря

		for row in range(INVENTORY_SIZE[1]):
			for col in range(INVENTORY_SIZE[0]):
				# Добавление ячеек в группу спрайтов
				self.rects.add(Grid((
					col * ITEM_SIZE[0] + \
						WIN_SIZE[0] * .11,
					row * ITEM_SIZE[1] + \
						WIN_SIZE[1] * .11
				)))


	def add_item(self, item):
		# Добавление предметов в инвентарь

		for r in self.rects:
			# Если ячейка не содержит предмет:
			if r.has_item is None:
				r.has_item = item	# Перезапись значения
				r.count += 1		# Количество += 1
				break

			# Если ячейка содержит такой же объект и его количество
			# 	не превышает допустимое:
			elif r.has_item.sprite_name == item.sprite_name and\
				r.count < r.has_item.stats.stack:

				r.count += 1	# Количество += 1
				break
		else:
			print('My inventory is full!')


	def del_item(self, x, y):
		for rect in self.rects:
			p1, p2 = rect.position

			if p1 <= x <= p1 + rect.width and \
				p2 <= y <= p2 + rect.height:

				rect.count -= 1


	def check_hover(self, x, y):
		def check(rect):
			p1, p2 = rect.position

			if p1 <= x <= p1 + rect.width and \
				p2 <= y <= p2 + rect.width:
				rect.hover = True
			else:	rect.hover = False

		for rect in self.rects:
			check(rect)
		else:
			for rect in self.equip.equip_rects:
				check(rect)


	def update(self, parent):
		parent.blit(self.background, POSITION)
		self.rects.update(parent)
		self.equip.update(parent)