# -*- coding: utf-8 -*-

import pygame
import Settings


class Camera(pygame.sprite.LayeredUpdates):
	def __init__(self, target, world_size):
		super().__init__()
		self.target = target
		self.world_size = world_size
		self.cam = pygame.Vector2(0, 0)
		if self.target:
			self.add(target)


	def update(self, *args):
		super().update(*args)
		if self.target:
			x = -self.target.rect.center[0] + Settings.BLOCK_SIZE[0]/2
			y = -self.target.rect.center[1] + Settings.BLOCK_SIZE[1]/2

			self.cam += (pygame.Vector2((x, y)) - self.cam) * .05
			self.cam.x = max(-(self.world_size[0] - Settings.WIN_SIZE[0]), min(0, self.cam.x))
			self.cam.y = max(-(self.world_size[1] - Settings.WIN_SIZE[1]), min(0, self.cam.y))


	def draw(self, surface):
		spritedict = self.spritedict
		surface_blit = surface.blit
		dirty = self.lostsprites
		self.lostsprites = []
		dirty_append = dirty.append
		init_rect = self._init_rect
		for spr in self.sprites():
			rec = spritedict[spr]
			newrect = surface_blit(spr.image, spr.rect.move(self.cam))
			if rec is init_rect:
				dirty_append(newrect)
			else:
				if newrect.colliderect(rec):
					dirty_append(newrect.union(rec))
				else:
					dirty_append(newrect)
					dirty_append(rec)
			spritedict[spr] = newrect
		return dirty