from colour import Color

note_to_num = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
is_white_key = [True, False, True, False, True, True, False, True, False, True, False, True]

def n_steps(halberstadt):
	return halberstadt[-1] - halberstadt[0]

def n_keys(halberstadt):
	return len(halberstadt) - 1

def remap(halberstadt, midi_note, repeated_note='c', concert_a=69):
	"""
		Remaps according to a Halberstadt layout.
		- midi_note = concert_a = output
		- repeated_note is the first and last note of halberstadt
	"""
	diff = 60 + note_to_num.index(repeated_note)
	midi_note -= diff
	note = midi_note % n_keys(halberstadt)
	octave = midi_note // n_keys(halberstadt)
	n_degrees = halberstadt[note]
	if n_degrees is not None:
		midi_note = octave*n_steps(halberstadt) + n_degrees
		midi_note += concert_a - halberstadt[concert_a-diff]
		if midi_note in range(0,128):
			return midi_note
	return None

# example Halberstadt layouts
edo12 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

edo7 = [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6, 7]

edo5 = [0, None, 1, None, None, 2, None, 3, None, 4, None, None, 5]

edt13 = [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6,
	7, None, 8, None, 9, None, 10, None, 11, None, 12, None, 13]

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

	def checks(self):
                if type(self.halberstadt[0]) is int:
                        assert type(self.halberstadt[-1]) is int
                elif type(self.halberstadt[0]) is tuple:
                        assert len(self.halberstadt[0]) == len(self.halberstadt[-1])
                else:
                        raise Warning('Halberstadt needs to begin and end with an int or tuple')
		# check concert_a is not None

	def halberstadtify(self, midi_note):
		midi_note = remap(self.halberstadt,
			midi_note,
			repeated_note=self.repeated_note,
			concert_a=self.concert_a)
		return midi_note

	def tuning(self):
		return self.coloring()

	def coloring(self):
		colors = [self.black_keys]*128
		for midi_note in range(0,128):
			new_note = remap(self.halberstadt,
				midi_note,
				repeated_note=self.repeated_note.
				concert_a=self.concert_a)
			if new_note is None:
				colors[new_note] = self.split_keys
			elif is_white_key[midi_note % 12]:
				colors[new_note] = self.white_keys
		return colors

# relate to tuning

# relate to lights
