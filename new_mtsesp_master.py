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

## Tuning

# utilities
def to_cents(ratio):
	"""
		Converts a frequency ratio to cents
	"""
	return 1200*np.log(ratio)/np.log(2)
	
def equal_step_tuning(steps=12, numerator=2, denominator=1):
	"""
		Produces a <steps> equally divided <numerator>/<denominator> tuning.
		Output is one equave in cents starting at 0.0 cents.
	"""
	equave = [0.0]*steps
	ratio = 1
	for step in range(steps):
		equave[step] = to_cents(ratio)
		ratio *= (numerator/denominator)**(1/steps)
	return equave
		
def pythagorean(steps=12):
	"""
		Produces a Pythagorean tuning.
		Default is 12 steps per octave.
		Output is one octave in intervals.
	"""
	octave = [0.0]*steps
	ratio = 1
	for tone in range(steps):
		octave[tone] = ratio
		if tone % 2 == 0:
			ratio *= 3/2
		else:
			ratio /= 4/3
	return octave

# tuning
class BaseTuning:
	
	concert_a_frequency = 440.0
	concert_a_key = 69
	middle_c = concert_a - 9
	white_keys = [0, 2, 4, 5, 7, 9, 11]
	black_keys = [1, 3, 6, 8, 10]
	key_switches = range(0, 24)
	foot_switch = 64
	
	# the manuals have a sparser set of notes and may require more than 128 notes,
	# hence they are spread out over 3 channels, which would still be more than 7 octaves for 53edo.
	master_channel = 0
	exquis_master = 0
	member_channels = range(1,16)
	exquis_members = range(1,10)
	lower_manual_channels = [10, 11, 12]
	lower_manual_main = lower_manual_channels[1]
	upper_manuals_channels = [13, 14, 15]
	upper_manual_main = upper_manual_channels[1]
	
	
	white = None
	black = None
	alternating = False
	self.frequencies = None
	self.tuning_name = 'Unnamed'
	
	def reset_lower_manual(self):
		raise Warning('reset_lower_manual must be defined in child class')
	
	def reset_upper_manual(self):
		raise Warning('reset_upper_manual must be defined in child class')
	
	def color_keys(self):
		 raise Warning('color_keys must be defined in child class')
	
	def reset(self,octave_shift=0,reset_switches=False):
		"""
			Resets the tuning.
		"""
		mts.set_note_tunings(self.frequencies**octave_shift)
		mts.set_scale_name(self.tuning_name)
		if reset_switches:
			self.reset_lower_manual()
			self.reset_upper_manual()
		self.color_keys()
		
	def default_args(self, tuning_name, lower_manual=None, upper_manual=None):
		if tuning_name is not None:
			self.tuning_name = tuning_name
		if lower_manual is not None:
			if upper_manual is not None:
				self.upper_manual = upper_manual
			else:
				self.upper_manual = lower_manual
		
	def remap_exquis(self, msg):
		raise Warning('remap_exquis must be defined in child class')
		
	def remap_lower_manual(self, msg):
		raise Warning('remap_lower_manual must be defined in child class')
	
	def remap_upper_manual(self, msg):
		raise Warning('remap_upper_manual must be defined in child class')
		
	def dispatch_exquis(self, msg):
		"""
			Dispatches incoming channels from Exquis to another set of channels.
		"""
			...
			return msg
			
	def dispatch_lower_manual(self, msg):
		"""
			Splits incoming lower manual to several channels.
		"""
			...
			return msg
			
	def dispatch_upper_manual(self, msg)
		"""
			Splits incoming upper manual to several channels.
		"""
			...
			return msg
			
	def merge_channels(self, msg): # This will necessitate that I put it in a separate file. Maybe should also apply to layouts?
		"""
			Merges the channels such that only 1, 2, 3 are in use.
			Useful for setBfree or other synths that are not 'omni'
		"""
			if hasattr(msg, 'channel'):
				if msg.channel == self.master_channel or msg.channel in self.member_channels:
					msg.channel = 0
				elif msg.channel in self.lower_manual_channels:
					msg.channel = 1
				elif msg.channel in self.upper_manuals_channels:
					msg.channel = 2
			return msg		


# different classes of tunings
class Default(BaseTuning): # only 12edo

	self.white = xq.white
	self.black = xq.blank
	
	def __init__(self):
		self.default_args('12edo')
			 
class Micro(BaseTuning): # e.g. 17edo, 19edo, 22edo, 24edo, 29edo, 31edo
	
	self.white = xq.red
	self.black = xq.blank
	
	def __init__(self,
		tuning_name: str,
		steps: int,
		numerator: int,
		denominator: int,
		lower_manual: list,
		upper_manual=None,
		):
		self.default_args(tuning_name, lower,_manual, upper_manual)
	
