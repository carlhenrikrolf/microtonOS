from colour import Color
import numpy as np

# Testing
#########

class Testport:
	def send(self, msg):
		print('meddelande', msg, 'klar')
testport = Testport()

class MtsTest:
	def set_scale_name(self, name):
		print('skalnamn', name, 'klar')
	def set_note_tunings(self, frequencies):
		print('Hertz')
		out = np.array(frequencies)
		print(out)
		out = 1200 * np.log2(out/440.0)
		print('cent')
		print(out)
		print('klar')
mts_test = MtsTest()

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
		self.ignore = [False]*128
		
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
				self.ignore[i] = True
			else:
				self.ignore[i] = False
		return result.tolist()

	def get_colors(self):
		colors = [Color(self.split_keys)]*128
		diff = 128/self.degrees_per_equave*self.keys_per_equave
		diff = int(diff) + 1
		for halberstadt_key in range(self.middle_key-diff,self.middle_key+diff):
			isomorphic_note = self.remap(halberstadt_key)
			if isomorphic_note is not None:
				if self.ignore[isomorphic_note]:
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
		
	def thru(self, outport, msg):
		if hasattr(msg, 'note'):
			if not self.ignore[msg.note]:
				outport.send(msg)
		else:
			outport.send(msg)

	def halberstadtify(self, outport, msg, manual=None):
		if hasattr(msg, 'note'):
			halberstadt_note = self.remap(msg.note)
			if halberstadt_note is not None:
				self.thru(outport, msg.copy(note=halberstadt_note))
		else:
			outport.send(msg)

	def keyswitches(self, outport, msg, manual=None):
		_ = self.halberstadtify(outport, msg, manual=manual)
		return None

	def footswitch(self, msg):
		if msg.type == 'control_change':
			new_pedal = True if msg.value >= 64 else False
			if new_pedal != self.pedal:
				if new_pedal is True:
					self.pedal = new_pedal
				elif self.pedal is not None:
					self.pedal = new_pedal
		return None


class Default(BaseTuning):

	white_keys = 'black'
	black_keys = 'gold'
	split_keys = 'black'


class Macro(BaseTuning):

	even_white_keys = 'green'
	even_black_keys = 'chartreuse'
	odd_keys = 'black'

	def get_colors(self):
		colors = [Color(self.odd_keys)]*128
		diff = 128/self.degrees_per_equave*self.keys_per_equave
		diff = int(diff) + 1
		for halberstadt_key in range(self.middle_key-diff,self.middle_key+diff):
			isomorphic_note = self.remap(halberstadt_key)
			if isomorphic_note is not None:
				if self.ignore[isomorphic_note]:
					colors[isomorphic_note] = Color(self.non_keys)
				else:
					halberstadt_equave = halberstadt_key // self.keys_per_equave
					if halberstadt_equave % 2 == 0:
						degree = halberstadt_key % self.keys_per_equave
						colors[isomorphic_note] = Color(self.even_white_keys if is_white_key[degree % 12] else self.even_black_keys)
		return colors


class Micro(BaseTuning):

	white_keys = 'red'
	black_keys = 'darkorange'
	split_keys = 'black'

	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			isomorphic_note = self.remap(msg.note)
			if isomorphic_note is not None:
				if manual == 1:
					self.thru(outport, msg.copy(note=isomorphic_note))
				else:
					self.thru(outport, msg.copy(note=isomorphic_note+1))
		else:
			outport.send(msg)

	def keyswitches(self, outport, msg):
		if msg.type == 'note_on':
			key = msg.note % self.keys_per_equave # maybe adjust this to get 1-to-1?
			if self.is_switch[key] and msg.velocity > 0:
				self.switches[key] += 1
				self.switches[key] %= len(self.halberstadt[key])
				colors = self.get_colors()
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

	white_keys = 'cyan'
	black_keys = 'blue'
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
				self.ignore[i] = True
			else:
				self.ignore[i] = False
		return result.tolist()
		
	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			isomorphic_note = self.remap(msg.note)
			if isomorphic_note is not None:
				if manual == 1:
					self.thru(outport, msg.copy(note=isomorphic_note))
					if self.pedal is True:
						self.thru(outport, msg.copy(note=isomorphic_note+1))
				else:
					self.thru(outport, msg.copy(note=isomorphic_note+1))
					if self.pedal is True:
						self.thru(outport, msg.copy(note=isomorphic_note))
		else:
			outport.send(msg)


class Uneven(Macro):

	even_white_keys = 'magenta'
	even_black_keys = 'indigo'
	odd_keys = 'black'


class Subset(Micro):

	white_keys = 'magenta'
	black_keys = 'indigo'
	split_keys = 'black'


# Examples
##########

edo12 = Default()

edo5 = Macro(name='5edo',
steps = 2 ** (1/5),
root_note = 70,
halberstadt = [0, None, 1, None, None, 2, None, 3, None, 4, None, None, 5],
boundary_tone = 'c#',
dilation = 1)

edt13 = Macro(name = '13ed3',
steps = 3 ** (1/13),
halberstadt = [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
dilation = 2)

just7 = Uneven(name = 'just7', # doesnt look right
steps = [9/8, 5/4, 11/8, 3/2, 13/8, 7/4, 2],
halberstadt = [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
dilation = 2)

edo41 = Micro(name = '41edo',
steps = 2 ** (1/41),
halberstadt = [0, 6, (7,8), (12,11), (13,14), 17, 21, 24, (29,30), (31,32), 35, (37,38), 41],
dilation = 8)

edo53 = Subset(name = '53edo',
steps = [2 ** (step/53) for step in [4, 5, 8, 9, 13, 14, 17, 18, 22, 26, 27, 30, 31, 35, 36, 39, 40, 44, 45, 48, 49, 53]],
halberstadt = [0, (1,2), (3,4), (5,6), (7,8), 9, (10,11), (13,12), (14,15), (17,16), (18,19), (20,21), 22],
dilation = 5,
comment = '22 shrutis.')

edo24 = Micro(name = '24edo',
steps = 2 ** (1/24),
halberstadt = [(0,-1), (2,1), (4,3), (6,5), (7,8), (10,9), (12,11), (14,13), (16,15), (18,17), (20,19), (21,22), (24,23)],
dilation = 6)

ed43hz = Macro(name = 'ed43Hz',
steps = 43.0,
unit = 'Hertz',
halberstadt = [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
dilation = 2)

ed3halves9 = Micro(name = '9ed3/2',
steps = (3/2) ** (1/9),
halberstadt = [0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14,
16, 17, 18, 19, 21, 22, 23, 25, 26, 28, 29, 30, 31], # 23, 24, None, 25, None, 26, 27],
dilation = 4)

edo9ombak = Ombak(name = '9edo+ombak',
steps = 2 ** (1/9),
root_note = 70,
pengisep = 7.0,
halberstadt = [0, 2, None, 4, 6, 8, 10, None, 12, None, 14, 16, 18],
dilation = 4)

