import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from music import Music

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
		self.aliens = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.music = Music()
		#system flags
		self.exit_game = False
		#functions
		self._create_fleet()

	def run_game(self):
		"""Start the main loop for the game."""
		self.music.play()
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()			

	def _check_events(self):
		"""Respond to keypress and mousevents."""
		#Watch for keyboard and mouse events.
		for event in pygame.event.get():				
				self._check_keydown_events(event)
				self._check_keyup_events(event)
				self._check_close_game(event)

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

	def _check_close_game(self, event):
		"""Respond to exit game."""
		if event.type == pygame.QUIT:
			self.exit_game =True
		if self.exit_game:
			self.music.stop()
			sys.exit()
	
	def _update_screen(self):
		"""Update images on the screen and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		self._draw_bullets()
		self.aliens.draw(self.screen)
		#Make the most recently drawn screen visible.
		pygame.display.flip()

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get reid of old bullets"""
		#Update bullet position.
		self.bullets.update()
		#Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

	def _draw_bullets(self):
		"""Simple functions to draw bullets on screen."""
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

	def _create_fleet(self):
		"""Create the fleet of aliens."""
		#Max Nr. Aliens in a row
		number_aliens_x = self._get_number_aliens_x()
		#Create first row of aliens.
		for alien_number in range (number_aliens_x):
			self._create_alien(alien_number)

	def _create_alien(self, alien_number):
		"""Simple method to add more aliens."""
		alien = Alien(self)
		alien_width = alien.rect.width
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		self.aliens.add(alien)

	def _get_number_aliens_x(self):
		"""Simple method to return max horizontal Nr.'s of aliens."""
		#Create an alien and find the number of aliens in a row.
		alien = Alien(self)
		alien_width = alien.rect.width
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)
		return number_aliens_x



	

			





if __name__ == "__main__":
	#Make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()