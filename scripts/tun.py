from colour import Color

note_to_num = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

def n_steps(halberstadt):
	return halberstadt[-1] - halberstadt[0]

def n_keys(halberstadt):
	return len(halberstadt) - 1


def remap(halberstadt, midi_note, repeated_note='c', concert_a=69, midi_notes=range(0,128)):
	# 5edo concert a 70 repeated c#
	# 12edo concert a 69 repeated c
	midi_note -= 60 # 10 # 9
	midi_note -=  note_to_num.index(repeated_note) # 9 # 9
	note = midi_note % n_keys(halberstadt) # 9 # 9
	octave = midi_note // n_keys(halberstadt) # 0 # 0
	n_degrees = halberstadt[note] # 4 # 9
	if n_degrees is not None:
		midi_note = octave*n_steps(halberstadt) + n_degrees # 4 # 9
		#midi_note += note_to_num.index(repeated_note) # 5
		midi_note += concert_a - halberstadt[concert_a-60-note_to_num.index(repeated_note)] #70 # 69
		# step above should set concert_a as the same before and after
		# edo12 concert_a=69, repeated_note='c' => 69 -> 69, middle=60
		# middle = 69 - halberstadt[9]
		# edo12 concert_a=67, repeated_note='c' => 67 -> 67 (note=7, oct=0), middle=60
		# middle = concert_a - halberstadt[concert_a - 60]
		# edo12 concert_a=69, repeated_note='b' => 69 -> 69 (note=-2, oct=0) middle=71
		# middle = 69 - halberstadt[9] + note_to_num.index(repeated_note)
		# edo7 concert_a=69, repeated_note='c' => 69 -> 69 (note=9, oct=0, deg=5) middle=64
		# middle = 69 - halberstadt[9]
		if midi_note in midi_notes:
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

# relate to tuning

# relate to lights
