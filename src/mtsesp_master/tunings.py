"""
	Tuning templates
"""

from colour import Color
import numpy as np


# Lib
#####

tone_to_int = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
is_white_key = [True, False, True, False, True, True, False, True, False, True, False, True]

def concat(terms, middle_note, note_range, cumulative):
	terms = np.array(terms) if len(np.array(terms).shape) == 1 else np.array([terms])
	span = max(note_range) - min(note_range) + 1
	middle = middle_note - min(note_range)
	arr = np.zeros(span)
	if cumulative:
		for i, note in enumerate(range(middle+1, span)):
			arr[note] += terms[i % len(terms)]
			arr[note] += terms[-1] * (i // len(terms))
		for i, note in enumerate(range(middle, -1, -1), start=0):
			arr[note] += terms[(-i-1) % len(terms)]
			arr[note] -= terms[-1] * ((i // len(terms)) + 1)
	else:
		for i, note in enumerate(range(middle+1, span)):
			term = terms[i % len(terms)]
			arr[note] += arr[note-1] + term
		for i, note in enumerate(range(middle-1, -1, -1), start=1):
			term = terms[-i % len(terms)]
			arr[note] += arr[note+1] - term
	return arr

def ombakify(pengumbang, pengisep, half):
	pengumbang = 0.0 if pengumbang is None else float(pengumbang)
	pengisep = 0.0 if pengisep is None else float(pengisep)
	full = []
	for frequency in half:
		full.append(frequency - pengumbang)
		full.append(frequency + pengisep)
	full = np.array(full)
	return full
	


# Templates
###########

class BaseTuning:
	
	non_keys = 'white'

	def __init__(self,
	name = '12edo',
	steps = 2 ** (1/12),
	unit = 'ratios',
	cumulative = True,
	root_note = 69,
	root_frequency = 440.0,
	equave = 0,
	pengumbang = None,
	pengisep = None,
	halberstadt = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
	boundary_tone = 'c',
	dilation = 3,
	comment = '',
	**kwargs):

		self.name = name if type(name) is str else 'Unnamed'
		self.steps = steps
		assert unit in ['ratios', 'cents', 'Hertz']
		self.unit = unit
		self.cumulative = cumulative
		self.root_note = root_note
		self.root_frequency = root_frequency
		self.equave = equave
		self.pengumbang = pengumbang
		self.pengisep = pengisep
		self.halberstadt = halberstadt
		self.boundary_tone = boundary_tone
		self.dilation = dilation
		self.comment = comment

		self.keys_per_equave = len(self.halberstadt) - 1
		self.switches = [0]*self.keys_per_equave
		self.is_switch = [True if hasattr(degree, '__len__') else False for degree in self.halberstadt]
		self.init_halberstadt = [degree[0] if self.is_switch[i] else degree for i, degree in enumerate(self.halberstadt)]
		self.degrees_per_equave = self.init_halberstadt[-1] - self.init_halberstadt[0]
		self.middle_key = 60 + tone_to_int.index(self.boundary_tone)
		self.root_degree = self.init_halberstadt[self.root_note - self.middle_key]
		self.middle_note = self.root_note - self.root_degree
		self.pedal = None
		self.is_ignored = [False]*128
		self.backup = [[set() for _ in range(16)] for _ in range(128)]
		
	def remap(self, note):
		note -= self.middle_key
		tone = note % self.keys_per_equave
		octave = note // self.keys_per_equave
		degree = self.halberstadt[tone][self.switches[tone]] if self.is_switch[tone] else self.halberstadt[tone]
		if degree is not None:
			new_note = octave * self.degrees_per_equave + degree
			new_note += self.middle_note
			if new_note in range(0,128):
				return new_note
		return None
		
	def get_frequencies(self):
		result = np.array(self.steps)
		root_note = self.root_note - self.equave * self.degrees_per_equave
		if self.unit == 'ratios':
			result = 1200 * np.log2(result)
		result = concat(result, self.middle_note, range(0,128), self.cumulative)
		if self.unit == 'Hertz':
			result -= result[root_note]
			result += self.root_frequency
		else:
			result = 2 ** (result/1200)
			result /= result[root_note]
			result *= self.root_frequency
		for i, frequency in enumerate(result):
			if frequency <= 0:
				result[i] = 440.0
				self.is_ignored[i] = True
			else:
				self.is_ignored[i] = False
		return result.tolist()

	def get_colors(self):
		colors = [Color(self.split_keys)]*128
		diff = 128/self.degrees_per_equave*self.keys_per_equave
		diff = int(diff) + 1
		for halberstadt_key in range(self.middle_key-diff,self.middle_key+diff):
			isomorphic_note = self.remap(halberstadt_key)
			if isomorphic_note is not None:
				if self.is_ignored[isomorphic_note]:
					colors[isomorphic_note] = Color(self.non_keys)
				else:
					#halberstadt_equave = halberstadt_key // self.keys_per_equave
					degree = halberstadt_key % self.keys_per_equave
					colors[isomorphic_note] = Color(self.white_keys if is_white_key[degree % 12] else self.black_keys)
		return colors

	def tuning(self, mts, equave=None):
		if equave is not None:
			self.equave = equave
		frequencies = self.get_frequencies()
		mts.set_note_tunings(frequencies)
		mts.set_scale_name(self.name)
		self.pedal = None
		colors = self.get_colors()
		return colors
			
	def ignore(self, note_msg):
		if hasattr(note_msg, 'note'):
			return self.is_ignored[note_msg.note]
		elif type(note_msg) is int:
			return self.is_ignored[note_msg] if note_msg in range(0,128) else True
		elif note_msg is None:
			return True
		return False
	
	def thru(self, old_msg, outport, msg):
		if old_msg.type == msg.type == 'note_on':
			self.backup[old_msg.note][old_msg.channel].add((msg.note, msg.channel))
			outport.send(msg)
		elif old_msg.type == msg.type == 'note_off':
			for note, channel in self.backup[old_msg.note][old_msg.channel]:
				outport.send(msg.copy(note=note, channel=channel))
			self.backup[old_msg.note][old_msg.channel] = set()

	def halberstadtify(self, outport, msg, manual=None):
		if hasattr(msg, 'note'):
			isomorphic_note = self.remap(msg.note)
			if not self.ignore(isomorphic_note):
				new_msg = msg.copy(note=isomorphic_note)
				self.thru(msg, outport, new_msg)
		else:
			outport.send(msg)

	def reset(self):
		for i in range(self.keys_per_equave):
			self.switches[i] = 0
		self.pedal = None

	def keyswitches(self, outport, msg, manual=1):
		_ = self.halberstadtify(outport, msg, manual=manual)
		return None

	def footswitch(self, msg):
		if msg.type == 'control_change':
			new_pedal = True if msg.value >= 64 else False
			if new_pedal != self.pedal:
				if new_pedal is True:
					self.pedal = True
				elif self.pedal is not None:
					self.pedal = False
		return None


class Default(BaseTuning):

	white_keys = 'black'
	black_keys = 'orange'
	split_keys = 'black'


class Macro(BaseTuning):

	even_white_keys = 'green'
	even_black_keys = 'orange'
	odd_keys = 'black'

	def get_colors(self):
		colors = [Color(self.odd_keys)]*128
		diff = 128/self.degrees_per_equave*self.keys_per_equave
		diff = int(diff) + 1
		for halberstadt_key in range(self.middle_key-diff,self.middle_key+diff):
			isomorphic_note = self.remap(halberstadt_key)
			if isomorphic_note is not None:
				if self.is_ignored[isomorphic_note]:
					colors[isomorphic_note] = Color(self.non_keys)
				else:
					halberstadt_equave = halberstadt_key // self.keys_per_equave
					if halberstadt_equave % 2 == 0:
						degree = halberstadt_key % self.keys_per_equave
						colors[isomorphic_note] = Color(self.even_white_keys if is_white_key[degree % 12] else self.even_black_keys)
		return colors


class Micro(BaseTuning):

	white_keys = 'orange'
	black_keys = 'red'
	split_keys = 'black'

	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			isomorphic_note = self.remap(msg.note)
			if not self.ignore(isomorphic_note):
				if manual == 1:
					new_msg = msg.copy(note=isomorphic_note)
					self.thru(msg, outport, new_msg)
				else:
					new_msg = msg.copy(note=isomorphic_note+1)
					self.thru(msg, outport, new_msg)
		else:
			outport.send(msg)

	def keyswitches(self, outport, msg, manual=1):
		if msg.type == 'note_on':
			key = (msg.note - tone_to_int.index(self.boundary_tone)) % self.keys_per_equave # maybe adjust this to get 1-to-1?
			if self.is_switch[key] and msg.velocity > 0:
				self.switches[key] += 1
				self.switches[key] %= len(self.halberstadt[key])
				colors = self.get_colors()
				return colors
		return None
		
	def footswitch(self, msg):
		if msg.type == 'control_change':
			new_pedal = True if msg.value >= 64 else False
			if new_pedal != self.pedal:
				if new_pedal is True:
					for key in range(self.keys_per_equave):
						if self.is_switch[key]:
							self.switches[key] -= 1
							self.switches[key] %= len(self.halberstadt[key])
					self.pedal = new_pedal
				elif self.pedal is not None:
					for key in range(self.keys_per_equave):
						if self.is_switch[key]:
							self.switches[key] += 1
							self.switches[key] %= len(self.halberstadt[key])
					self.pedal = new_pedal
				else:
					return None
				colors = self.get_colors()
				return colors
		return None


class Ombak(BaseTuning):

	white_keys = 'green'
	black_keys = 'cyan'
	split_keys = 'black'
		
	def get_frequencies(self):
		result = np.array(self.steps)
		floor = int(self.root_note/2)
		root_note = self.root_note - self.equave * self.degrees_per_equave
		root_note -= floor
		if self.unit == 'ratios':
			result = 1200 * np.log2(result)
		result = concat(result, 2*floor, range(floor,floor+64), self.cumulative)
		if self.unit == 'Hertz':
			result -= result[root_note]
			result += self.root_frequency
		else:
			result = 2 ** (result/1200)
			result /= result[root_note]
			result *= self.root_frequency
		result = ombakify(self.pengumbang, self.pengisep, result)
		for i, frequency in enumerate(result):
			if frequency <= 0:
				result[i] = 440.0
				self.is_ignored[i] = True
			else:
				self.is_ignored[i] = False
		return result.tolist()
		
	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			isomorphic_note = self.remap(msg.note)
			if not self.ignore(isomorphic_note) and not self.ignore(isomorphic_note+1):
				if manual == 1:
					new_msg = msg.copy(note=isomorphic_note)
					self.thru(msg, outport, new_msg)
					if self.pedal is True:
						msg2 = msg.copy(note=isomorphic_note+1)
						self.thru(msg, outport, msg2)
				else:
					new_msg = msg.copy(note=isomorphic_note+1)
					self.thru(msg, outport, new_msg)
					if self.pedal is True:
						msg2 = msg.copy(note=isomorphic_note)
						self.thru(msg, outport, msg2)
		else:
			outport.send(msg)


class Uneven(Macro):

	even_white_keys = 'purple'
	even_black_keys = 'navy'
	odd_keys = 'black'


class Subset(Micro):

	white_keys = 'purple'
	black_keys = 'navy'
	split_keys = 'black'

