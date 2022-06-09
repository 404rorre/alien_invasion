import pygame
from pygame.surface import Surface
import math

class Shield:
	"""Class to visuallize a shield for the ship."""
	def __init__(self, ai_game):
		"""Initialize attributes for shield class."""
		#Init game attributes
		self.settings = ai_game.settings 
		self.stats = ai_game.stats
		self.screen = ai_game.screen
		self.ship = ai_game.ship
		#Init shield
		self.center = self.ship.rect.center
		self.radius = math.sqrt(2 * math.pow(self.ship.rect.width, 2)) / 2
		"""
		ALWAYS ALWAYS ALWAYS!!!!
		A CLASS WHICH SHOULD COLLIDE WITH ANOTHER RECTANGLE NEEDS A VARIABLE
		CALLED 'self.rect' !!!
		THIS VARIABLE WILL OVERWRITE THE SHELL ATTRIBUTE IN PYGAME.
		OTHERWISE THERE WILL BE AN EXCEPTION!!!
		"""
		#Init shield hitbox
		self.hitbox_color = (255, 0, 0)
		self.hitbox = pygame.Rect(0, 0, 2 * self.radius, self.radius)
		self.rect = self.hitbox
		#start functions	
		self._update_hitbox()
		self.update()

	def update(self):
		"""Updates shield position with ship movement."""
		self.center = self.ship.rect.center
		self._update_hitbox()

	def _update_hitbox(self):
		"""Returns Hitbox and position of the shield."""
		self.rect.midtop = self.ship.rect.midtop
		self.rect.top = self.ship.rect.top -20
		

	def blitme(self):
		"""Draws shield on screen."""
		if self.stats.shields_left > 0:
			#pygame.draw.rect(self.screen, self.hitbox_color, self.hitbox, 1)
			pygame.draw.circle(self.screen,
							self.settings.shield_color,
							self.center,
							self.radius,
							5,
							True, True, False, False)


		
		
		
