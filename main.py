# -*- coding: utf-8 -*-

import pygame

# My modules
''' MENU: '''
# from bin.modules.menu import widgets
''' GAME: '''
# Обработчик событий
from bin.modules.game.KeyEvents import Events
# Настройки
from bin.modules.game import Settings


def main():
	pygame.init()
	screen = pygame.display.set_mode(Settings.SCREEN.size)
	pygame.display.set_caption('My Garden')
	timer = pygame.time.Clock()
	events = Events(screen)

	while True:
		# Обработка событий
		events.check_events()

		# Если произошло событие закрытия окна - Выходим
		if events.CLOSE_EVENT:
			return

		# Заливка экрана
		screen.fill((255, 255, 255))

		# Обновление состояния объектов
		events.update()

		# Обновление окна
		pygame.display.update()
		# 60 FPS
		timer.tick(60)


if __name__ == '__main__':
	main()