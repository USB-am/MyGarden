# -*- coding: utf-8 -*-

import pygame
import shelve
import os, sys

# My modules
from . import Map


# Returned folder with 'step' move back
def backdir(path, step):
	step = abs(step) * -1
	return '\\'.join(path.split('\\')[:step])


class Game(object):
	def __init__(self, name):
		self.name = name


class LoadFiles(object):
	def __init__(self, name=None, master=None):
		print('='*20, '\nStart class "LoadFiles"\n', '='*20, sep='')
		if name is None:
			while True:
				self.name = self.askUserName(master=master)
				try:
					self.create_new_save()
				except OSError:
					continue
		self.name = name
		self.master = master


	def askUserName(self, master=None):
		if master is None:
			raise AttributeError('Master is None')

		print('Start func "askUserName"')
		name = ''

		w, h = pygame.display.get_surface().get_size()

		widgets = []
		font = pygame.font.Font(
		 backdir(os.path.dirname(__file__), 2) + '\\fonts\\times.ttf',
		 20
		)

		bg = pygame.image.load(os.path.dirname(__file__) + '\\images\\input\\bg.jpg')
		bg = pygame.transform.scale(bg, (w, h))
		input_text = [
		 font.render('Enter a character name', False, (0, 0, 0)),
		 (w/2-font.size('Enter a character name')[0]/2, h*.3)
		]
		input_block = pygame.image.load(os.path.dirname(__file__) + '\\images\\input\\table.png')
		table = [pygame.transform.scale(input_block, (int(w*.5), int(h*.6))), (int(w*.25), int(h*.4))]
		name_text = [
		 font.render(name, False, (0, 0, 0)),
		 (w/2-font.size(name)[0]/2, h*.5)
		]

		RUN = True

		while RUN:
			pygame.time.delay(30)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						RUN = False
					if event.key == pygame.K_RETURN:
						print('Your new name: "{}"'.format(name))
						RUN = False
						return name
					elif event.key == pygame.K_BACKSPACE:
						name = name[:-1]
					else:
						if font.size('m'*15)[0] > font.size(name)[0]:
							name += event.unicode

					name_text = [
					 font.render(name, False, (0, 0, 0)),
					 (w/2-font.size(name)[0]/2, h*.5)
					]

				if event.type == pygame.QUIT:
					sys.exit()

			master.blit(bg, (0, 0))
			master.blit(table[0], table[1])
			master.blit(input_text[0], input_text[1])
			master.blit(name_text[0], name_text[1])

			pygame.display.update()

		return name


	def create_new_save(self):
		new_path = backdir(os.path.dirname(__file__), 2) + '\\saves\\{name}'.format(name=self.name)
		if not os.path.exists(new_path):
			os.makedirs(new_path)
		else:
			raise OSError('Dir is {} exists!'.format(new_path))

		with shelve.open(new_path + '\\inventory', flag='n') as inventory:
			inventory['money'] = 10000
			inventory['inventory'] = []
			inventory['state'] = {'gathering': 1, 'fishing': 1}

		with shelve.open(new_path + '\\options') as options:
			options['general_volume'] = 100
			options['volume'] = 100
			options['music'] = 100
			options['language'] = 'EN'

		with shelve.open(new_path + '\\hero') as hero:
			hero['hair'] = 0		# Волосы
			hero['eyes'] = 0		# Глаза
			hero['beard'] = 0		# Борода
			hero['body'] = 0		# Тело
			hero['legs'] = 0		# Ноги
			hero['feet'] = 0		# Стопы

			hero['hat'] = None			# Шляпа
			hero['right_ring'] = None	# Правое кольцо
			hero['left_ring'] = None	# Левое кольцо
			hero['boots'] = None		# Ботинки
