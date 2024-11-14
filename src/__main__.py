# if there is no broad menu, then menu could be divided across several instruments.

from colour import Color
import mido
from menu import Sounds
from utils import Inport, Outport, make_threads
from settings import init_engine
from midi_implementation.dualo import exquis as xq
from midi_implementation.yamaha import reface_cp as cp

client_name = 'microtonOS'

class Script:

	def __init__(self):
		
		self.exquis_is_init = True
		self.engine = init_engine
		self.bank = 0
		self.pgm = 0

	
	def open_outport(self, name):
		try:
			self.outport = mido.open_output('to '+name+' Wrapper')
		except:
			self.outport = mido.open_output()
		

	def exquis(self, msg):
		
		if self.exquis_is_init:
			xq.send(to_exquis, xq.sysex(xq.color_button, xq.sounds, sounds.base_color))	
			for menu_button in [xq.settings, xq.record, xq.tracks, xq.scenes, xq.play_stop]:
				xq.send(to_exquis, xq.sysex(xq.color_button, menu_button, xq.to_color(Color('black'))))	
			self.exquis_is_init = False
			self.open_outport(self.engine)
		
		if sounds.onoff(msg) is True:
			self.engine, self.bank, self.pgm = sounds.select(msg)
		elif sounds.onoff(msg) is False:
			print('eng =', self.engine, 'bnk =', self.bank, 'pgm =', self.pgm)
			to_isomorphic.send(msg)
			self.outport.close()
			self.open_outport(self.engine)
			self.outport.send(mido.Message('control_change', control=cc.bank_select, value=self.bank))
			self.outport.send(mido.Message('program_change', value=self.pgm))
		else:
			to_isomorphic.send(msg)
			
			
	def reface_cp(self, msg):
		
		if msg.type == 'control_change':
			msg.channel = 0
			self.outport.send(msg)
		else:
			to_halberstadt.send(msg)
			
		
	def mtsesp_master(self, msg):
		self.outport.send(msg)
		

to_exquis = Outport(client_name, name='Exquis')
to_isomorphic = Outport(client_name, name='Isomorphic')
to_halberstadt = Outport(client_name, name='Halberstadt')
sounds = Sounds(to_exquis)
script = Script()
from_exquis = Inport(script.exquis, client_name, name='Exquis')
from_reface_cp = Inport(script.reface_cp, client_name, name='Reface CP')
from_mtsesp_master = Inport(script.mtsesp_master, client_name, 'MTS-ESP master')
make_threads([from_exquis.open, from_reface_cp.open])

