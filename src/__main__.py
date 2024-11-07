# if there is no broad menu, then menu could be divided across several instruments.

import menu
from utils import Input, Output, make_threads
from midi_implementation.dualo import exquis as xq
from midi_implementation.yamaha import reface_cp as cp

client_name = 'microtonOS'

class Script:

	def __init__(self):
		self.exquis_is_init = True

	def exquis(self, msg):
		
		if self.exquis_is_init:	
			misc.reset()		
			self.exquis_is_init = False
			
		if sounds.onoff(msg):
			engine, bank, pgm = sounds.select(msg)
			print(engine, bank, pgm)
		elif misc.onoff(msg):
			pass
		else:
			to_isomorphic.send(msg)
			
		if sounds.two(msg) is True:
			print('cp on')
		elif sounds.two(msg) is False:
			print('cp off')

	def reface_cp(self, msg):
		pass

to_exquis = Outport(client_name, name='Exquis')
to_isomorphic = Outport(client_name, name='Isomorphic')
sounds = menu.Sounds(to_exquis, two_is_connected=cp.is_connected)
misc = menu.Misc(to_exquis)
script = Script()
from_exquis = Inport(script.exquis, client_name, name='Exquis')
from_reface_cp = Inport(script.reface_cp, client_name, name='Reface CP')
make_threads([from_exquis.open, from_reface_cp.open])

