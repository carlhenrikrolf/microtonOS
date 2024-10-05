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
from utils import Outport, Inport

print('Färdig.')
