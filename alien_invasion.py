import sys
import pygame
from settings import Settings
from ship import Ship
from music import Music
from bullet import Bullet

class AlienInvasion:
	"""Overall class to manage games assets and behaviour."""

	def __init__(self):
		"""Initialize the game, an create game ressources."""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode(
					(0,0),pygame.FULLSCREEN
					)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.music = Music()
		#system flags
		self.exit_game = False

	def run_game(self):
		"""Start the main loop for the game."""
		self.music.play()
		while True:
			self._check_events()
			self.ship.update()
			self.bullets.update()
			#Get rid of bullets that have disappeared.
			for bullet in self.bullets.copy():
				if bullet.rect.bottom <= 0:
					self.bullets.remove(bullet)
				print(len(self.bullets))
			self._update_screen()			

	def _check_events(self):
		"""Respond to keypress and mousevents."""
		#Watch for keyboard and mouse events.
		for event in pygame.event.get():
				self._check_close_game(event)
				self._check_keydown_events(event)
				self._check_keyup_events(event)
	
	def _update_screen(self):
		"""Update images on the screen and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		#Make the most recently drawn screen visible.
		pygame.display.flip()

	def _check_close_game(self, event):
		"""Respond to exit game."""
		if event.type == pygame.QUIT:
			self.exit_game =True
		if self.exit_game:
			self.music.stop()
			sys.exit()

	def _check_keydown_events(self, event):
		"""Respond to key press."""
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				#Move the ship to the right.
				self.ship.moving_right = True
			if event.key == pygame.K_LEFT:
				#Move the ship to the left.
				self.ship.moving_left = True
			if event.key == pygame.K_q:
				self.play_music = False
				self.exit_game = True
			if event.key == pygame.K_SPACE:
				self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Respond to key release."""
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				#stops the ship from moving to the right.
				self.ship.moving_right = False
			if event.key == pygame.K_LEFT:
				#stops the ship from moving to the left.
				self.ship.moving_left = False

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		new_bullet = Bullet(self)
		self.bullets.add(new_bullet)

if __name__ == "__main__":
	#Make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()