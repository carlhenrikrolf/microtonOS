import mido
import time

class Exquis:
	
	prefix = [0x00, 0x21, 0x7E]
	
	# mapping keys to notes
	default_map = [27, 28, 29, 30, 31, 32, 31, 32, 33, 34, 35, 34, 35, 36, 37, 38, 39, 38, 39, 40, 41, 42, 41, 42, 43, 44, 45, 46, 45, 46, 47, 48, 49, 48, 49, 50, 51, 52, 53, 52, 53, 54, 55, 56, 55, 56, 57, 58, 59, 60, 59, 60, 61, 62, 63, 62, 63, 64, 65, 66, 67] 
	default_crop = [0,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,0]
	equals_keys_map = list(range(0,61))
	no_crop = [0]*61
	
	# controls
	buttons = range(0,10)
	menu = range(0,6)
	knobs = range(0,5)
	settings = 0
	sounds = 1
	record = 2
	loops = 3
	snaps = 4
	start_stop = 5
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
	notes = set(default_map)
	
	blank = [0x00, 0x00, 0x00]
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
	
	default_key_colors = [[0,0,0]]*61
	
	polling_time = 0.0005
	
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
	
	def __init__(self):
		self.last_sensing = time.perf_counter_ns()
		self.current_map = [27, 28, 29, 30, 31, 32, 31, 32, 33, 34, 35, 34, 35, 36, 37, 38, 39, 38, 39, 40, 41, 42, 41, 42, 43, 44, 45, 46, 45, 46, 47, 48, 49, 48, 49, 50, 51, 52, 53, 52, 53, 54, 55, 56, 55, 56, 57, 58, 59, 60, 59, 60, 61, 62, 63, 62, 63, 64, 65, 66, 67] 
		self.current_crop = [0,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,1, 1,0,0,0,1, 1,0,0,0,0,0]
		self.current_key_colors = [[0,0,0]]*61
		self.current_knob_colors = [0,0,0,0]
		self.current_menus = [self.released]*len(self.menu)
	
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
				if data[2] is any:
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
		
	def to_keys(self, note):
		keys = []
		if note in self.get_notes():
			for k, n in enumerate(self.current_map):
				if n == note:
					keys.append(k)
		return keys
	
	def to_note(self, key):
		return self.current_map[key]
		
	def all_lights_off(self, port):
		for button in self.buttons:
			port.send(self.sysex(self.color_button, button, self.blank))
		for knob in self.knobs:
			port.send(self.sysex(self.color_knob, knob, self.blank))
		for key in self.keys:
			port.send(self.sysex(self.color_key, key, self.blank))
			
	def get_row_col(self,key):
		row = 0
		col = key
		while col >= (6 if row % 2 == 0 else 5):
			col -= 6 if row % 2 == 0 else 5
			row += 1
		return row, col
		
	def get_key(self,row,col):
		key = sum(6 if i % 2 == 0 else 5 for i in range(row))
		return key + col
			
	def flip_up_down(self, port):
		new_keys = [0]*61
		for current_key in self.keys:
			row, col = self.get_row_col(current_key)
			new_row = 10 - row
			new_keys[current_key] = self.get_key(new_row, col)
		new_map =  [0]*61
		new_key_colors = [[0,0,0]]*61
		new_crop = [0]*61
		for current_key, new_key in enumerate(new_keys):
			new_map[current_key] = self.current_map[new_key]
			new_key_colors[current_key] = self.current_key_colors[new_key]
			new_crop[current_key] = self.current_crop[new_key]
		self.current_map = new_map
		self.current_key_colors = new_key_colors
		self.current_crop = new_crop
		self.remap_notes(port)
		self.recolor_keys(port)
	
	def flip_left_right(self, port):
		new_keys = [0]*61
		for current_key in self.keys:
			row, col = self.get_row_col(current_key)
			new_col = (5 if (row % 2) == 0 else 4) - col
			new_keys[current_key] = self.get_key(row, new_col)
		new_map = [0]*61
		new_key_colors = [[0,0,0]]*61
		new_crop = [0]*61
		for current_key, new_key in enumerate(new_keys):
			new_map[current_key] = self.current_map[new_key]
			new_key_colors[current_key] = self.current_key_colors[new_key]
			new_crop[current_key] = self.current_crop[new_key]
		self.current_map = new_map
		self.current_key_colors = new_key_colors
		self.current_crop = new_crop
		self.remap_notes(port)
		self.recolor_keys(port)
		
		
	def reset(self,port,action=None):
		self.current_map = self.default_map
		self.current_key_colors = self.default_key_colors
		for key, note in enumerate(self.current_map):
			port.send(self.sysex(self.map_key_to_note, key, note))	
	
	def send(self, port, sysex):
		ignore = False
		if sysex.data[3] == self.color_key:
			if self.current_crop[sysex.data[4]]:
				ignore = True
			else:
				self.current_key_colors[sysex.data[4]] = list(sysex.data[5:8])
		elif sysex.data[3] == self.map_key_to_note:
			self.current_map[sysex.data[4]] = sysex.data[5]
		elif sysex.data[3] == self.color_knob:
			self.current_knob_colors[sysex.data[4]] = sysex.data[5]
		if not ignore:
			port.send(sysex)
			time.sleep(self.polling_time)
		
	def remap_notes(self, port):
		for key, note in enumerate(self.current_map):
			port.send(self.sysex(self.map_key_to_note, key, note))
			time.sleep(self.polling_time)
		
	def recolor_keys(self, port, color=None):
		for key in self.keys:
			port.send(self.sysex(self.color_key, key, self.blank))
			time.sleep(self.polling_time)
		if color is None:
			for key in self.keys:
				port.send(self.sysex(self.color_key, key, self.current_key_colors[key]))
				time.sleep(self.polling_time)
		else:
			for key in self.keys:
				self.send(port,self.sysex(self.color_key, key, color))
				
	def get_notes(self):
		return set(self.current_map)
		
	def is_menu(self, msg=None, state=None):
		if msg is None:
			return True if sum(self.current_menus) > 0 else False
		if msg.type == 'sysex' and list(msg.data[0:4]) == [*self.prefix, self.click]:
			button = msg.data[4]
			if button in self.menu:
				onoff = msg.data[5]
				self.current_menus[button] = onoff
				if state == self.pressed:
					return True if sum(self.current_menus) > 0 else False
				elif state == self.released:
					return True if sum(self.current_menus) == 0 else False
		if state is None:
			return True if sum(self.current_menus) > 0 else False
		else:
			return False
		
	
	def set_map(self, port, new_map, new_crop):
		for key in self.keys:
			self.current_key_colors[key] = self.blank
			port.send(self.sysex(self.color_key, key, self.blank))
			time.sleep(self.polling_time)
		self.current_map = new_map
		self.current_crop = new_crop
		self.remap_notes(port)
		
		
				
	def test(self):
		return mido.open_output('Exquis MIDI 1')
		
	def to_knob(self, button):
		return button - 10
		
	def wait(self):
		time.sleep(self.polling_time)
		
	def transpose(self, port, shift):
		new_map = self.default_map
		for key in self.keys:
			new_map[key] = self.current_map[key] + shift
			if not (new_map[key] in range(0,128)):
				return False
		self.set_map(port, new_map, self.current_crop)
		return True
		
		
			
		
exquis = Exquis()