class Macro(BaseTuning): # e.g. 5edo, 7edo, 9edo, 13ed3
	
	self.white = xq.lime
	self.black = xq.cyan
	self.alternating = True
	
	def __init__(self,
		tuning_name: str,
		steps: int,
		numerator: int,
		denominator: int,
		lower_manual: list,
		upper_manual=None,
		):
		self.default_args(tuning_name, lower,_manual, upper_manual)

# the below are considered 'uneven' for now
class Subset(BaseTuning): # e.g. 48edo, 53edo
	
	self.white = xq.magenta
	self.black = xq.blue
	
	def __init__(self,
		tuning_name: str,
		is_deleted: list, # is kept? subset, set
		steps: int,
		numerator: int,
		denominator: int,
		lower_manual: list,
		upper_manual=None,
		):
		self.default_args(tuning_name, lower,_manual, upper_manual)
	
class Ombak(BaseTuning): # e.g. 7edo-ombak, 5edo+ombak
	
	self.white = xq.magenta
	self.black = xq.blue
	self.alternating = True
	
	def __init__(self,
		tuning_name: str,
		even: float,
		odd: float,
		steps: int,
		numerator: int,
		denominator: int,
		lower_manual: list,
		upper_manual=None,
		):
		self.default_args(tuning_name, lower_manual, upper_manual)
	
class Octave(BaseTuning): # e.g. Pythagorean, 7 notes from Wendy Carlos's harmonic scale
	
	self.white = xq.magenta
	self.black = xq.blue
	
	def __init__(self,
		tuning_name: str,
		frequencies: [float]*12,
		is_filtered=[False]*12,
		):
		self.default_args(tuning_name)
	
class Arbitrary(BaseTuning): # e.g. the harmonic series
	
	self.white = xq.blank
	self.black = xq.blank
	
	def __init__(self,
		tuning_name: str,
		frequencies: [float]*128,
		is_filtered=[False]*128,
		):
		self.default_args(tuning_name)
		
class Custom(BaseTuning):
	
	self.white = xq.blank
	self.black = xq.white
	
	def __init__(self,
		steps,
		numerator,
		denominator,
		):
		self.default_args('Custom')
		
tunings = [
	Macro('5edo', 5, 2, 1, [None, 0, None, 1, None, None, 2, None, 3, None, 4, None], concert_a_frequency=440.0*2**(1/5)),
	Macro('7edo', 7, 2, 1, [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6]),
	Octave('Just7', [1, None, 9/8, None, 5/4, 11/8, None, 3/2, None, 13/8, None 7/4, None], unit='ratios'),
	Macro('13ed3', 13, 3, 1, [
			0, None, 1, None, 2, 3, 4, 5, None, 6, None, 7,
			8, 9, 10, None, 11, 12, None, 13, None, 14, 15, 16,
			17, None, 18, None, 19, 20, 21, 22, None, 23, 24, 25
		]),
	Macro('9edo', 9, 2, 1, [0, 1, None, 2, 3, 4, 5, None, 6, None, 7, 8]),
	Ombak('5edo+ombak', 0.0, +10.0, 5, 2, 1, [
			None, 0, None, 2, None, None, 4, None, 6, None, 8, None,
			None, 10, None, 12, None, None, 14, None, 16, None, 18, None,
			None, 1, None, 3, None, None, 5, None, 7, None, 9, None,
			None, 11, None, 13, None, None, 15, None, 17, None, 19, None
		], concert_a_frequency=440.0*2**(1/5)),
	Macro('10edo', 10, 2, 1, [0, 1, 2, 3, None, 4, 5, 6, 7, 8, 9, None]),
	Default(),
	Octave('Pythagorean', pythagorean(), unit='ratios'),
	Micro('14edo', 14, 2, 1, [0, 1, 2, 3, (4,5), 6, 7, 8, 9, 10, 11, (12,13)]),
	Micro('9ed3/2', 9, 3, 2, [
			0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14,
			16, 17, 18, 19, 21, 22, 23, 24, None, 25, None, 26
		]),
	Micro('17edo', 17, 2, 1, [0, (1,2), 3, 4, (5,6), 7, (8,9), 10, (11,12), 13, 14, (15,16)]),
	Ombak('9edo-ombak', -10.0, 0.0, 9, 2, 1, [
			0, 2, None, 4, 6, 8, 10, None, 12, None, 14, 16,
			18, 20, None, 22, 24, 26, 28, None, 30, None, 32, 34,
			1, 3, None, 5, 7, 9, 11, None, 13, None, 15, 17,
			19, 21, None, 23, 25, 27, 29, None, 31, None, 33, 35
		]),
	Micro('19edo', 19, 2, 1, [0, (2,1), 3, (5,4), (6,7), 8, (10,9), 11, (13,12), 14, (16,15), (17,18)]),
	Subset('48edo', 48, 2, 1, {0, 3, 4, 8, 12, 13, 15, 16, 20, 24, 23, 28, 31, 32, 36, 40, 41, 43, 44}, [0, (4,3), 8, (12,13), (15,16), 20, (24,23), 28, (32,31), 36, (40,41), (43,44)]),
	Micro('8ed4/3'), 8, 4, 3, [
			0, 2, 3, 5, 6, 8, 10, 11, 13, 15, 16, 18),
			19, 21, 22, 24, 26, 27, 29, 31, 32, 34, 37, 39)
		]),
	Micro('22edo', 22, 2, 1, [0, (2,1), (4,3), (5,6), (7,8), 9, (11,10), (13,12), (15,14), (17,16), (18,19), (20,21)]),
	Subset('53edo', 53, 2, 1, {0, 4, 5, 8, 9, 13, 14, 17, 18, 22, 26, 27, 30, 31, 35, 36, 39, 40, 44, 45, 48, 49}, [0, (4,5), (9,8), (13,14), (17,18), 22, (26,27), (31,30), (35,36), (40,39), (44,45), (48,49)]),
	Micro('24edo', 24, 2, 1, [(0,-1), (2,1), (4,3), (6,5), (7,8), (10,9), (12,11), (14,13), (16,15), (18,17), (20,19), (21,22)]),
	Micro('29edo', 29, 2, 1, [0, (2,3), 5, (7,8), (9,10), 12, (14,15), 17, (19,20), 22, (24,25), (26,27)]),
	Micro('31edo', 31, 2, 1, [0, (3,2), (5,6), (8,7), (10,9), 13, (16,15), (18,19), (21,20), (23, 24), (26,25), (28,27)]),
	Micro('34edo', 34, 2, 1, [0, (2,3), 6, (8,9), (10,11), (14,12), (17,16), (20,19), (23,22), (25,26), (27,28), (29,30), (32,31)]),
	Micro('36edo', 36, 2, 1, [(0,-1), (3,2), (6,5), (9,8), (11,12), (15,14), (18,17), (21,20), (24,23), (27,26), (30,29), (32,33)]),
	Arbitrary('Harmonic Series', range(1,129), unit='ratios'),
	]
	

