#! /home/pi/.venv/bin/python3

# parameters
client_name = 'MTS-ESP Master'
verbose = True

# modules
import mido
import mtsespy as mts
import numpy as np
import threading
import time
from midi_implementation.exquis import exquis as xq
from utils import Outport, Inport, make_threads

# definitions
def retune(interval=2.0, n_divisions=12, hz440=440.0, concert_a=69):
	frequencies = [hz440]*128
	for note in range(0,128):
		frequencies[note] = hz440 * interval**(1.0*(note-concert_a)/n_divisions)
	mts.set_note_tunings(frequencies)
	
class EdYoverZinX:
	hz440 = 440.0
	concert_a = 69
	white_keys = [0, 2, 3, 5, 7, 8, 10]
	def __init__(self,
		X: int,
		Y: int,
		Z: int,
		halberstadt: list,
		scale_name='Unnamed',
		bottom_switch=12,
	):
		self.X = X
		self.Y = Y
		self.Z = Z
		self.halberstadt = halberstadt
		self.scale_name = scale_name
		self.bottom_switch = bottom_switch
		self.current_halberstadt = [i if type(i) is int else i[0] for i in self.halberstadt]
	def reset(self):
		mts.set_scale_name(self.scale_name)
		retune(interval=self.Y*1.0/self.Z, n_divisions=self.X, hz440=self.hz440, concert_a=self.concert_a)
		self.current_halberstadt = [i if type(i) is int else i[0] for i in self.halberstadt]
		#xq.transpose(exquis_output, 2) # add dependency on tuning in shift
		self.color_notes()
	def color_notes(self):
		xq.recolor_keys(exquis_output, color=xq.blank)
		for octave in range(0,10):
			for k, n in enumerate(self.current_halberstadt):
				note = self.concert_a + n + self.X*(octave-5)
				if note in xq.get_notes():
					for key in xq.to_keys(note):
						xq.send(exquis_output, xq.sysex(xq.color_key, key, (xq.dark_red if k in self.white_keys else xq.yellow)))
	def halberstadtify(self, note):
		note_letter = (note+12+12*5-self.concert_a) % 12
		octave = (note+12+12*5-self.concert_a) // 12
		return self.current_halberstadt[note_letter] + self.concert_a + self.X*(octave-5)
	def remap(self, msg):
		if msg.type in ['note_on', 'note_off', 'polytouch']:
			if msg.note in range(self.bottom_switch,self.bottom_switch+12) and msg.channel == 0:
				if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
					switch = (msg.note - self.bottom_switch + 12 - 12*5 - self.concert_a) % 12
					if type(self.halberstadt[switch]) is tuple:
						into = (self.halberstadt[switch].index(self.current_halberstadt[switch]) + 1) % len(self.halberstadt[switch])
						self.current_halberstadt[switch] = self.halberstadt[switch][into]
						self.color_notes()
			else:
				note = self.halberstadtify(msg.note)
				if note in range(0,128):
					if msg.type == 'polytouch':
						halberstadt_output.send(
							mido.Message('polytouch', note=note, value=msg.value, channel=msg.channel)
						)
					else:
						halberstadt_output.send(
							mido.Message(msg.type, note=note, velocity=msg.velocity, channel=msg.channel)
						)


# tunings
class Tunings:
	def __init__(self):
		self.tunings = []
		self.tunings.append(
			EdYoverZinX(
				X=12,
				Y=2,
				Z=1,
				halberstadt=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
				scale_name='12edo',
			)
		)
		self.tunings.append(
			EdYoverZinX(
				X=17,
				Y=2,
				Z=1,
				halberstadt=[0, 1, (2,3), 4, (5,6), 7, 8, (9,10), 11, (12,13), 14, (15,16)],
				scale_name='17edo',
			)
		)
		self.tunings.append(
			EdYoverZinX(
				X=19,
				Y=2,
				Z=1,
				halberstadt=[0, (2,1), (3,4), 5, (7,6), 8, (10,9), (11,12), 13, (15,14), 16, (18,17)],
				scale_name='19edo'
			)
		)
		self.tunings.append(
			EdYoverZinX(
				X=24,
				Y=2,
				Z=1,
				halberstadt=[(1,0), (3,4), (4,5), (7,6), (9,8), (11,10), (13,12), (14,15), (17,16), (19,18), (21,20), (23,22)],
				scale_name='24edo',
			)
		)
		self.tunings.append(
			EdYoverZinX(
				X=29,
				Y=2,
				Z=1,
				halberstadt=[0, (2,3), (4,5), 7, (9,10), 12, (14,15), (16,17), 19, (21,22), 24, (26,27)],
				scale_name='29edo',
			)
		)
		self.tunings.append(
			EdYoverZinX(
				X=31,
				Y=2,
				Z=1,
				halberstadt=[(0,1), (3,2), (5,4), 8, (11,10), (13,14), (16,15), (18,17), 21, (24,23), (26,27), (29,28)],
				scale_name='31edo',
			)
		)
		
		

