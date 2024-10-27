# if there is no broad menu, then menu could be divided across several instruments.

import menu

class Script:

	def __init__(self):
		self.exquis_is_init = True

	def exquis(self, msg):
		
		if self.exquis_is_init:
			self.sounds = menu.Sounds(to_exquis)
			self.misc = menu.Misc(to_exquis)
			self.exquis_is_init = False
			
		select_sound = self.sounds.select(msg)
		if select_sound:
			print(self.sounds.engine)
			
	def reface_cp(self):
		pass


	

