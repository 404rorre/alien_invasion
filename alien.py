import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to represent a single alien in the fleet."""
	def __init__(self, ai_game):
		#Initialization of superclass Sprite
		super().__init__()
		#copy variables from the Instance ai_game (class AlienInvasion)
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()
		#get alien picture and rect
		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()
		#Start each new alien near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height 
		#Store the alien's exact horizontal position.
		self.x = float(self.rect.x)


