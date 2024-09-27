from midi_implementation.dualo import exquis as xq

class BaseCustom:
	
	def __init__(self, outport):
		self.is_editing = False

class CustomTuning(BaseCustom):
	
	def edit(self, msg):
		pass # go through all knob inputs

class CustomLayout(BaseCustom):
	
	def edit(self, msg):
		pass

class Encoders

	def __init__(self, outport):
		self.outport = outport
		self.custom_tuning = CustomTuning(self.outport)
		self.custom_layout = CustomLayout(self.outport)
		self.is_left_right = False
		self.is_up_down = False
		self.equave = 0
		self.equaves = range(-2, 3) # shouldnt this go in main file?
		self.transposition = 69
		self.dilation = 3
		self.is_menu = False
		self.tuning_program = ...
		self.layout_program = 0
		
	def handle(self, msg):
		if xq.is_sysex(msg):
			self.is_menu = ...
			self.custom_tuning.is_editing = ...
			self.custom_layout.is_editing = ...
			is_altered = False
			is_altered += self.equave_up(msg)
			is_altered += self.equave_down(msg)
			is_altered += self.flip_left_right(msg)
			is_altered += self.flip_up_down(msg)
			...
			if is_altered:
				self.send()
			
	def send(self):
		...
			
		
	def is_on(self):
		is_editing = self.custom_tuning.is_editing or self.custom_layout.is_editing
		return not is_editing and not self.is_menu
	
	def equave_up(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.octave_up, xq.is_pressed]) and self.is_on():
			pass # move equave up
			# move entire tuning system
			return True
		return False
	
	def equave_down(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.octave_down, xq.is_pressed]) and self.is_on():
			pass # move equave down
			# move entire tuning system
			return True
		return False
		
	def flip_left_right(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.left_right, xq.is_pressed]) and self.is_on():
			pass 
		
	def flip_up_down(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.left_right
		
	def transpose(self, msg):
		...
		
	def tuning_preset(self, msg):
		...
		
	def switch_preset_mos(self, msg):
		...
		
	def dilate(self, msg):
		...
		
	def suggest_dilation(self, msg):
		...
		
	def layout_preset(self, msg):
		...
		
