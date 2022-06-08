class Save:
	"""Simple class to store the HighScore."""
	def __init__(self, ai_game):
		#Initializing attributes
		self.game = ai_game
		self.stats = ai_game.stats
		#Initialize path
		self.path_hs = "saves/high_score.txt"

	def hs_save(self):
		"""Simple mehod to save high score to file."""
		high_score = self.stats.high_score
		with open(self.path_hs, "w", encoding = "utf-8") as f:
			f.write(f"{high_score}\n")

	def hs_load(self):
		"""Simple method to load high score from save."""
		try:
			with open(self.path_hs, encoding = "utf-8") as f:
				content = f.read().strip()
			self.stats.high_score = int(content)
			self.game.sb.prep_high_score()
		except FileNotFoundError:
			pass
		
		





