import pygame
from pygame.sprite import Sprite
from settings import Settings

class Alien(Sprite):
	"""A class to represent a single alien in the fleet."""
	def __init__(self, ai_game):
		#Initialization of superclass Sprite
		super().__init__()
		#copy variables from the Instance ai_game (class AlienInvasion)
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()
		#Initialize instance settings
		self.settings = ai_game.settings
		#get alien picture and rect
		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()
		#Start each new alien near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height 
		#Store the alien's exact location.
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def update(self):
		"""Move alien right or left."""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		"""Return True if alien is at edge of the screen."""
		if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
			return True




