from colour import Color
import numpy as np


def remap(halberstadt, midi_note, repeated_note='c', concert_a=69): #midi note first no?
	"""
		Remaps according to a Halberstadt layout.
		- midi_note = concert_a = output
		- repeated_note is the first and last note of halberstadt
	"""
	diff = 60 + note_to_num.index(repeated_note)
	n_keys = len(halberstadt) - 1
	n_steps = halberstadt[-1] - halberstadt[0]
	midi_note -= diff
	note = midi_note % n_keys
	octave = midi_note // n_keys
	n_degrees = halberstadt[note]
	if n_degrees is not None:
		midi_note = octave*n_steps + n_degrees
		midi_note += concert_a - halberstadt[concert_a-diff]
		if midi_note in range(0,128):
			return midi_note # note exists and is either a black or white key
		else:
			pass # note exists but is outside of span
	return None # note does not exist---it's not even a split key


def remap2(halberstadt, midi_note, switches=None, repeated_note='c', concert_a=69):
	# constants
	diff = 60 + note_to_num.index(repeated_note)
	init_halberstadt = [deg[0] if type(deg) is tuple else deg for deg in halberstadt]
	current_halberstadt = [deg[switches[i]] if type(deg) is tuple else deg for i, deg in enumerate(halberstadt)]
	n_keys = len(halberstadt) - 1
	n_steps = init_halberstadt[-1] - init_halberstadt[0] # could be current as well
	# main
	midi_note -= diff
	note = midi_note % n_keys
	octave = midi_note // n_keys
	n_degrees = current_halberstadt[note]
	if n_degrees is not None:
		midi_note = octave*n_steps + n_degrees
		midi_note += concert_a - init_halberstadt[concert_a-diff] # right?
		if midi_note in range(0,128):
			return True, midi_note
	# check if split key
	#elif type(halberstadt[note]) is tuple:
	#	midi_notes = []
	#	for n_degrees in halberstadt[note]:
	#		midi_note = octave*n_steps + n_degrees
	#		midi_note += concert_a - init_halberstadt[concert_a-diff] # right?
	#		if midi_note in range(0,128):
	#			midi_notes.append(midi_note)
	#	if len(midi_notes) > 0:
	#		return False, midi_notes
	# all else
	return None, None

class Testport:

	def send(self, msg):
		print(msg)

testport = Testport()

class MtsTest:

	def set_scale_name(self, name):
		print('scale name')
	def set_note_frequencies(self, f):
		print('set frequencies', f[0], f[1], f[2], '...', f[127])

# Lib
#####

# more use of numpy encouraged

tone_to_int = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
is_white_key = [True, False, True, False, True, True, False, True, False, True, False, True]

def ratios_to_cents(ratios):
        if hasattr(ratios, '__len__'):
		ratios = np.array(ratios)
                return 1200 * np.log2(ratios)
        else:
                return 1200 * np.log2(ratios)

def equal_divisions_to_cents(equal_divisions, period):
        equave_size = equal_divisions[-1] - equal_divisions[0]
        step_size = ratio_to_cents(period) / equave_size
        n = len(equal_divisions)
	cents = [0]*n
        for i in range(n):
                cents[i] = step_size * equal_divisions[i]
	return cent

def cents_to_hertz(cents, init_halberstadt, repeated_tone='c', root_note=69, root_frequency, note_floor=0, note_ceil=128):
        assert concert_a in range(note_floor, note_ceil)
	cycle = len(cents) - 1
        diff = 60 - note_to_num(repeated_tone)
	root_degree = init_halberstadt[root_tone - diff]
	cents -= cents[root_degree]
	cents = np.concat([cents[root_degree:], cents[:root_degree]])
	hertz = np.array([])
	for i, note in enumerate(range(root_note, note_ceil)):
		octave = i // cycle
		np.append(herz, cents[i % cycle] + octave)
	for i, note in enumerate(range(root_note-1, note_floor-1, -1), start=1):
		octave = i // cycle
		np.insert(hertz, 0, cents[(cycle-i) % cycle] - octave)
	hertz = root_frequency * 2 ** (hertz/1200)
	return hertz

def ombakify(cents, pengumbang, pengisep, init_halberstadt, repeated_tone='c', root_note=69, root_frequency=440.0):
        pengumbang = 0.0 if pengumbang is None else float(pengumbang)
	pengisep = 0.0 if pengisep is None else float(pengisep)
	half = cents_to_hertz(cents, init_halberstadt, repeated_tone, root_note, root_frequency, note_floor=128*1/4, note_ceil=128*3/4)
        full = np.empty(128)
        for i, pair in enumerate(zip(range(0,127,2), range(1,128,2))):
                full[pair[0]] = half[i] - pengumbang
                full[pair[1]] = half[i] + pengisep
        return full

def expand:
	...
def ratios_to_cents:
	...
def cents_to_hertz:
	...
def ombakify:
	...


# Banks
#######

