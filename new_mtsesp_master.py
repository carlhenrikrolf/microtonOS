#! /home/pi/.venv/bin/python3

# parameters
client_name = 'MTS-ESP Master'

# modules
import mido
import mtsespy as mts
import numpy as np
import threading
import time
from midi_implementation.exquis import exquis as xq
from utils import Outport, Inport, make_threads

class BaseTuning:
	
	concert_a_frequency = 440.0
	concert_a_key = 69
	middle_c = concert_a - 9
	white_keys = [0, 2, 4, 5, 7, 9, 11]
	black_keys = [1, 3, 6, 8, 10]
	key_switches = range(0, 24)
	foot_switch = 64
	
	white = None
	black = None
	alternating = False
	self.frequencies = None
	self.tuning_name = 'Unnamed'
	
	def color_keys(self):
		 raise Warning('color_keys must be defined in child class')
	
	def reset(self,
		mts.set_note_tunings(self.frequencies)
		mts.set_scale_name(self.tuning_name)
		self.color_keys()
		
	def equal_step_tuning(self, steps=12, numerator=2, denominator=1):
		frequencies = [self.concert_a_frequency]*128
		for note in range(128):
			frequencies[note] *= (numerator/denominator)**((note-self.concert_a)/steps
		return frequencies
		


# different classes of tunings
class Default(BaseTuning): # only 12edo

	self.white = xq.white
	self.black = xq.blank
	
	def __init__(self):
		...
			 
class Micro(BaseTuning): # e.g. 17edo, 19edo, 22edo, 24edo, 29edo, 31edo
	
	self.white = xq.red
	self.black = xq.blank
	
	def __init__(self,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		...
	
class Macro(BaseTuning): # e.g. 5edo, 7edo, 9edo, 13ed3
	
	self.white = xq.lime
	self.black = xq.cyan
	self.alternating = True
	
	def __init__(self,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		...

# the below are considered 'uneven' for now
class Partial(BaseTuning): # e.g. 48edo, 53edo
	
	self.white = xq.magenta
	self.black = xq.blue
	
	def __init__(self,
		is_deleted: list,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		...
	
class Ombak(BaseTuning): # e.g. 7edo-ombak, 5edo+ombak
	
	self.white = xq.magenta
	self.black = xq.blue
	self.alternating = True
	
	def __init__(self,
		odd: float,
		even: float,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		...
	
class Octave(BaseTuning): # e.g. Pythagorean, 7 notes from Wendy Carlos's harmonic scale
	
	self.white = xq.magenta
	self.black = xq.blue
	
	def __init__(self,
		frequencies: [float]*12,
		is_filtered=[False]*12,
		):
		...
	
class Arbitrary(BaseTuning): # e.g. the harmonic series
	
	self.white = xq.blank
	self.black = xq.blank
	
	def __init__(self,
		frequencies: [float]*128,
		is_filtered=[False]*128,
		):
		...
		
def to_cents(ratio):
	return 1200*np.log(ratio)/np.log(2)
	
def equal_step_tuning(steps=12, numerator=2, denominator=1):
	equave = [0.0]*steps
	ratio = 1
	for step in range(steps):
		equave = to_cents(ratio)
		ratio *= (numerator/denominator)**(1/steps)
		
def pythagorean(steps=12):
	octave = [0.0]*steps
	ratio = 1
	for tone in range(steps):
		octave[tone] = to_cents(ratio)
		if tone % 2 == 0:
			ratio *= 3/2
		else:
			ratio /= 4/3
	return octave
	
harmonic_series = [to_cents(i+1) for i in range(128)]
