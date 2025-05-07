import mido
import time
from colour import Color

manufacturer_id = [0x00, 0x21, 0x7E]

class Exquis: # version 1.2.0
		
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
				mido.Message('sysex', data=manufacturer_id)
			)
			time.sleep(sleep)
			
	def is_active_sensing(self, msg=None):
		if type(msg) is None:
			return (time.perf_counter_ns() - self.last_sensing <= 1e9)
		elif (msg.type == 'sysex') and (list(msg.data) == manufacturer_id):
			self.last_sensing = time.perf_counter_ns()
			return True
		else:
			return False
			
	
	def sysex(self, action=[], control=[], state=[]):
		if ([] in [action, control, state]) or (None in [action, control, state]):
			return mido.Message('sysex', data=manufacturer_id)
		else:
			if type(state) is list:
				return mido.Message('sysex', data=[*manufacturer_id, action, control, *state])
			else:
				return mido.Message('sysex', data=[*manufacturer_id, action, control, state])
				
	def is_sysex(self, msg, data=None):
		if msg.type == 'sysex':
			indata = list(msg.data)
			if data is None:
				if indata[0:3] == manufacturer_id:
					return True
				else:
					return False
			else:
				if data[2] is None:
					if indata[3:5] == data[0:2]:
						return True #, (indata[5] if len(indata[5:]) == 1 else indata[5:])
					else:
						return False
				elif type(data[2]) is list:
					if indata == [*manufacturer_id, data[0], data[1], *data[2]]:
						return True
					else:
						return False
				else:
					if indata == [*manufacturer_id, data[0], data[1], data[2]]:
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

	def rotation(self, msg):
		if msg.type == 'sysex':
			indata = list(msg.data)
			if indata[0:4] == [*manufacturer_id, self.clockwise]:
				return int(indata[5])
			elif indata[0:4] == [*manufacturer_id, self.counter_clockwise]:
				return -int(indata[5])
		return None
		
	def to_knob(self, button):
		return button - 10
	
	def to_button(self, knob):
		return knob + 10
		
	def wait(self):
		time.sleep(self.polling_time)
		
	def led(self, color):
		if type(color) is Color:
			return [round(i*127) for i in color.rgb]
		elif type(color) is str:
			return self.led(Color(color))
		else:
			raise Warning('Color type not supported')
		
	def brightness(self, level: float, outport=None):
		if outport is None:
			return mido.Message("sysex")

exquis = Exquis()

exquis_v1_2_0 = Exquis()


class Exquis200:

	# exquis receives
	mpe_poly = 7
	pad_remote = 30
	luminosity = 5 # 0 to 100 # strange above 120
	slider_remote = 60
	slider_color = 61
	sliders = [i for i in range(6)]
	button_remote = 40
	knob_remote = 51
	color_knob = 51
	on = 1
	off = 0
	color_key = 31
	color_note = 20
	map_key_to_note = 21

	knob1 = exquis_v1_2_0.knob1
	knob2 = exquis_v1_2_0.knob2
	knob3 = exquis_v1_2_0.knob3
	knob4 = exquis_v1_2_0.knob4

	# exquis transmits
	button_click = 42
	pad_click = 32 # commence en haut à gauche
	knob_turn = 53 # 0 to 5 knob number # sounds unfinished?

	sounds = exquis_v1_2_0.sounds
	record = exquis_v1_2_0.record
	loops = exquis_v1_2_0.loops
	tracks = loops
	snaps = exquis_v1_2_0.snaps
	scenes = snaps
	octave_up = exquis_v1_2_0.octave_down # switch?
	octave_down = exquis_v1_2_0.octave_up # switch?
	page_left = exquis_v1_2_0.page_left
	page_right = exquis_v1_2_0.page_right


	def led(self, color):
		if type(color) is str:
			color = Color(color)
		result = [0]*3
		for i, j in enumerate(color.rgb):
			result[i] = round(j * 127)
		return result
	
	def mpe(self, turn_on: bool, outport=None):
		last_byte = self.on if turn_on else self.off
		data = [*manufacturer_id, self.mpe_poly, last_byte]
		sysex = mido.Message("sysex", data)
		if outport is None:
			return sysex
		else:
			outport.send(sysex)
	
	def brightness(self, level: float, outport=None):
		assert 0 <= level <= 1
		level = round(level*100)
		data = [*manufacturer_id, self.luminosity, level]
		sysex = mido.Message("sysex", data)
		if outport is None:
			return sysex
		else:
			outport.send(sysex)


class Exquis213:

	prefix = [*manufacturer_id, 0x7F]

	setup_developer_mode = 0x00

	# Below requires develoment mode to be active
	scale_list = 0x01
	color_palette = 0x02
	refresh = 0x03
	led_color = 0x04
	tempo = 0x05
	root_note = 0x06
	scale_number = 0x07
	custom_scale = 0x08
	snapshot = 0x09

	# Below can be added to setup developer mode
	pads = 0x01
	encoders = 0x02
	slider = 0x03
	up_down = 0x08
	settings_sound = 0x10
	misc_buttons = 0x20
	all_buttons = pads + encoders + slider + up_down + settings_sound + misc_buttons


	def developer_mode(self,
		action,
		pads=True,
		encoders=True,
		slider=True,
		up=True,
		down=True,
		settings=True,
		sound=True,
		misc=True,
	):
		"""Enter or exit developer mode."""
		assert action in ["enter", "exit"]
		mode = 0
		if action == "enter":
			if pads:
				mode += self.pads
			if encoders:
				mode += self.encoders
			if slider:
				mode += self.slider
			if up or down:
				mode += self.up_down
			if settings or sound:
				mode += self.settings_sound
			if misc:
				mode += self.misc_buttons
		data = [*self.prefix, self.setup_developer_mode, mode]
		msg = mido.Message("sysex", data)
		return msg

def use_scales(self, number):
	"""Specify the number of scales to be selectable in the setting menu."""
	if number in range(0,256):
		data = [*self.prefix, self.scale_list, number // 128, number % 128]
	else:
		data = [*self.prefix, self.scale_list]
	msg = mido.Message("sysex", data)
	return msg

def get_color_palette(self, msg=None, index=None):
	"""Request the entire color palette or a specific index. Analyse response"""
	assert index in range(0,128)
	data = [*self.prefix, self.color_palette]
	prefix_len = len(data)
	if msg is None:
		if index is None:
			return mido.Message("sysex", data)
		else:
			data.append(index)
			return mido.Message("sysex", data)
	elif msg.type == "sysex" and msg.data[:prefix_len] == data:
		entire_palette = len(msg.data) == prefix_len + 128*3
		single_color = len(msg.data) == prefix_len + 3
		if entire_palette:
			palette = []*128
			for n, i in enumerate(range(prefix_len, prefix_len + 3*128, 3)):
				color = Color()
				color.rgb = [j/128.0 for j in msg.data[i:i+3]]
				palette[n] = color
		elif single_color:
			palette = Color()
			palette.rgb = [j/128.0 for j in msg.data[prefix_len:]]
		else:
			return None
		return palette
	else:
		return None
	
def set_color_palette(self):
	...
	




