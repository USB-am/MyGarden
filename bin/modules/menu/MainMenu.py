# -*- coding: utf-8 -*-

import pygame
import os, sys

# My Modules
# from bin.modules.globals import Loading
from bin.modules.globals import Manager


# Returned folder with 'step' move back
def backdir(path, step):
	step = abs(step) * -1
	return '\\'.join(path.split('\\')[:step])


class MainMenu(object):
	def __init__(self, master, mouse):
		self.master = master							# Parent window
		self.mouse = mouse								# Cursor module
		self.widget_list = []							# List with widget names
		self.widgets = {}								# {name : image-object}

		''' Text font '''
		self.menu_font = pygame.font.Font(
			backdir(os.path.dirname(__file__), 2) + '\\fonts\\times.ttf',
			20
		)
		w, h = pygame.display.get_surface().get_size()	# Parent window sizes

		''' Widgets sizes '''
		self.size = {
			'bg' : (int(w), int(h)),
			'logo' : (int(w*.6), int(h*.15)),
			'button' : (int(w*.6), int(h*.2))
		}

		''' Widgets positions '''
		self.position = {
			'bg' : (0, 0),
			'logo' : (w*.2, h*.01),
			'button' : [
				(int(w*.2), int(h*.17)),
				(int(w*.2), int(h*.38)),
				(int(w*.2), int(h*.59)),
				(int(w*.2), int(h*.80))
			]
		}

		self.initUI()


	def initUI(self):
		''' Background image '''
		bg = pygame.image.load(os.path.dirname(__file__) + '\\images\\1-bg.jpg')
		self.widgets.setdefault('bg', pygame.transform.scale(bg, self.size['bg']))
		self.widget_list.append('bg')

		''' Logo text '''
		logo = self.menu_font.render('My Garden', False, (255, 255, 255))
		self.widgets.setdefault('logo', pygame.transform.scale(logo, self.size['logo']))
		self.widget_list.append('logo')

		''' Button image '''
		button = pygame.image.load(os.path.dirname(__file__) + '\\images\\2-button.png')
		self.widgets.setdefault('button', pygame.transform.scale(button, self.size['button']))
		self.widget_list.append('button')
		# Light version
		self.light_button = pygame.image.load(os.path.dirname(__file__) + '\\images\\2-button_light.png')
		self.light_button = pygame.transform.scale(self.light_button, self.size['button'])


	# Show interface
	def run(self):
		for widget in self.widget_list:
			''' If for widget 1 position: '''
			if not isinstance(self.position[widget], list):
				''' Show widget on him position '''
				self.master.blit(self.widgets[widget], self.position[widget])
			else:
				''' Get all widget positions '''
				for num, pos in enumerate(self.position[widget]):
					texts = ('New game', 'Load game', 'Options', 'Exit')
					'''
					Check all position with cursor.position.
					If cursor.position on widget:
						Draw ligth button
					Else:
						Draw default button
					'''
					if self.check_guidance(self.mouse.x, self.mouse.y, widget, num):
						self.master.blit(self.light_button, pos)
					else:
						self.master.blit(self.widgets[widget], pos)

					''' Create text widget '''
					temp_text = self.menu_font.render(texts[num], False, (255, 255, 255))
					''' Draw text '''
					self.master.blit(temp_text, (
						pos[0] + self.size[widget][0]/2 - self.menu_font.size(texts[num])[0]/2,
						pos[1] + self.size[widget][1]/2 - self.menu_font.size(texts[num])[1]/2)
					)


	def check_guidance(self, x, y, widget, num):
		'''
		x, y = cursor.position
		widget = widget.name
		num = index of internal position entry
		'''
		bx, by = self.position[widget][num]
		for _ in self.position[widget]:
			if x >= bx and x <= bx + self.size[widget][0] and \
				y >= by and y <= by + self.size[widget][1]:
				return True
		return False


	# Check on press LeftMouseButton
	def mouse_press(self, pos):
		'''
		pos = cursor.position
		'''
		for num, btn_pos in enumerate(self.position['button']):
			if self.check_guidance(*pos, 'button', num):
				if num == 0:									# New game
					return Manager.STATUS.set_value(1)
				elif num == 1:									# Load game
					print('You load old game')
				elif num == 2:									# Options
					print('You open options')
				elif num == 3:									# Exit
					sys.exit()