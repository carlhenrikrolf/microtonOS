"""
	microtonOS.
"""

from colour import Color
import mido
from menu import Sounds
from utils import Inport, Outport, make_threads
from settings import engine_banks_pgms
from midi_implementation.midi1 import control_change as cc
from midi_implementation.dualo import exquis as xq
from midi_implementation.yamaha import reface_cp as cp

client_name = 'microtonOS'

class Script:

	def __init__(self):
		
		self.exquis_is_init = True
		self.reopen = False
		self.engine = 0
		self.bank = 0
		self.pgm = 0


	def exquis(self, msg):
		
		if self.exquis_is_init:
			xq.send(to_exquis, xq.sysex(xq.color_button, xq.sounds, sounds.base_color))	
			for menu_button in [xq.settings, xq.record, xq.tracks, xq.scenes, xq.play_stop]:
				xq.send(to_exquis, xq.sysex(xq.color_button, menu_button, xq.to_color(Color('black'))))	
			self.exquis_is_init = False
		
		if sounds.onoff(msg) is True:
			self.engine, self.bank, self.pgm = sounds.select(msg)
			for outport in to_engine:
				outport.send(mido.Message('control_change', control=cc.all_notes_off))
		elif sounds.onoff(msg) is False:
			print('eng =', self.engine, 'bnk =', self.bank, 'pgm =', self.pgm)
			to_isomorphic.send(msg)
			to_engine[self.engine].send(mido.Message('control_change', control=cc.bank_select[0], value=self.bank))
			to_engine[self.engine].send(mido.Message('program_change', program=self.pgm))
		else:
			to_isomorphic.send(msg)

			
	def widi(self, msg):
		to_halberstadt.send(msg)

			
	def reface_cp(self, msg): # this is here in case I want to move the assign pedal here
		to_manual2.send(msg)
			
		
	def mtsesp_master(self, msg):
		to_engine[self.engine].send(msg)
		

to_exquis = Outport(client_name, name='Exquis')
to_isomorphic = Outport(client_name, name='Isomorphic')
to_halberstadt = Outport(client_name, name='Halberstadt')
to_manual2 = Outport(client_name, name='Manual 2')
to_engine = [Outport(client_name, name=engine_banks_pgms[i][0]) for i in range(len(engine_banks_pgms))]
sounds = Sounds(to_exquis)
script = Script()
from_exquis = Inport(script.exquis, client_name, name='Exquis')
from_widi = Inport(script.widi, client_name, name='WiDi')
from_reface_cp = Inport(script.reface_cp, client_name, name='Reface CP')
from_mtsesp_master = Inport(script.mtsesp_master, client_name, 'MTS-ESP master')
make_threads([from_exquis.open, from_reface_cp.open, from_mtsesp_master.open])

