import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
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
		#Create an instance to store game statistics
			#and a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		#Initializing objects
		self.ship = Ship(self)
		self.aliens = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		#system flags
		self.exit_game = False
		#Functions
		self._create_fleet()
		#Initializing buttons.
		self.play_button = Button(self, "Play")
		self.button_lvl_easy = Button(self, "Easy", "topleft")
		self.button_lvl_medium = Button(self, "Medium", "midleft")
		self.button_lvl_hard = Button(self, "Hard", "bottomleft")
		#Initializing music.
		self.music = Music()

	def run_game(self):
		"""Start the main loop for the game."""
		self.music.play()
		while True:
			self._check_events()

			if self.stats.game_active and self.stats.game_lvl:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()			

	def _check_events(self):
		"""Respond to keypress and mousevents."""
		#Watch for keyboard and mouse events.
		for event in pygame.event.get():				
				self._check_keydown_events(event)
				self._check_keyup_events(event)
				self._check_close_game(event)
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					if not self.stats.game_active:
						self._check_play_button(mouse_pos)
					if self.stats.game_active and not self.stats.game_lvl:
						self._get_game_difficulty(mouse_pos)

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
			if event.key == pygame.K_p and not self.stats.game_active:
				self._start_game()
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

	def _check_play_button(self, mouse_pos):
		"""Checks if button was clicked."""
		if (self.play_button.rect.collidepoint(mouse_pos) and 
			not self.stats.game_active):
			self.stats.game_active = True

	def _start_game(self):
		"""
		Script to start game after clicking on the 'start'-button
		or pressing 'p'.
		"""
		#Reset the game statistics.
		self.stats.reset_stats()
		self.stats.game_active = True
		self.sb.prep_score()
		self.sb.prep_lvl()
		self.sb.prep_ships()
		self.stats.game_lvl = True
		#Get rid of any remaining aliens and bullets.
		self.aliens.empty()
		self.bullets.empty()
		#create new fleet and reset ship position
		self._create_fleet()
		self.ship.center_ship()
		#Hide the mouse cursor.
		pygame.mouse.set_visible(False)
		
	def _update_screen(self):
		"""Update images on the screen and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		self._draw_bullets()
		self.aliens.draw(self.screen)
		#Draw the score information
		self.sb.show_score()
		#Draw the button if the game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()
		if self.stats.game_active and not self.stats.game_lvl:
			self.button_lvl_easy.draw_button()
			self.button_lvl_medium.draw_button()
			self.button_lvl_hard.draw_button()
		#Make the most recently drawn screen visible.
		pygame.display.flip()			

	def _get_game_difficulty(self, mouse_pos):
		"""
		Shows difficulty buttons and returns difficulty level to start with.
		"""
		if (self.button_lvl_easy.rect.collidepoint(mouse_pos) and 
			not self.stats.game_lvl):
			self.stats.game_lvl = self.settings.lvl_easy
			print("easy")
		if (self.button_lvl_medium.rect.collidepoint(mouse_pos) and 
			not self.stats.game_lvl):
			self.stats.game_lvl = self.settings.lvl_medium
			print("medium")
		if (self.button_lvl_hard.rect.collidepoint(mouse_pos) and 
			not self.stats.game_lvl):
			self.stats.game_lvl = self.settings.lvl_hard
			print("hard")

		#Starts game after diffculty level is choosen
		#& Resets settings to choosen level
		if self.stats.game_lvl:
			self.settings.initialize_dynamic_settings(self.stats.game_lvl)
			self._start_game()	

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
		self._check_bullet_alien_collision()
		#Check if alien group is empty
		if not self.aliens:
			#Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			#Increas level.
			self.stats.lvl += 1
			self.sb.prep_lvl()

	def _draw_bullets(self):
		"""Simple functions to draw bullets on screen."""
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
 
	def _check_bullet_alien_collision(self):
		"""Respond to bullet-alien collision."""
		#Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

	def _create_fleet(self):
		"""Create the fleet of aliens."""
		#Check rect parameters of the alien
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		#Find the number of aliens in a row.
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)
		#Find the number of aliens in a line.
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) 
							- ship_height)
		number_rows = available_space_y // (2 * alien_height)
		#Create the full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Simple method to add more aliens in a row."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.y = alien_height + 2 * alien_height * row_number
		alien.rect.y = alien.y
		self.aliens.add(alien)

	def _update_aliens(self):
		"""
		Check if the fleet is at an edge,
		then ipdate the position of all alien in the fleet.
		"""
		self._check_fleet_edges()
		self.aliens.update()

		#Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
					self._ship_hit()
		#Look for aliens hitting the bottom of the screen.
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if the ships got hit.
				self._ship_hit()
				break

	def _ship_hit(self):
		"""Respond to the ship being hit by an alien."""
		self.stats.ships_left -= 1
		self.sb.prep_ships()
		if self.stats.ships_left > 0:
			#Decrement ships_left.
			#Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()
			#Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()
			#Pause
			sleep(0.5)

		else:
			self.stats.game_active = False
			self.stats.game_lvl = None
			#Show mouse cursor again
			pygame.mouse.set_visible(True)

	def _check_fleet_edges(self):
		"""Respond apporpriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		self.settings.fleet_direction *= -1
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed

if __name__ == "__main__":
	#Make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()