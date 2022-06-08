import pygame
from pygame.surface import Surface
import math

class Shield:
	"""Class to visuallize a shield for the ship."""
	def __init__(self, ai_game):
		"""Initialize attributes for shield class."""
		#Init game attributes
		self.settings = ai_game.settings 
		self.screen = ai_game.screen
		self.ship = ai_game.ship
		#Init shield
		self.center = self.ship.rect.center
		self.radius = math.sqrt(2 * math.pow(self.ship.rect.width, 2)) / 2
		#Init shield hitbox
		self.hitbox_color = (255, 0, 0)
		self.hitbox_rect = pygame.Rect(0, 0, 2 * self.radius, self.radius)
		#start functions	
		self._update_hitbox()
		self.update()

	def update(self):
		"""Updates shield position with ship movement."""
		self.center = self.ship.rect.center
		self._update_hitbox()

	def _update_hitbox(self):
		"""Returns Hitbox and position of the shield."""
		self.hitbox_rect.midtop = self.ship.rect.midtop
		self.hitbox_rect.top = self.ship.rect.top -20
		

	def blitme(self):
		"""Draws shield on screen."""
		pygame.draw.rect(self.screen, self.hitbox_color, self.hitbox_rect, 1)
		pygame.draw.circle(self.screen,
						self.settings.shield_color,
						self.center,
						self.radius,
						5,
						True, True, False, False)


		
		
		
