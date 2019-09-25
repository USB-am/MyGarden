# -*- coding: utf-8 -*-

import pygame
import shelve
import os


# Returned folder with 'step' move back
def backdir(path, step):
	step = abs(step) * -1
	return '\\'.join(path.split('\\')[:step])


class Loading(object):
	def __init__(self, step=1):
		self.step = step										# Iteration step
		self.value = 0											# Start value
		self.finish = 100										# Finish value

		self.w, self.h = pygame.display.get_surface().get_size()		# Parent window size
		''' Background image '''
		bg = pygame.image.load(os.path.dirname(__file__) + '\\images\\Loading\\bg.jpg')
		self.bg = pygame.transform.scale(bg, (self.w, self.h))
		''' Text '''
		self.font = pygame.font.Font(
			os.path.dirname(__file__) + '\\fonts\\times.ttf',
			30
		)
		self.text_loading = self.font.render('Loading', False, (255, 0, 0))	# Text "Loading" on load window


	# # Class is Iterable
	# def __iter__(self):
	# 	return self


	# # Returned next value
	# def __next__(self):
	# 	if self.value >= self.finish:
	# 		raise StopIteration
	# 	current = self.value
	# 	self.value += self.step
	# 	UserFiles(name='Usbam')
	# 	return current


	def run(self, master):
		master.blit(self.bg, (0, 0))
		master.blit(self.text_loading,
			(self.w/2 - self.font.size('Loading')[0]/2,
			 self.h/3 - self.font.size('Loading')[1]/2
			)
		)


# Manager player files
class UserFiles(object):
	def __init__(self, name, status=True):
		self.name = name										# Player name
		'''
		status:
			True - Load game
			False - Create new player
		'''
		if not status:
			self.create_files()
		self._stats = self.load_stats()


	def create_files(self):
		''' Create new folder if not exists '''
		PATH = backdir(os.path.dirname(__file__), 2) + '\\saves\\%s' % self.name
		try:
			os.makedirs(PATH)
		except FileExistsError:
			raise Exception('User is exists!')

		with shelve.open(PATH + '\\farm_widgets') as farm_widgets:
			farm_widgets['home'] = (0, 0)


	def load_stats(self):
		pass