from colour import Color
import numpy as np

# Testing
#########

class Testport:
	def send(self, msg):
		print('meddelande', msg, 'klar')
		return msg
testport = Testport()

class MtsTest:
	def set_scale_name(self, name):
		print('skalnamn', name, 'klar')
		return name
	def set_note_frequencies(self, frequencies):
		print('Hertz')
		out = np.array(frequencies)
		print(out)
		out = 1200 * np.log2(out/440.0)
		print('cent')
		print(out)
		print('klar')
		return out
mts_test = MtsTest()

# Lib
#####

# more use of numpy encouraged

tone_to_int = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
is_white_key = [True, False, True, False, True, True, False, True, False, True, False, True]

def concat(terms, middle_note, note_range):
	terms = np.array(terms)
	span = max(note_range) - min(note_range) + 1
	middle = middle_note - min(note_range)
	arr = np.zeros(span)
	if len(terms.shape) == 1:
		for i, note in enumerate(range(middle+1, span)):
			term = terms[i % len(terms)]
			arr[note] += arr[note-1] + term
		for i, note in enumerate(range(middle-1, -1, -1), start=1):
			term = terms[-i % len(terms)]
			arr[note] += arr[note+1] - term
	else:
		for note in range(1, span):
			arr[note] += arr[note-1] + terms
	return arr

def ombakify(pengumbang, pengisep, half):
	pengumbang = 0.0 if pengumbang is None else float(pengumbang)
	pengisep = 0.0 if pengisep is None else float(pengisep)
	full = np.empty(128)
	for i, pair in enumerate(zip(range(0,127,2), range(1,128,2))):
		full[pair[0]] = half[i] - pengumbang
		full[pair[1]] = half[i] + pengisep
	return full

# Banks
#######