class BaseTuning:

	def __init__(self,
	name = '12edo',
	steps = 2 ** (1/12),
	unit = 'ratios',
	root_note = 69,
	root_frequency = 440.0,
	pengumbang = None,
	pengisep = None,
	halberstadt = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
	boundary_tone = 'c',
	dilation = 3,
	comment = '',
	**kwargs):

		self.name = name if type(name) is str else 'Unnamed'
		self.steps = steps
		self.unit = unit
		self.root_note = root_note
		self.root_frequency = root_frequency
		self.pengumbang = pengumbang
		self.pengisep = pengisep
		self.halberstadt = halberstadt
		self.boundary_tone = boundary_tone
		self.dilation = dilation
		self.comment = comment

		self.period = len(self.halberstadt) - 1
		self.switches = np.zeros(self.period)
		self.is_switch = [True if has_attr(i, '__len__') else False for i in self.halberstadt]
		self.init_halberstadt = np.array([i[0] if hasattr(i, '__len__') else i for i in self.halberstadt])
		self.concert_a = 60 + tone_to_int.index(self.boundary_tone)
		self.root_degree = self.init_halberstadt[self.root_tone - self.concert_a]
		self.middle_c = selt.root_tone - self.root_degree
		self.bottom_c = self.middle_c - 60

		self.frequences = self.get_frequencies()

	def get_frequencies(self)
		frequencies = self.steps
		if self.unit == 'ratios':
			frequencies = ratios_to_cents(frequencies, ...)
		frequencies = expand(frequencies, ...)
		if self.unit != 'Hertz':
			frequencies = cents_to_hertz(frequencies, ...)
		frequencies = center(frequencies, ...)
		return frequencies

	def get_colors(self):
		colors = [Color(self.split_keys)]
		for note in range(128):
			halberstadt_note = self.remap(note)
 			if halberstadt_note is not None:
				degree = halberstadt_note % self.period
				colors[note] = Color(self.white_keys if is_white_key[degree] else self.black_keys)
		return colors


	def remap(self, note):
		...
		return halberstadt_note

	def tuning(self, mts, msg):
		mts.set_note_tunings(self.frequencies)
		mts.set_scale_name(self.name)
		colors = self.get_colors()
		return colors

	def halberstadtify(self, outport, msg, manual=None):
		if hasattr(msg, 'note'):
			halberstadt_note = self.remap(msg.note)
			outport.send(msg.copy(note=halberstadt_note))
		else:
			outport.send(msg)

	def switch_flick(self, outport, msg):
		self.halberstadtify(outport, msg)

	def pedal_press(self, msg):
		pass

class Default(BaseTuning):

	white_keys = 'black'
	black_keys = 'orange'
	split_keys = 'black'

class Macro(BaseTuning):

	even_white_keys = 'green'
	even_black_keys = 'orange'
	odd_keys = 'black'

	def get_colors(self):
		colors = [Color(self.odd_keys_keys)]
		for note in range(128):
			halberstadt_note = self.remap(note)
			if halberstadt_note is not None:
				octave = halberstadt_note // self.period
				if octave % 2 == 0:
					degree = halberstadt_note % self.period
					colors[note] = Color(self.white_keys if is_white_key[degree] else self.black_keys)

class Micro(BaseTuning):

	white_keys = 'red'
	black_keys = 'orange'
	split_keys = 'black'

	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			halberstadt_note = self.remap(msg.note)
			if manual <= 1:
				outport.send(msg.copy(note=halberstadt_note))
			else:
				outport.send(msg.copy(note=halberstadt_note+1))
		else:
			outport.send(msg)

	def switch_flick(self, outport, msg):
		if msg.type == 'note_on':
			degree =  msg.note % self.period
			if self.is_switch[degree] and msg.velocity > 0:
				self.switches[degree] += 1
				self.switches[degree] %= len(self.halberstadt[degree])

	def pedal_press(self, msg):
		if msg.type == 'control_change':
			for degree, is_switch in enumerate(self.is_switch):
				if is_switch:
					if msg.value >= 64:
						self.switches[degree] -= 1
					else:
						self.switches[degree] += 1
					self.switches %= len(self.halberstadt[degree])


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
				degree = halberstadt_note % self.period
				colors[pengumbang_note] = Color(self.even_white_keys if is_white_key[degree] else self.even_black_keys)
		return colors

	def get_frequencies(self):
		pengumbang = 0 if None else float(self.pengumbang)
		pengisep = 0 if None else float(self.pengisep)
		frequencies = self.step_sizes
		if self.unit == 'ratios':
			frequencies = ratios_to_cents(frequencies, ...)
		frequencies = expand(frequencies, note_range=[32,96], ...)
		if self.unit != 'Hertz':
			frequencies = cents_to_hertz(frequencies, ...)
		frequencies = ombakify(frequencies, ...)
		return frequencies

	def halberstadtify(self, outport, msg, manual=1):
		if hasattr(msg, 'note'):
			halberstadt_note = self.remap(msg.note)
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

	def pedal_press(self, msg):
		if msg.type == 'control_change':
			self.duophonic = True if msg.value => 64 else False

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
'boundary_tone', 'c#',
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
