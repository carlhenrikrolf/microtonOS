from colour import Color

note_to_num = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
is_white_key = [True, False, True, False, True, True, False, True, False, True, False, True]

# add something about a subset
# - equal step tuning
# - translation for writing them in in absolute terms rather than relative

edo53 = [0, (4,5), (9,8), (13,14), (17,18), 22, (26,27), (31,30), (35,36), (40,39), (44,45), (48,49), 53]
edo53subset = {0, 4, 5, 8, 9, 13, 14, 17, 18, 22, 26, 27, 30, 31, 35, 36, 39, 40, 44, 45, 48, 49}

# other things maybe for more implementation
# - how to handle the switches
#	- increment along tuple if tuple
#	- add to Halberstadtify
# - add dilation
# - maybe add the octave option?
#   and the entire length option?

def pythagorean(steps=12):
	"""
		# Produces a Pythagorean tuning.
		# Default is 12 steps per octave.
		# Output is one octave in intervals.
	# """
	octave = [0.0]*steps
	ratio = 1
	for tone in range(steps):
		octave[tone] = ratio
		if tone % 2 == 0:
			ratio *= 3/2
		else:
			ratio /= 4/3
	return octave

just7 = [1, None, 9/8, None, 5/4, 11/8, None, 3/2, None, 13/8, None 7/4, None] # how to deal with ratios or cents?

############################

def equal_step_tuning(equal_steps, period, diapason=440.0, concert_a=69, midi_notes=range(0,128)):
	out = [diapason]*len(midi_notes)
	for i, midi_note in enumerate(midi_notes):
		out[i] *= period ** ((midi_note - concert_a)/equal_steps)
	return out

def ombak(equal_steps, period, even, odd, diapason=440.0, concert_a=69):
	half = equal_step_tuning(equal_steps, period, diapason=diapason, concert_a=concert_a, midi_notes=range(64-32, 64+32))
	full = [diapason]*128
	for i, pair in enumerate(zip(range(0,127,2), range(1,128,2))):
		full[pair[0]] = half[i] + even
		full[pair[1]] = half[i] + odd
	return full


def remap(halberstadt, midi_note, repeated_note='c', concert_a=69):
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
	elif type(halberstadt[note]) is tuple:
		midi_notes = []
		for n_degrees in halberstadt[note]:
			midi_note = octave*n_steps + n_degrees
			midi_note += concert_a - init_halberstadt[concert_a-diff] # right?
			if midi_note in range(0,128):
				midi_notes.append(midi_note)
		if len(midi_notes) > 0:
			return False, midi_notes
	# all else
	return None, None


# example Halberstadt layouts
edo12 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

edo7 = [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7]

edo5 = [0, None, 1, None, None, 2, None, 3, None, 4, None, None, 5]

edt13 = [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6,
	7, None, 8, None, 9, None, 10, None, 11, None, 12, None, 13]

edo41 = [0, 6, (7,8), (12,11), (13,14), 17, 21, 24, (29,30), (31,32), 35, (37,38), 41]

class Tuning:

	def __init__(self,
		halberstadt=edo12,
		repeated_note='c',
		concert_a = 69,
		diapason=440.0,
		white_keys=Color('black'),
		black_keys=Color('orange'),
		split_keys=Color('red')):

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
		colors = [self.black_keys]*128
		for midi_note in range(0,128):
			switched_on, new_note = remap2(self.halberstadt,
				midi_note,
				switches=self.switches,
				repeated_note=self.repeated_note.
				concert_a=self.concert_a)
			if switched_on is True:
				if is_white_key[midi_note % 12]:
					colors[new_note] = self.white_keys
			elif switched_on is False:
				for split_note in new_note:
					colors[split_note] = self.split_keys
		return colors
