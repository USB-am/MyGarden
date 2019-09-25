import pygame


WIN_SIZE = (800, 600)
BG_COLOR = (83, 199, 92)
BLOCK_SIZE = (30, 30)
MOVE_SPEED = 5

HERO_MANAGMENT = {
	'up' : pygame.K_w,
	'left' : pygame.K_a,
	'down' : pygame.K_s,
	'right' : pygame.K_d,
	'attack' : pygame.K_SPACE
}