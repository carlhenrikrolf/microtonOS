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

# utilities
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

# tuning
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
		octave_shift,
		):
		mts.set_note_tunings(self.frequencies**octave_shift)
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
		self.tuning_name = '12edo'
			 
class Micro(BaseTuning): # e.g. 17edo, 19edo, 22edo, 24edo, 29edo, 31edo
	
	self.white = xq.red
	self.black = xq.blank
	
	def __init__(self,
		tuning_name: str,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		if tuning_name is not None:
			self.tuning_name = tuning_name
	
class Macro(BaseTuning): # e.g. 5edo, 7edo, 9edo, 13ed3
	
	self.white = xq.lime
	self.black = xq.cyan
	self.alternating = True
	
	def __init__(self,
		tuning_name: str,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		if tuning_name is not None:
			self.tuning_name = tuning_name

# the below are considered 'uneven' for now
class Subset(BaseTuning): # e.g. 48edo, 53edo
	
	self.white = xq.magenta
	self.black = xq.blue
	
	def __init__(self,
		tuning_name: str,
		is_deleted: list,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		if tuning_name is not None:
			self.tuning_name = tuning_name
	
class Ombak(BaseTuning): # e.g. 7edo-ombak, 5edo+ombak
	
	self.white = xq.magenta
	self.black = xq.blue
	self.alternating = True
	
	def __init__(self,
		tuning_name: str,
		odd: float,
		even: float,
		steps: int,
		numerator: int,
		denominator: int,
		halberstadt_map: list,
		):
		if tuning_name is not None:
			self.tuning_name = tuning_name
	
class Octave(BaseTuning): # e.g. Pythagorean, 7 notes from Wendy Carlos's harmonic scale
	
	self.white = xq.magenta
	self.black = xq.blue
	
	def __init__(self,
		tuning_name: str,
		frequencies: [float]*12,
		is_filtered=[False]*12,
		):
		if tuning_name is not None:
			self.tuning_name = tuning_name
	
class Arbitrary(BaseTuning): # e.g. the harmonic series
	
	self.white = xq.blank
	self.black = xq.blank
	
	def __init__(self,
		tuning_name: str,
		frequencies: [float]*128,
		is_filtered=[False]*128,
		):
		if tuning_name is not None:
			self.tuning_name = tuning_name
		
tunings = [
	Macro('5edo', 5, 2, 1, [None, 0, None, 1, None, None, 2, None, 3, None, 4, None]),
	Macro('7edo', ...),
	Octave('Just7', ...),
	Macro('13ed3', ...),
	Macro('9edo', ...),
	Ombak('5edo+ombak', ...),
	Macro('10edo', ...),
	Default(),
	Octave('Pythagorean', ...),
	Micro('14edo', ...),
	Micro('9ed3/2', ...),
	Micro('17edo', ...),
	Ombak('9edo-ombak', ...),
	Micro('19edo', ...),
	Micro('8ed4/3'), ...),
	Subset('48edo', ...),
	Micro('22edo', ...),
	Subset('53edo', ...),
	Micro('24edo', ...),
	Micro('29edo', ...),
	Micro('31edo', ...),
	Micro('34edo', ...),
	Micro('36edo', ...),
	Arbitrary('Harmonic Series', ...),
	]


