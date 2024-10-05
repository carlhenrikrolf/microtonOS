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
from mtsesp_master.encoders import Encoders
from mtsesp_master.active_sensing import ActiveSensing
from utils import Outport, Inport, make_threads

# script
class Script:
	def __init__(self):
		self.is_init = True
	def run(self, msg):
		if self.is_init:
			encoders.reset()
			self.is_init = False
		left_right = encoders.flip_left_right(msg)
		if left_right is True:
			print('höger-vänster-speglad')
		elif left_right is False:
			print('höger-vänster normal')
		
to_isomorphic = Outport(client_name, name='isomorphic', verbose=False)
encoders = Encoders(to_isomorphic)
active_sensing = ActiveSensing(to_isomorphic)
script = Script()
from_isomorphic = Inport(script.run, client_name, name='isomorphic', verbose=False)
make_threads([from_isomorphic.open, active_sensing.open])