class Script:
	def __init__(self):
		self.tuning_id = 0
		self.left_right = False
		self.up_down = False
		self.width = 3
		self.top_note = 69
		xq.set_map(exquis_output, xq.exquis_layout(width=self.width, top_note=self.top_note), xq.no_crop)
		tunings[self.tuning_id].reset()
	def process_halberstadt(self, msg):
		if msg.type in ['note_on', 'note_off', 'polytouch']:
			if msg.channel == 0:
				msg.note -= 12
		tunings[self.tuning_id].remap(msg)
	def process_exquis(self, msg):
		if not xq.is_menu(msg):
			if xq.is_sysex(msg, [xq.click, xq.button2, xq.pressed]):
				tunings[0].reset()
			switch_tuning = self.switch_tuning(msg)
			if switch_tuning:
				tunings[self.tuning_id].reset()
			self.flip(msg)
			self.shift_notes(msg)
			self.change_width(msg)
			if not xq.is_sysex(msg):
				exquis_output.send(msg)
		if xq.is_menu(msg,xq.released):
			xq.set_map(exquis_output, xq.current_map, xq.current_crop)
			self.resend()
	def color_flip(self):
		if self.left_right:
			xq.send(exquis_output, xq.sysex(xq.color_button, xq.page_right, xq.white))
		else:
			xq.send(exquis_output, xq.sysex(xq.color_button, xq.page_right, xq.green))
		if self.up_down:
			xq.send(exquis_output, xq.sysex(xq.color_button, xq.page_left, xq.white))
		else:
			xq.send(exquis_output, xq.sysex(xq.color_button, xq.page_left, xq.green))
	def flip(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.page_right, xq.pressed]):
			xq.flip_left_right(exquis_output)
			self.left_right = not self.left_right
			self.color_flip()
		elif xq.is_sysex(msg, [xq.click, xq.page_left, xq.pressed]):
			xq.flip_up_down(exquis_output)
			self.up_down = not self.up_down
			self.color_flip()
	def switch_tuning(self, msg):
		switch = True
		if msg.type == 'sysex':
			if msg in [xq.sysex(xq.clockwise, xq.knob2, speed) for speed in xq.speeds]:
				if self.tuning_id == len(tunings) - 1:
					switch = False
				else:
					self.tuning_id += 1
			elif msg in [xq.sysex(xq.counter_clockwise, xq.knob2, speed) for speed in xq.speeds]:
				if self.tuning_id == 0:
					switch = False
				else:
					self.tuning_id -= 1
			else:
				switch = False
		return switch
			
	def shift_notes(self, msg):
		#shift = None
		#if xq.is_sysex(msg, [xq.clockwise, xq.knob1, any]):
		#	#_, shift = xq.is_sysex(msg, [xq.clockwise, xq.knob1, any])
		#	shift = 1
		#elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, any]):
		#	#_, shift = xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, any])
		#	shift = -1
		#if shift is not None:
		#	go = xq.transpose(exquis_output, shift)
		#	if go:
		#		tunings[self.tuning_id].color_notes()
		shifted = True
		if xq.is_sysex(msg, [xq.clockwise, xq.knob1, any]):
			if self.top_note == 127:
				shifted = False
			else:
				self.top_note += 1
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, any]):
			if self.top_note == len(xq.keys) - 1:
				shifted = False
			else:
				self.top_note -= 1
		else:
			shifted = False
		if shifted:
			self.new_layout()
		
	def change_width(self, msg):
		changed = True
		if xq.is_sysex(msg, [xq.clockwise, xq.knob3, any]):
			if self.width == 10:
				changed = False
			else:
				self.width += 1
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob3, any]):
			if self.width == 1:
				changed = False
			else:
				self.width -= 1
		else:
			changed = False
		if changed:
			#xq.set_map(exquis_output, xq.exquis_layout(width=self.width, top_note=69), xq.no_crop)
			#tunings[self.tuning_id].color_notes()
			#if self.left_right:
			#	self.left_right = False
			#	self.flip(xq.sysex(xq.click, xq.page_right, xq.pressed))
			#if self.up_down:
			#	self.up_down = False
			#	self.flip(xq.sysex(xq.click, xq.page_left, xq.pressed))
			self.new_layout()
				
	def new_layout(self):
		xq.set_map(exquis_output, xq.exquis_layout(width=self.width, top_note=self.top_note), xq.no_crop)
		tunings[self.tuning_id].color_notes()
		if self.left_right:
			self.left_right = False
			self.flip(xq.sysex(xq.click, xq.page_right, xq.pressed))
		if self.up_down:
			self.up_down = False
			self.flip(xq.sysex(xq.click, xq.page_left, xq.pressed))
			
	def resend(self):
		tunings[self.tuning_id].color_notes()
		self.color_flip()
	def fire(self):
		period_range = range(1,11)
		step_sigma = 0.3
		sleep_lambda = 100 # ms
		opacity_range = [0.6, 1]
		
		period = list(period_range)[int(len(period_range)/2)]
		while True:
			new_period = period + 1 - np.random.randint(3)
			if new_period in period_range:
				period = new_period
			for step in range(period):
				for key in xq.keys:
					opacity = (np.sin(2*np.pi*np.random.normal(step, step_sigma) / period) + 1) / 2
					opacity *= max(opacity_range) - min(opacity_range)
					opacity += min(opacity_range)
					color = [int(opacity*xq.current_key_colors[key][rgb]) for rgb in range(3)]
					exquis_output.send(xq.sysex(xq.color_key, key, color))
					xq.wait()
				time.sleep(np.random.poisson(sleep_lambda)/1000)
			

# run script
if mts.has_ipc():
	mts.reinitialize()
halberstadt_output = Outport(client_name, name='Halberstadt')
exquis_output = Outport(client_name, name='Exquis', verbose=False)
def active_sensing():
	xq.active_sensing(exquis_output)
t = Tunings()
tunings = t.tunings
script = Script()
halberstadt_inport = Inport(script.process_halberstadt, client_name, name='Halberstadt')
exquis_inport = Inport(script.process_exquis, client_name, name='Exquis')
initialised = [
	halberstadt_inport.open,
	exquis_inport.open,
	active_sensing,
	#script.fire,
]
with mts.Master():
	make_threads(initialised)
	