class Layouts:
	
	def crop(self, overlap, split=False):
		...
	
	def exquis(self, width=3, top_note=67):
	
		assert top_note in range(60, 128)
		mapping = [[0]*6 if row % 2 == 0 else [0]*5 for row in range(0,11)]
		overlap = (10 - width) % 5
		
		if width in range(1,6):
			last_note = top_note
			for row in range(10, -1, -1):
				if row % 2 == 0: # is even
					for col in range(5, -1, -1):
						note = last_note - (5 - col)
						mapping[row][col] = note
					last_note = note - 1 + overlap
				else:
					for col in range(4, -1, -1):
						note = last_note - (4 - col)
						mapping[row][col] = note
					last_note = note - 1 + overlap
							
		elif width in range(6,11):
			last_note = top_note
			for row in range(10, 5, -1):
				if row % 2 == 0: # is even
					for col in range(5, -1, -1):
						note = last_note - (5 - col)
						mapping[row][col] = note
					last_note = note - 1 - 5 + overlap
				else:
					for col in range(4, -1, -1):
						note = last_note - (4 - col)
						mapping[row][col] = note
					last_note = note - 6 + overlap
			last_note = top_note - 6 + 1
			for row in range(4, -1, -1):
				if row % 2 == 0: # is even
					for col in range(5, -1, -1):
						note = last_note - (5 - col)
						mapping[row][col] = note
					last_note = note  - 1 - 5 + overlap
				else:
					for col in range(4, -1, -1):
						note = last_note - (4 - col)
						mapping[row][col] = note
					last_note = note - 6 + overlap
			
		else:
			raise ValueError('width must be in range [1, 11)')
			
		output = []
		for row in mapping:
			for key in row:
				output.append(key)
		return output
		

## Controls
class Controls:
	
	def __init__(self):
		...
		
	def octave(self, msg):
		if 
	
	def orientation(self, ...):
		...
		
	def transposition(self, ...):
		...
	
	def tuning(self, ...):
		...
		
	def dilation(self, ...):
		...
		
	def layout(self, ...):
		...
		
		

class Script:
	def __init__(self):
		...


## Script




from_exquis = ...
from_lower_manual = ...
from_upper_manual = ...
script = Script()
to_exquis = ...
to_lower_manual = ...
to_upper_manual = ...
	
		

# comments
# --------
# tuning is controlled by
# 1. octave buttons
# 2. knob 2 (tuning preset)
# mapping is controlled by
# 1. page buttons
# 2. knob 1 (transpose)
# 3. knob 3 (dilation)
# 4. knob 4 (layout preset)
# at each change all tuning/mapping respectively is reset
#
# tuning preset is chosen by picking an element from the tunings array and resetting
# octave is chosen by passing an octave argument to reset
