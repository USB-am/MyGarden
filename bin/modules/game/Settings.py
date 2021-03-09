import pygame
from os.path import dirname

''' Общие '''
# Размер окна
WIN_SIZE = (800, 600)
# Экземпляр Rect с положение размером окна
SCREEN = pygame.Rect((0, 0, WIN_SIZE[0], WIN_SIZE[1]))
# Размер блока
BLOCK_SIZE = (50, 50)

# Путь до папки текстур
PATH_TO_TEXTURES = '%s\\images\\textures\\' % dirname(__file__)

''' Время '''
# Текущее время
HOUR = 11
MINUTE = 0
HOUR_ARROW_SPEED = .01 / 12 / 10	# Скорость часовой стрелки
MINUTE_ARROW_SPEED = .6 / 10		# Скорость минутной стрелки

# Свет
SHARPNESS = 5		# Резкость
LIGHT_RANGE = 1.5	# Дальность освещения

''' Персонаж '''
ANIMATION_SPEED = 0.15	# Скорость обновления анимации персонажа
PLAYER_MANAGMENT = {	# Кнопки управления персонажем
	'up' : pygame.K_w,
	'left' : pygame.K_a,
	'down' : pygame.K_s,
	'right' : pygame.K_d,
	'run' : pygame.K_LSHIFT,
	'inventory' : pygame.K_e,
	'event' : pygame.K_f,
	'eat' : pygame.K_q,
	'nums' : (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
		pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0),
	'add' : pygame.K_z,	# Temp
	'add_x' : pygame.K_x	# Temp
}

''' Инвентарь '''
# Размер инвентаря
INVENTORY_SIZE = (10, 4)
# Размер всего блока инвентаря
SIZE = tuple(map(lambda v: int(v*.8), WIN_SIZE))
# Позиция расположения инвентаря при отрисовке
POSITION = (
	WIN_SIZE[0] * .1,
	WIN_SIZE[1] * .1
)
# Размер области одной ячейки инвентаря
ITEM_SIZE = (
	# int((SIZE[0] // INVENTORY_SIZE[0]) * .7),
	# int((SIZE[0] // INVENTORY_SIZE[0]) * .7)
	SIZE[0] // INVENTORY_SIZE[0],
	SIZE[0] // INVENTORY_SIZE[0]
)