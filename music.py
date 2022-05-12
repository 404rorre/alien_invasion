import pygame

class Music():
	"""Class for playing music inside the game."""
	def __init__(self,ai_game):
		"""Initializing music parameters."""
		#Needed for playing music
		pygame.init()
		self.title_list = {
			0: "music/game_music.mp3"
			}

	def play(self, title = 0):
		pygame.mixer.music.load(self.title_list[title])
		pygame.mixer.music.play()

	def stop(self, title = 0):
		pygame.mixer.music.stop()


		