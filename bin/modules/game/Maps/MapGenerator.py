# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import os
from random import randint # TEMP
# My modules
# from .. import Setting


# BLOCK_SIZE = Settings.BLOCK_SIZE
BLOCK_SIZE = (50, 50)
# PATH = Settings.PATH_TO_TEXTURES
PATH = r'D:\Site\Python\Games\My_Garden\bin\modules\game\images\textures'


class Map(tk.Frame):
	def __init__(self, parent, **options):
		super().__init__(parent, **options)

		self.scr_y_canv = tk.Scrollbar(self, orient=tk.VERTICAL)
		self.scr_x_canv = tk.Scrollbar(self, orient=tk.HORIZONTAL)
		self.canv = tk.Canvas(self)

		self.canv['yscrollcommand'] = self.scr_y_canv.set
		self.canv['xscrollcommand'] = self.scr_x_canv.set

		self.scr_y_canv['command'] = self.canv.yview
		self.scr_y_canv.pack(side='right', fill='y')
		self.scr_x_canv['command'] = self.canv.xview
		self.scr_x_canv.pack(side='bottom', fill='x')
		self.canv.pack(side='left', fill='both', expand=tk.ON)


class Instruments(tk.Frame):
	def __init__(self, parent, **options):
		super().__init__(parent, **options)

		self.notebook = ttk.Notebook(self)
		self.notebook.pack(side='left', fill='both', expand=tk.ON)

		relief = ttk.Frame(self.notebook)
		self.fill_relief_frame(relief)
		self.notebook.add(relief, text='Relief')

		interactive_objects = ttk.Frame(self.notebook)
		self.fill_interactive_objects(interactive_objects)
		self.notebook.add(interactive_objects, text='Objects')


	def fill_relief_frame(self, frame):
		scr_y_reliefs = tk.Scrollbar(frame, orient=tk.VERTICAL)
		canv = tk.Canvas(frame, yscrollcommand=scr_y_reliefs.set)
		scr_y_reliefs['command'] = canv.yview
		scr_y_reliefs.pack(side='right', fill='y')
		canv.pack(side='left', fill='both', expand=tk.ON)

		max_col = 8
		now_col = 0
		now_row = 0
		button_count = 51
		size = canv.winfo_reqwidth() // max_col

		for i in range(1, button_count):
			color = '#' + ''.join([str(randint(0, 9)) \
				for x in range(6)])
			tk.Button(canv, text=str(i), bg=color).grid(
				row=now_row, column=now_col, sticky='WE')

			now_col += 1
			if now_col >= max_col:
				now_col = 0
				now_row += 1


	def fill_interactive_objects(self, frame):
		textures = [file for file in os.listdir(PATH) \
			if os.path.isfile(PATH + '\\' + file)]

		scr_y_objects = tk.Scrollbar(frame, orient=tk.VERTICAL)
		canv = tk.Canvas(frame, yscrollcommand=scr_y_objects.set)
		scr_y_objects['command'] = canv.yview
		scr_y_objects.pack(side='right', fill='y')
		canv.pack(side='left', fill='both', expand=tk.ON)

		max_col = 6
		now_col = 0
		now_row = 0
		button_count = len(textures)
		size = canv.winfo_reqwidth() // max_col

		for i in range(1, button_count):
			color = '#' + ''.join([str(randint(0, 9)) \
				for x in range(6)])
			image = tk.PhotoImage(PATH + '\\' + textures[i])
			tk.Button(canv, width=size, height=size, text=str(i),
				image=image, command=lambda e: print()
				).grid(row=now_row, column=now_col, sticky='WE')

			now_col += 1
			if now_col >= max_col:
				now_col = 0
				now_row += 1


class UI(tk.Tk):
	def __init__(self, size):
		super().__init__()
		self.title('MapGenerator')
		# self.geometry('+100+50')
		self.geometry('+50+350')

		self.size = size
		self.map_array = np.full(self.size, 0) # , dtype=____)

		self.scroll_panel = tk.PanedWindow(self, orient=tk.HORIZONTAL)
		self.scroll_panel.pack(side='left', fill='both', expand=tk.ON)

		self.main_canv = Map(
			self.scroll_panel,
			width = size[0] * BLOCK_SIZE[0],
			height = size[1] * BLOCK_SIZE[1],
			bg = 'lightgrey'
		)
		self.main_canv.bind_all('<Button-1>', self.set_object)
		self.scroll_panel.add(self.main_canv)
		self.instruments = Instruments(self.scroll_panel, bg='black')
		self.scroll_panel.add(self.instruments)


	def set_object(self, event):
		print(
			'X:', event.x // BLOCK_SIZE[0],
			'\tY:', event.y // BLOCK_SIZE[1]
		)


def main():
	ui = UI((50, 50))
	ui.mainloop()


if __name__ == '__main__':
	main()