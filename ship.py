import pygame #is needed for the instance of "ai_game"

class Ship:
	"""A class to manage the ship."""
	def __init__(self, ai_game):
		"""Intialize the ship and set its starting position."""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()
		#Load the ship image and get its rect.
		self.image = pygame.image.load("images/ship.bmp")
		self.rect = self.image.get_rect() #uses rectangles values of the ship
		#Start each new ship at the bottom center of the screen.
		self.rect.midbottom = self.screen_rect.midbottom
		#Movement flag
		self.moving_right = False
		self.moving_left = False
		#Store a decimal value for the ship's horizontal position.
		self.x = float(self.rect.x)

	def update(self):
		"""Update the ship's position bases on the movement flag."""
		if self.moving_right:
			self.x += self.settings.ship_speed
		if self.moving_left:
			self.x -= self.settings.ship_speed

		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)