class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		#Ship settings
		self.ship_limit = 3
		#Shield settings
		self.shield_limit = 1
		self.shield_color = (0, 0, 255)
		#Bullet settings
		self.bullet_width = 3440
		self.bullet_height = 15
		self.bullet_color = (31, 81, 255)
		self.bullets_allowed = 10
		#Difficulty settings (factor for game start)
		self.lvl_easy = 0.5
		self.lvl_medium = 1.0
		self.lvl_hard = 20
		#Alien settings
		self.fleet_drop_speed = 5
		#How quickly the game speeds up
		self.speedup_scale = 1.1
		#How quickly the alien point values increase
		self.score_scale = 1.5
		self.initialize_dynamic_settings(lvl_difficulty = self.lvl_medium)

	def initialize_dynamic_settings(self, lvl_difficulty):
		"""Initialize settings that change throughout the game."""
		#sip settings (dynamic)
		self.ship_speed = 1.5 * lvl_difficulty
		#bullet settings (dynamic)
		self.bullet_speed = 3.0 * lvl_difficulty
		#alien settings (dynamic)
		self.alien_speed = 1.0 * lvl_difficulty
			#scoring
		self.alien_points = 50 * lvl_difficulty
		#fleet direction (dynamic)
		#orientation 1 == right, -1 == left
		self.fleet_direction = 1

	def increase_speed(self):
		"""Increase speed settings amd alien point values."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)

