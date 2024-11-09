import mido
import time
from colour import Color

class Exquis: # version 1.2.0
	
	prefix = [0x00, 0x21, 0x7E]
	
	# mapping keys to notes
	default_map = [27, 28, 29, 30, 31, 32, 31, 32, 33, 34, 35, 34, 35, 36, 37, 38, 39, 38, 39, 40, 41, 42, 41, 42, 43, 44, 45, 46, 45, 46, 47, 48, 49, 48, 49, 50, 51, 52, 53, 52, 53, 54, 55, 56, 55, 56, 57, 58, 59, 60, 59, 60, 61, 62, 63, 62, 63, 64, 65, 66, 67] 
	equals_keys_map = list(range(0,61))
	
	# controls
	buttons = range(0,10)
	menu = range(0,6)
	knobs = range(0,5)
	settings = 0
	sounds = 1
	record = 2
	loops = 3 # app name
	tracks = 3 # synonym, webpage name
	snaps = 4 # app name
	scenes = 4 # synonym, webpage name
	play_stop = 5
	octave_down = 6
	octave_up = 7
	page_left = 8
	page_right = 9
	knob1 = 0
	button1 = 10
	knob2 = 1
	button2 = 11
	knob3 = 2
	button3 = 12
	knob4 = 3
	button4 = 13
	keys = range(0, 61)
	
	
	### received
	# actions
	color_key = 0x03
	map_key_to_note = 0x04
	color_button = 0x07
	color_knob = 0x09
	
	# states	
	blank = [0x00, 0x00, 0x00]
	dark = [0x00, 0x00, 0x00]
	exquis_blue = [0x38, 0x1D, 0x41]
	exquis_white = [0x7F, 0x5F, 0x3F]
	red = [127, 0, 0]
	lime = [0, 127, 0]
	green = [0, 64, 0]
	white = [127, 127, 127]
	cyan = [0, 127, 127]
	teal = [0, 64, 64]
	navy = [0, 0, 64]
	magenta = [127, 0, 127]
	purple = [64, 0, 64]
	maroon = [64, 0, 0]
	blue = [0, 0, 127]
	yellow = [127, 127, 0]
	chartreuse = [64, 127, 0]
	orange = [127, 83, 0]
	coral = [127, 64, 0]
	dark_red = [70, 0, 0]
	
	### transmitted
	click = 0x08
	clockwise = 11
	counter_clockwise = 10
	## states
	pressed = 1
	released = 0
	speeds = range(1,16)
		
	polling_time = 0.0001 # should be less than 0,0005 and more than 0.00001
	
	## cc
	sounds_control = 31
	record_control = 32
	loops_control = 33
	snaps_control = 34
	
	knob1_control = 41
	button1_control = 21
	knob2_control = 42
	button2_control = 22
	knob3_control = 43
	button3_control = 23
	knob4_control = 44
	button4_control = 24
	
	# dimensions
	length = 11
	widths = [5,6]
	n_keys = 61
	
	
	client_name = 'Exquis'
	inports = ['Exquis MIDI 1', 'Exquis MIDI 2']
	outports = ['Exquis MIDI 1', 'Exquis MIDI 2']
	
	def __init__(self):
		self.last_sensing = time.perf_counter_ns()
		self.current_map = [27, 28, 29, 30, 31, 32, 31, 32, 33, 34, 35, 34, 35, 36, 37, 38, 39, 38, 39, 40, 41, 42, 41, 42, 43, 44, 45, 46, 45, 46, 47, 48, 49, 48, 49, 50, 51, 52, 53, 52, 53, 54, 55, 56, 55, 56, 57, 58, 59, 60, 59, 60, 61, 62, 63, 62, 63, 64, 65, 66, 67] 
		self.current_key_colors = [[0,0,0]]*61
		self.current_knob_colors = [0,0,0,0]
		self.current_menus = [self.released]*len(self.menu)
		
		
	def is_connected(self):
		out = 0
		for outport in mido.get_output_names():
			out += max([port in self.client_name+':'+outport for port in self.outports])
		for inport in mido.get_input_names():
			out += max([port in self.client_name+':'+inport for port in self.inports])
		return bool(out)
	
	def active_sensing(self, port, sleep=0.3):
		assert 0 < sleep < 1 
		while True:
			port.send(
				mido.Message('sysex', data=self.prefix)
			)
			time.sleep(sleep)
			
	def is_active_sensing(self, msg=None):
		if type(msg) is None:
			return (time.perf_counter_ns() - self.last_sensing <= 1e9)
		elif (msg.type == 'sysex') and (list(msg.data) == self.prefix):
			self.last_sensing = time.perf_counter_ns()
			return True
		else:
			return False
			
	
	def sysex(self, action=[], control=[], state=[]):
		if ([] in [action, control, state]) or (None in [action, control, state]):
			return mido.Message('sysex', data=self.prefix)
		else:
			if type(state) is list:
				return mido.Message('sysex', data=[*self.prefix, action, control, *state])
			else:
				return mido.Message('sysex', data=[*self.prefix, action, control, state])
				
	def is_sysex(self, msg, data=None):
		if msg.type == 'sysex':
			indata = list(msg.data)
			if data is None:
				if indata[0:3] == self.prefix:
					return True
				else:
					return False
			else:
				if data[2] is None:
					if indata[3:5] == data[0:2]:
						return True, (indata[5] if len(indata[5:]) == 1 else indata[5:])
					else:
						return False
				elif type(data[2]) is list:
					if indata == [*self.prefix, data[0], data[1], *data[2]]:
						return True
					else:
						return False
				else:
					if indata == [*self.prefix, data[0], data[1], data[2]]:
						return True
					else:
						return False
		else:
			return False

	
	def send(self, port, sysex):
		if sysex.data[3] == self.color_key:
			self.current_key_colors[sysex.data[4]] = list(sysex.data[5:8])
		elif sysex.data[3] == self.map_key_to_note:
			self.current_map[sysex.data[4]] = sysex.data[5]
		elif sysex.data[3] == self.color_knob:
			self.current_knob_colors[sysex.data[4]] = sysex.data[5]
		port.send(sysex)
		time.sleep(self.polling_time)
				
		
	# def is_menu(self, msg=None, state=None):
		# if msg is None:
			# return True if sum(self.current_menus) > 0 else False
		# if msg.type == 'sysex' and list(msg.data[0:4]) == [*self.prefix, self.click]:
			# button = msg.data[4]
			# if button in self.menu:
				# onoff = msg.data[5]
				# self.current_menus[button] = onoff
				# if state == self.pressed:
					# return True if sum(self.current_menus) > 0 else False
				# elif state == self.released:
					# return True if sum(self.current_menus) == 0 else False
		# if state is None:
			# return True if sum(self.current_menus) > 0 else False
		# else:
			# return False
		
	def to_knob(self, button):
		return button - 10
		
	def wait(self):
		time.sleep(self.polling_time)
		
	def to_color(self, color):
		if type(color) is Color:
			return [round(i*127) for i in color.rgb]
		elif type(color) is str:
			return self.to_color(Color(color))
		else:
			raise Warning('Color type not supported')
		
exquis = Exquis()


