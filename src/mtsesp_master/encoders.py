"""
	These are the encoders (buttons, knobs, sliders) used to control tuning and layout settings.
	Can be altered to fit different kinds of hardware.
"""

from midi_implementation.dualo import exquis as xq

def color_coding(number):
	digits = [xq.dark, xq.lime, xq.yellow, xq.red, xq.magenta, xq.blue, xq.cyan, xq.white]
	return [digits[number // 8], digits[number % 8]]


class BaseCustom: # future work
	
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
			

class Encoders:

	def __init__(self,
		outport,
		equave=0,
		equave_range=range(-2,3),
		transposition=69,
		n_tunings=24,
		tuning_pgm=0,
		dilation=3,
		n_layouts=4,
		layout_pgm=0,
	):
			
		self.outport = outport
		self.equave_range = equave_range
		self.init_equave = equave
		self.n_tunings = n_tunings
		self.init_tuning_pgm = tuning_pgm
		self.n_layouts = n_layouts
		self.init_layout_pgm = layout_pgm
		self.init_transposition = self.transposition = transposition
		self.init_dilation = self.dilation = dilation
		
		self.custom_tuning = CustomTuning(self.outport) # future work
		self.custom_layout = CustomLayout(self.outport) # future work
		self.is_left_right = False
		self.is_up_down = False
		self.transposition_is_toggled = False
		self.dilation_is_toggled = False
		
		
	def reset(self):
		"""
			Resets the LEDs on buttons on Exquis.
			Resets some saved values in this class.
		"""
		if self.init_equave in self.equave_range:
			xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.lime))
			xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.lime))
		else:
			raise Warning('Initial end-point octaves not yet implemented.')
		xq.send(self.outport, xq.sysex(xq.color_button, xq.page_right, xq.lime))
		xq.send(self.outport, xq.sysex(xq.color_button, xq.page_left, xq.lime))
		tuning_code = color_coding(self.init_tuning_pgm)
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob1, tuning_code[0]))
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, tuning_code[1]))
		layout_code = color_coding(self.init_layout_pgm)
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob3, layout_code[0]))
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob4, layout_code[1]))
		
		self.is_left_right = False
		self.is_up_down = False
		self.transposition_is_toggled = False
		self.dilation_is_toggled = False
		self.transposition = self.init_transposition
		self.dilation = self.init_dilation
	
			
		
	def is_on(self): # for compatibility of future work
		is_editing = self.custom_tuning.is_editing or self.custom_layout.is_editing
		return not is_editing
		
	
	def change_equave(self, msg, equave):
		"""
			Given the current equave, this function checks whether it should be incremented or decremented or neither.
		"""
		if xq.is_sysex(msg, [xq.click, xq.octave_up, xq.pressed]) and self.is_on():
			equave = equave+1 if equave+1 in self.equave_range else equave
			if equave == self.init_equave:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.green))
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.green))
			elif equave == max(self.equave_range):
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.dark))
			else:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.white))
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.white))
			return True, equave
		elif xq.is_sysex(msg, [xq.click, xq.octave_down, xq.pressed]) and self.is_on():
			equave = equave-1 if equave-1 in self.equave_range else equave
			if equave == self.init_equave:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.green))
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.green))
			elif equave == min(self.equave_range):
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.dark))
			else:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, xq.white))
				xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_down, xq.white))
			return True, equave
		return False, equave
		
		
	def flip_left_right(self, msg, is_left_right=None):
		"""
			Checks whether the layout should be mirrored left to right.
		"""
		#self.is_left_right = self.is_left_right if is_left_right is None else is_left_right
		if xq.is_sysex(msg, [xq.click, xq.page_right, xq.pressed]) and self.is_on():
			self.is_left_right = not self.is_left_right
			if self.is_left_right:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.page_right, xq.white))
			else:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.page_right, xq.green))
			return True, self.is_left_right
		return False, self.is_left_right
		
		
	def flip_up_down(self, msg, is_up_down=None):
		"""
			Checks whether the layout should be mirrored up to down.
		"""
		#self.is_up_down = self.is_up_down if is_up_down is None else is_up_down
		if xq.is_sysex(msg, [xq.click, xq.page_left, xq.pressed]) and self.is_on():
			self.is_up_down = not self.is_up_down
			if self.is_up_down:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.page_left, xq.white))
			else:
				xq.send(self.outport, xq.sysex(xq.color_button, xq.page_left, xq.green))
			return True, self.is_up_down
		return False, self.is_up_down
		
		
	def transpose(self, msg, transposition, transposition_range):
		"""
			Given a current transposition and a transposition_range,
			the function checks whether to change the transposition,
			and, if so, it rreturns the new transposition.
		"""
		if xq.is_sysex(msg, [xq.clockwise, xq.knob1, None]) and self.is_on():
			transposition = transposition+1 if transposition+1 in transposition_range else transposition
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, None]) and self.is_on():
			transposition = transposition-1 if transposition-1 in transposition_range else transposition
		else:
			return False, transposition
		return True, transposition
		
		
	def toggle_transposition(self, msg, transposition):
		"""
			Given the current transposition,
			the function checks whether it should be reverted to the initial transposition
			or whether to go from the last custom transposition to the initial
		"""
		if xq.is_sysex(msg, [xq.click, xq.button1, xq.pressed]) and self.is_on():
			self.transposition_is_toggled = not self.transposition_is_toggled
			if self.transposition_is_toggled:
				self.transposition = transposition
				return True, self.init_transposition
			else:
				return True, self.transposition
		return False, transposition
		
		
	def tuning_preset(self, msg, tuning_pgm):
		"""
			Given the current tuning
			the function checks whether to increment or decrement
			the current tuning.
		"""
		if xq.is_sysex(msg, [xq.clockwise, xq.knob2, None]) and self.is_on():
			tuning_pgm = tuning_pgm+1 if tuning_pgm+1 < self.n_tunings else tuning_pgm
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob2, None]) and self.is_on():
			tuning_pgm = tuning_pgm-1 if tuning_pgm-1 >= 0 else tuning_pgm
		else:
			return False, tuning_pgm
		code = color_coding(tuning_pgm)
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob1, code[0]))
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, code[1]))
		return True, tuning_pgm
		
		
	def dilate(self, msg, dilation, dilation_range):
		"""
			Given the current dilation
			and the dilation range,
			the function checks whether to increment
			or decrement the dilation.
		"""
		if xq.is_sysex(msg, [xq.clockwise, xq.knob3, None]) and self.is_on():
			self.dilation = dilation+1 if dilation+1 in dilation_range else dilation
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob3, None]) and self.is_on():
			self.dilation = dilation-1 if dilation-1 in dilation_range else dilation
		else:
			return False, dilation
		return True, self.dilation
		
		
	def toggle_dilation(self, msg, min3rd):
		"""
			Given the number of steps in the minor third,
			the function checks whether that value should be used for dilation
			or whether the last used dilation should be in use instead.
		"""
		if xq.is_sysex(msg, [xq.click, xq.button3, xq.pressed]) and self.is_on():
			self.dilation_is_toggled = not self.dilation_is_toggled
			if self.dilation_is_toggled:
				return True, min3rd
			else:
				return True, self.dilation
		return False, self.dilation
		
		
	def layout_preset(self, msg, layout_pgm):
		"""
			Given the current layout and the total number of layouts,
			the function checks whether to increment or decrement
			the layout program.
		"""
		if xq.is_sysex(msg, [xq.clockwise, xq.knob4, None]) and self.is_on():
			layout_pgm = layout_pgm+1 if layout_pgm+1 < self.n_layouts else layout_pgm
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob4, None]) and self.is_on():
			layout_pgm = layout_pgm-1 if layout_pgm-1 >= 0 else layout_pgm
		else:
			return False, layout_pgm
		code = color_coding(layout_pgm)
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob3, code[0]))
		xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob4, code[1]))
		return True, layout_pgm
		
