from midi_implementation.dualo import exquis as xq

def color_coding(number):
	digits = [xq.white, xq.green, xq.yellow, xq.red, xq.magenta, xq.blue, xq.cyan, xq.dark]
	return [digits[number // 8], digits[number % 8]]
	

class BaseCustom:
	
	def __init__(self, outport):
		self.is_editing = False
		

class CustomTuning(BaseCustom): # future work
	
	def edit(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.button2, xq.pressed]):
			self.is_editing = True
		elif xq.is_sysex(msg, [xq.click, xq.button2, xq.released]):
			self.is_editing = False
		else:
			return False
		return True
			

class CustomLayout(BaseCustom): # future work
	
	def edit(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.button4, xq.pressed]):
			self.is_editing = True
		elif xq.is_sysex(msg, [xq.click, xq.button4, xq.released]):
			self.is_editing = False
		else:
			return False
		return True
			

class Encoders

	def __init__(self,
		outport,
		init_equave=0,
		equave_range=range(-2,3),
		init_tuning_program = ...,
		tuning_presets=24,
		init_layout_program = ...,
		layout_presets=4,
		init_transposition=69,
		init_dilation=3,
		):
			
		self.outport = outport
		self.init_equave = init_equave
		self.equave_range = equave_range
		self.init_tuning_program = init_tuning_program
		self.tuning_presets = tuning_presets
		self.init_layout_program = init_layout_program
		self.layout_presets = layout_presets
		self.init_transposition = init_transposition
		self.transposition_range = ...
		self.init_dilation = init_dilation
		self.dilation_range = ... 
		
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
		tuning_code = color_coding(self.init_tuning_program)
		xq.send(self.outport, [xq.color_knob, xq.knob1, tuning_code[0]])
		xq.send(self.outport, [xq.color_knob, xq.knob2, tuning_code[1]])
		layout_code = color_coding(self.init_layout_program)
		xq.send(self.outport, [xq.color_knob, xq.knob3, layout_code[0]])
		xq.send(self.outport, [xq.color_knob, xq.knob4, layout_code[1]])
	
	
	def handle(self,
		msg,
		transposition_range,
		dilation_range,
		is_mos,
		min3rd,
		):
			
		self.transposition_range = transposition_range
		if self.transposition not in self.transposition_range:
			...
		self.dilation_range = dilation_range
		if self.dilation not in self.dilation_range:
			...
		self.is_mos = is_mos
		self.min3rd = min3rd
		
		is_encoder = False
		if xq.is_sysex(msg):
			# tuning
			is_encoder += self.equave_up(msg)
			is_encoder += self.equave_down(msg)
			is_encoder += self.transpose(msg)
			is_encoder += self.switch_preset_mos(msg)
			is_encoder += self.tuning_preset(msg)
			is_encoder += self.custom_tuning.edit(msg)
			# layout
			is_encoder += self.flip_left_right(msg)
			is_encoder += self.flip_up_down(msg)
			is_encoder += self.dilate(msg)
			is_encoder += self.suggest_dilation(msg)
			is_encoder += self.layout_preset(msg)
			is_encoder += self.custom_layout.edit(msg)
		return bool(is_encoder)
			
		
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
		if xq.is_sysex(msg, [xq.clockwise, xq.knob1, None]) and self.is_on():
			self.transpose += 1 if self.transpose+1 in self.transpose_range else 0
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, None]) and self.is_on():
			self.transpose -= 1 if self.transpose-1 in self.transpose_range else 0
		else:
			return False
		return True
		
		
	def switch_preset_mos(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.button1, xq.pressed]) and self.is_on():
			self.is_mos = not self.is_mos
			return True
		return False
		
		
	def tuning_preset(self, msg):
		if xq.is_sysex(msg, [xq.clockwise, xq.knob2, None]) and self.is_on():
			self.tuning_program += 1 if self.tuning_program+1 in range(self.tuning_presets) else 0
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob2, None]) and self.is_on():
			self.tuning_program -= 1 if self.tuning_program-1 in range(self.tuning_presets) else 0
		else:
			return False
		code = color_coding(self.tuning_program)
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob1, code[0]))
 		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, code[1]))
 		return True
		
		
	def dilate(self, msg):
		if xq.is_sysex(msg, [xq.clockwise, xq.knob3, None]) and self.is_on():
			self.dilation += 1 if self.dilation+1 in self.dilation_range else 0
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob3, None]) and self.is_on():
			self.dilation -= 1 if self.dilation-1 in self.dilation_range else 0
		else:
			return False
		return True
		
		
	def suggest_dilation(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.button3, xq.pressed]) and self.is_on():
			self.dilation = self.min3rd
			return True
		return False
		
		
	def layout_preset(self, msg):
		if xq.is_sysex(msg, [xq.clockwise, xq.knob4, None]) and self.is_on():
			self.layout_program += 1 if self.layout_program+1 in range(self.layout_presets) else 0
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob2, None]) and self.is_on():
			self.layout_program -= 1 if self.layout_program-1 in range(self.layout_presets) else 0
		else:
			return False
		code = color_coding(self.layout_program)
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob3, code[0]))
 		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob4, code[1]))
 		return True
		
