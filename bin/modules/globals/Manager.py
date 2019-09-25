# -*- coding: utf-8 -*-

from bin.modules.globals.Loading import Loading
from bin.modules.globals.Loading import UserFiles


"""
Determining the state of the window
0 - MainMenu
1 - Create user files
2 - GamePlay
"""
class _Status(object):
	def __init__(self):
		self.__value = 0


	def set_value(self, val, *args, **kwargs):
		self.__value = val
		return Loading(*args, **kwargs)


	def get_value(self):
		return self.__value


STATUS = _Status()