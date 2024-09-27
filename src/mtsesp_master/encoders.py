from midi_implementation.dualo import exquis as xq

def color_coding(number):
	digits = [xq.white, xq.green, xq.yellow, xq.red, xq.magenta, xq.blue, xq.cyan, xq.dark]
	return [digits[number // 8], digits[number % 8]]
	

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

	def __init__(self,
		outport,
		init_equave=0,
		equave_range=range(-2,3),
		init_tuning_program = ...,
		tuning_presets=24,
		init_layout_program = ...,
		layout_presets=4,
		init_transposition=[69]*4,
		transposition_range=[range(...)]*4,
		init_dilation=[3]*4,
		dilation_range=[range(0,8)]*4,
		):
			
		assert layout_presets == len(init_transposition) == len(transposition_range) == len(init_dilation) == len(dilation_range)
		
		self.outport = outport
		self.init_equave = init_equave
		self.equave_range = equave_range
		self.init_tuning_program = init_tuning_program
		self.tuning_presets = tuning_presets
		self.init_layout_program = init_layout_program
		self.layout_presets = layout_presets
		self.init_transposition = init_transposition
		self.transposition_range = transposition_range
		self.init_dilation = init_dilation
		self.dilation_range = dilation_range
		
		self.equave = init_equave
		self.tuning_program = init_tuning_program
		self.layout_program = init_layout_program
		self.transposition = self.init_transposition
		self.dilation = init_dilation
		
		self.custom_tuning = CustomTuning(self.outport)
		self.custom_layout = CustomLayout(self.outport)
		self.is_left_right = False
		self.is_up_down = False
		
	def reset(self):
		xq.send(self.outport, [xq.color_button, xq.octave_up, xq.green])
		xq.send(self.outport, [xq.color_button, xq.octave_down, xq.green])
		xq.send(self.outport, [xq.color_button, xq.page_right, xq.green])
		xq.send(self.outport, [xq.color_button, xq.page_left, xq.green])
		xq.send(self.outport, [xq.color_knob, xq.knob1, color_coding(self.init_tuning_program)[0]])
		xq.send(self.outport, [xq.color_knob, xq.knob2, color_coding(self.init_tuning_program)[1]])
		xq.send(self.outport, [xq.color_knob, xq.knob3, color_coding(self.init_layout_program)[0]])
		xq.send(self.outport, [xq.color_knob, xq.knob4, color_coding(self.init_layout_program)[1]])
		
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
				return {'equave': self.equave,
				'tuning_program': self.tuning_program,
				'layout_program': self.layout_program,
				'transposition': self.transposition[self.layout_program],
				'dilation': self.dilation[self.layout_program],
				'is_left_right': self.is_left_right,
				'is_up_down': self.is_up_down,
				'is_editing': ...,
				'is_custom_tuning': ...,
				'custom_steps': ...,
				'custom_numerator':, ...,
				'custom_denominator': ...,
				'is_custom_layout': ...,
				'custom_up': ...,
				'custom_left': ...,
				'custom_splits': ...,
				}
			return None
			
		
	def is_on(self):
		is_editing = self.custom_tuning.is_editing or self.custom_layout.is_editing
		return not is_editing and not self.is_menu
	
	def equave_up(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.octave_up, xq.pressed]) and self.is_on():
			self.equave += 1 if self.equave+1 in self.equave_range else 0
			if self.equave == self.init_equave:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.green))
			elif self.equave == max(self.equave_range):
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.white))
			else:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.dark)) # update blank
			return True
		return False
	
	def equave_down(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.octave_down, xq.pressed]) and self.is_on():
			self.equave -= 1 if self.equave-1 in self.equave_range else 0
			if self.equave == self.init_equave:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.green))
			elif self.equave == min(self.equave_range):
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.white))
			else:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.dark)) # update blank
			return True
		return False
		
	def flip_left_right(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.page_right, xq.pressed]) and self.is_on():
			self.is_left_right = not self.is_left_right
			if self.is_left_right:
				xq.send(self.outport, [xq.color_button, xq.page_right, xq.white])
			else:
				xq.send(self.outport, [xq.color_button, xq.page_right, xq.green])
			return True
		return False
		
	def flip_up_down(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.page_left, xq.pressed]) and self.is_on():
			self.is_up_down = not self.is_up_down
			if self.is_up_down:
				xq.send(self.outport, [xq.color_button, xq.page_left, xq.white])
			else:
				xq.send(self.outport, [xq.color_button, xq.page_left, xq.green])
			return True
		return False
		
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
		
