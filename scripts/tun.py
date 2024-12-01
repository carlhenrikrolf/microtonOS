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

class Tuning:

	def __init__(self,
		name='12edo',
		halberstadt=edo12,
		repeated_note='c',
		concert_a = 69,
		diapason=440.0,
		white_keys=Color('black'),
		black_keys=Color('orange'),
		split_keys=Color('red'),
		dilation=3,
		equal_divisions=range(12),
		numerator=2,
		divisor=1,
		ratios=None,
		cents=None,
		pengumbang=None,
		pengisep=None):

		self.halberstadt = halberstadt
		self.repeated_note = repeated_note
		self.concert_a = concert_a
		self.diapason = diapason
		self.white_keys = white_keys
		self.black_keys = black_keys
		self.split_keys = split_keys

		self.checks()

		self.switches = [0 for i in range(len(self.halberstadt))]

	def checks(self):
                if type(self.halberstadt[0]) is int:
                        assert type(self.halberstadt[-1]) is int
                elif type(self.halberstadt[0]) is tuple:
                        assert len(self.halberstadt[0]) == len(self.halberstadt[-1])
                else:
                        raise Warning('Halberstadt needs to begin and end with an int or tuple')
		# check concert_a is not None

	def halberstadtify(self, midi_note, manual=1):
		midi_note = remap(self.halberstadt,
			midi_note,
			repeated_note=self.repeated_note,
			concert_a=self.concert_a)
		if manual == 1:
			return midi_note
		elif manual == 2:
			return midi_note + 1
		else:
			return 'two midi notes should go here for ombak' #################

	def tuning(self):
		return self.coloring()

	def coloring(self):
		colors = [self.split_keys]*128
		for midi_note in range(0,128):
			switched_on, new_note = remap2(self.halberstadt,
				midi_note,
				switches=self.switches,
				repeated_note=self.repeated_note.
				concert_a=self.concert_a)
			if switched_on is True:
				if is_white_key[midi_note % 12]:
					colors[new_note] = self.white_keys
				else:
					colors[new_note] = self.black_keys
			#elif switched_on is False:
			#	for split_note in new_note:
			#		colors[split_note] = self.split_keys
		return colors


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
        half = cents_to_hertz(cents, init_halberstadt, repeated_tone, root_note, root_frequency, note_floor=128*1/4, note_ceil=128*3/4)
        full = np.empty(128)
        for i, pair in enumerate(zip(range(0,127,2), range(1,128,2))):
                full[pair[0]] = half[i] - pengumbang
                full[pair[1]] = half[i] + pengisep
        return full



# Banks
#######

class BaseTuning:

	def __init__(self,
	name='12edo',
	pitches = range(0, 13),
	unit = 'equal_divisions',
	cumulative = True,
	numerator = 2,
	divisor = 1,
	repeated_tone = 'c',
	root_note = 69,
	root_frequency = 440.0,
	pengumbang = 0,
	pengisep = 0,
	halberstadt = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
	dilation = 3,
	**kwargs):

		self.name = name
		self.pitches = np.array(pitches)
		self.period = float(numerator)  / float(divisor)

		self.checks()

	def checks(self):

		pass

	def tuning(self):

		pass

	def halberstadtify(self, msg):

		pass

	def switch_flick(self, msg):

		pass

class Default(BaseTuning):

	white_keys = 'black'
	black_keys = 'orange'

class Macro(BaseTuning):

	even_white_keys = ...
	even_black_keys = ...
	odd_white_keys = ...
	odd_black_keys = ...

class Micro(BaseTuning):

	pass

class Ombak(BaseTuning):

	pass

class Uneven(BaseTuning):

	pass

# ¿How to deal with non-octave tunings?

# Examples
##########

edo12 = {}

edo5 = {'name': '5edo',
'pitches': range(0, 6),
'repeated_tone': 'c#',
'root_note': 70,
'halberstadt': [0, None, 1, None, None, 2, None, 3, None, 4, None, None, 5],
'dilation': 1}

edt13 = {'name': '13ed3',
'pitches': range(0, 14),
'numerator': 3,
'halberstadt': [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7, None, 8, None, 9, None, 10, None, 11, None, 12, None, 13],
'dilation': 2}

edo41 = {'name': '41edo',
'pitches': range(0, 42),
'halberstadt': [0, 6, (7,8), (12,11), (13,14), 17, 21, 24, (29,30), (31,32), 35, (37,38), 41],
'dilation': 8}

just7 = {'name': 'just7',
'pitches': just7ratios = [1, 9/8, 5/4, 11/8, 3/2, 13/8, 7/4, 2],
'unit': 'ratios',
'halberstadt': [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
'dilation': 2}

edo9ombak = {'name': '9edo+ombak',
'pitches': range(0, 10),
'root_note': 70,
'pengisep': 7.0,
'halberstadt': [0, 1, None, 2, 3, 4, 5, None, 6, None, 7, 8, 9],
'dilation': 2}

edo24 = {'name': '24edo',
'pitches': range(0, 25),
'halberstadt': [(-1,0), (2,1), (4,3), (6,5), (7,8), (10,9), (12,11), (14,13), (16,15), (18,17), (20,19), (22,21), (23,24)],
'dilation': 6}

arithmetic43hz = {'name': '17Hz arithmetic',
'pitches': range(0,8),
'unit': 'hertz',
'cumulative': False,
'halberstadt': [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7],
'dilation': 2}

ed9eighths27 = {'name': '18ed9/8',
'pitches': range(0, 19),
'numerator': 9,
'divisor': 8
'halberstadt': [0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, None, 25, None, 26, 27],
'dilation': 4}
