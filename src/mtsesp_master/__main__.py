#! /home/pi/.venv/bin/python3
#! /home/pi/microtonOS/.venv/bin/python3

"""
	MTS-ESP Master.
	Works with genereric midi controllers with the Halberstadt layout.
	Assumes 5 octaves, and for some functionalities, pedals,
	namely sustain, hold, sostenuto, soft, and expression,
	as well as pitchbend and modulation.
	Furthermore, it assumes the Exquis controller.
	For changing the parameters of tuning with another controller,
	modify encoders.py.
	For changing what kind of isomorphic layouts are possible,
	modify layouts.py
"""

# parameters
client_name = 'New MTS-ESP master'

# imports
import mido
from mtsesp_master.settings import init
from mtsesp_master.encoders import Encoders
from mtsesp_master.active_sensing import ActiveSensing
from utils import Outport, Inport, make_threads

# script
class Script:
	
	def __init__(self):
		
		self.is_init = True
		
		self.equave = init.equave
		self.is_left_right = init.is_left_right
		self.is_up_down = init.is_up_down
		self.transposition = init.transposition
		self.transposition_range = init.transposition_range
		self.n_tunings = init.n_tunings
		self.tuning_pgm = init.tuning_pgm
		self.dilation = init.dilation
		self.dilation_range = init.dilation_range
		self.n_layouts = init.n_layouts
		self.layout_pgm = init.layout_pgm
		
	def run(self, msg):
		
		if self.is_init:
			encoders.reset()
			self.is_init = False
			
		happened, self.equave = encoders.change_equave(msg, self.equave)
		if happened:
			print('ekvav =', self.equave)
			
		happened, self.is_left_right = encoders.flip_left_right(msg)
		if happened:
			print('höger--vänster-speglad är', self.is_left_right)
		happened, self.is_up_down = encoders.flip_up_down(msg)
		if happened:
			print('upp--ner-speglad är', self.is_up_down)
			
		happened, self.transposition = encoders.transpose(msg, self.transposition, self.transposition_range)
		if happened:
			print('transponering =', self.transposition)
		happened, self.transposition = encoders.toggle_transposition(msg, self.transposition)
		if happened:
			print('transponering =', self.transposition)
			
		happened, self.tuning_pgm = encoders.tuning_preset(msg, self.tuning_pgm)
		if happened:
			print('stämning =', self.tuning_pgm)
			
		happened, self.dilation = encoders.dilate(msg, self.dilation, self.dilation_range)
		if happened:
			print('utspädning =', self.dilation)
		happened, self.dilation = encoders.toggle_dilation(msg, 3)
		if happened:
			print('utspädning =', self.dilation)
			
		happened, self.layout_pgm = encoders.layout_preset(msg, self.layout_pgm)
		if happened:
			print('layout =', self.layout_pgm)
			
		
		
to_isomorphic = Outport(client_name, name='isomorphic', verbose=False)
encoders = Encoders(to_isomorphic,
	equave=init.equave,
	equave_range=init.equave_range,
	transposition=init.transposition,
	n_tunings=init.n_tunings,
	tuning_pgm=init.tuning_pgm,
	dilation=init.dilation,
	n_layouts=init.n_layouts,
	layout_pgm=init.layout_pgm,
)
active_sensing = ActiveSensing(to_isomorphic)
script = Script()
from_isomorphic = Inport(script.run, client_name, name='isomorphic', verbose=False)
make_threads([from_isomorphic.open, active_sensing.open])
