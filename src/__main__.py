# if there is no broad menu, then menu could be divided across several instruments.

import menu
from midi_implementation.dualo import exquis as xq
from midi_implementation.yamaha import reface_cp as cp


class Script:

	def __init__(self):
		self.exquis_is_init = True

	def exquis(self, msg):
		
		if self.exquis_is_init:
			self.sounds = menu.Sounds(to_exquis, two_is_connected=cp.is_connected)
			self.misc = menu.Misc(to_exquis)
			self.exquis_is_init = False
			
		select_sound = self.sounds.select(msg)
		if select_sound is not None:
			print(self.sounds.engine)
		reface_cp_onoff = self.sounds.two(msg)
		if reface_cp_onoff is True:
			print('cp on')
		elif reface_cp_onoff is False:
			print('cp off')
			
	def reface_cp(self):
		pass


	