class BaseTuning:

	def __init__(self, # add equaves
	name = '12edo',
	steps = 2 ** (1/12),
	unit = 'ratios',
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
		self.switches = np.zeros(self.keys_per_equave)
		self.is_switch = [True if hasattr(i, '__len__') else False for i in self.halberstadt]
		self.init_halberstadt = np.array([i[0] if self.is_switch[i] else i for i in self.halberstadt])
		self.keys_per_period = len(self.halberstadt) - 1
		self.degrees_per_equave = self.init_halberstadt[-1] - self.init_halberstadt[0]
		self.middle_key = 60 + tone_to_int.index(self.boundary_tone)
		self.root_degree = self.init_halberstadt[self.root_none - self.middle_key]
		self.middle_note = self.root_note - self.root_degree

	def get_frequencies(self):
		terms = np.array(self.steps)
		if self.unit == 'ratios':
			terms = 1200 * np.log2(frequencies)
		frequencies = concat(terms, self.middle_note, note_range=[0,127])
		if self.unit != 'Hertz':
			frequences = 2 ** (frequences/1200)
		root_note = self.root_note + self.equave * self.degrees_per_equave
		frequencies -= frequencies[root_note]
		frequencies += self.root_frequency
		return frequencies.tolist()

	def get_colors(self):
		colors = [Color(self.split_keys)]
		for note in range(128):
			halberstadt_note = self.remap(note)
			if halberstadt_note is not None:
				degree = halberstadt_note % self.keys_per_equave
				colors[note] = Color(self.white_keys if is_white_key[degree] else self.black_keys)
		return colors

	def remap(self, note):
		note -= self.middle_key
		tone = note % self.keys_per_equave
		octave = note // self.keys_per_equave
		degree = self.halberstadt[tone][self.switches[tone]] if self.is_switch[tone] else self.halberstadt[tone]
		if degree is not None:
			halberstadt_note = octave * self.degrees_per_equave + degree
			halberstadt_note += self.middle_note
			if halberstadt_note in range(0,128):
				return halberstadt_note
		return None

	def tuning(self, mts, equave=None):
		if equave is not None:
			self.equave = equave
		frequencies = self.get_frequencies()
		mts.set_note_tunings(frequencies)
		mts.set_scale_name(self.name)
		colors = self.get_colors()
		return colors

	def halberstadtify(self, outport, msg, manual=None):
		if hasattr(msg, 'note'):
			halberstadt_note = self.remap(msg.note)
			if halberstadt_note is not None:
				outport.send(msg.copy(note=halberstadt_note))
		else:
			outport.send(msg)

	def keyswitches(self, outport, msg):
		colors = self.halberstadtify(outport)
		return None

	def footswitch(self, msg):
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
		for note in range(128):
			halberstadt_note = self.remap(note)
			if halberstadt_note is not None:
				octave = halberstadt_note // self.keys_per_equave
				if octave % 2 == 0:
					degree = halberstadt_note % self.keys_per_equave
					colors[note] = Color(self.white_keys if is_white_key[degree] else self.black_keys)


class Micro(BaseTuning):

	white_keys = 'red'
	black_keys = 'orange'
	split_keys = 'black'

	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			halberstadt_note = self.remap(msg.note)
			if halberstadt_note is not None:
				if manual <= 1:
					outport.send(msg.copy(note=halberstadt_note))
				else:
					outport.send(msg.copy(note=halberstadt_note+1))
		else:
			outport.send(msg)

	def keyswitches(self, outport, msg):
		if msg.type == 'note_on':
			key = msg.note % self.keys_per_equave
			if self.is_switch[key] and msg.velocity > 0:
				self.switches[key] += 1
				self.switches[key] %= len(self.halberstadt[key])
				colors = self.get_colors()
		return None

	def footswitch(self, msg):
		if msg.type == 'control_change':
			for key, is_switch in enumerate(self.is_switch):
				if is_switch:
					if msg.value >= 64:
						self.switches[key] -= 1
					else:
						self.switches[key] += 1
					self.switches %= len(self.halberstadt[key])
					colors = self.get_colors()
					return colors
		return None


class Ombak(Macro):

	pengumbang_white_keys = 'cyan'
	pengumbang_black_keys = 'blue'
	pengisep_keys = 'black'
	duophonic = False

	def get_colors(self):
		colors = [Color(self.pengisep_keys)]*128
		for pengumbang_note in range(0,127,2):
			halberstadt_note = self.remap(pengumbang_note)
			if halberstadt_note is not None:
				degree = halberstadt_note % self.keys_per_equave
				colors[pengumbang_note] = Color(self.even_white_keys if is_white_key[degree] else self.even_black_keys)
		return colors

	def get_frequencies(self):
		terms = np.array(self.steps)
		if self.unit == 'ratios':
			terms = 1200 * np.log2(frequencies)
		frequencies = concat(terms, self.middle_note, note_range=[32,96])
		if self.unit != 'Hertz':
			frequences = 2 ** (frequences/1200)
		frequencies = ombakify(self.pengumbang, self.pengisep, frequencies)
		root_note = self.root_note + self.equave * self.degrees_per_equave
		frequencies -= frequencies[root_note]
		frequencies += self.root_frequency
		return frequencies.tolist()

	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			if msg.note in range(32, 96):
				halberstadt_note = self.remap(msg.note) - 32
				if manual <= 1:
					pengumbang_note = min([2*halberstadt_note, 127])
					outport.send(msg.copy(note=pengumbang_note))
					if self.duophonic:
						outport.send(msg.copy(note=pengumbang_note+1))
				else:
					pengisep_note = min([2*halberstadt_note+1, 127])
					outport.send(msg.copy(note=pengisep_note))
					if self.duophonic:
						outport.send(msg.copy(note=pengisep_note-1))
		else:
			outport.send(msg)

	def footswitch(self, msg):
		if msg.type == 'control_change':
			duophonic = True if msg.value >= 64 else False
			if duophonic != self.duophonic:
				self.duophonic = duophonic
				colors = self.get_colors()
				return colors
		return None


class Uneven(Macro):

	even_white_keys = 'magenta'
	even_black_keys = 'blue'
	odd_keys = 'black'


class Subset(Micro):

	white_keys = 'magenta'
	black_keys = 'blue'
	split_keys = 'black'


# Examples
##########

edo12 = {'comment': 'Standard tuning.'}

edo5 = {'name': '5edo',
'steps': 2 ** (1/5),
'root_note': 70,
'halberstadt': [0, None, 1, None, None, 2, None, 3, None, 4, None, None, 5],
'boundary_tone': 'c#',
'dilation': 1}

edt13 = {'name': '13ed3',
'steps': 3 ** (1/13),
'numerator': 3,
'halberstadt': [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
'dilation': 2}

edo41 = {'name': '41edo',
'steps': 2 ** (1/41),
'halberstadt': [0, 6, (7,8), (12,11), (13,14), 17, 21, 24, (29,30), (31,32), 35, (37,38), 41],
'dilation': 8}

just7 = {'name': 'just7',
'steps': [9/8, 5/4, 11/8, 3/2, 13/8, 7/4, 2],
'halberstadt': [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
'dilation': 2}

edo9ombak = {'name': '9edo+ombak',
'steps': 2 ** (1/9),
'root_note': 70,
'pengisep': 7.0,
'halberstadt': [0, 1, None, 2, 3, 4, 5, None, 6, None, 7, 8, 9],
'dilation': 2}

edo24 = {'name': '24edo',
'steps': 2 ** (1/24),
'halberstadt': [(-1,0), (2,1), (4,3), (6,5), (7,8), (10,9), (12,11), (14,13), (16,15), (18,17), (20,19), (22,21), (23,24)],
'dilation': 6}

ed43hz = {'name': 'ed43Hz',
'steps': 43.0,
'unit': 'Hertz',
'halberstadt': [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
'dilation': 2}

ed3halves9 = {'name': '9ed3/2',
'steps': (3/2) ** (1/9),
'halberstadt': [0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14,
16, 17, 18, 19, 21, 22, 23, 25, 26, 28, 29, 30, 31], # 23, 24, None, 25, None, 26, 27],
'dilation': 4}

edt11 = {'name': '11ed3',
'steps': 3 ** (1/11),
'halberstadt': [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
'dilation': 2,
'comment': 'Thai tuning.'}

edo53 = {'name': '53edo',
'steps': [2 ** (step/53) for step in [4, 5, 8, 9, 13, 14, 17, 18, 22, 26, 27, 30, 31, 35, 36, 39, 40, 44, 45, 48, 49, 53]],
'halberstadt': [0, (1,2), (3,4), (5,6), (7,8), 9, (10,11), (13,12), (14,15), (17,16), (18,19), (20,21), 22],
'dilation': 5,
'comment': '22 shrutis.'}
