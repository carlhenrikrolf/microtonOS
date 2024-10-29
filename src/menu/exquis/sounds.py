from colour import Color
from midi_implementation.dualo import exquis as xq
from config import engine_banks_pgms
from utils import Outport
import mido
				
				
layout = [ # just for reference
	[56, 57, 58, 59, 60, 61],
	[51, 52, 53, 54, 55],
	[45, 46, 47, 48, 49, 50],
	[40, 41, 42, 43, 44],
	[34, 35, 36, 37, 38, 39],
	[29, 30, 31, 32, 33],
	[23, 24, 25, 26, 27, 28],
	[17, 18, 19, 20, 21],
	[11, 12, 13, 14, 15, 16],
   	[6, 7, 8, 9, 10],
    [0, 1, 2, 3, 4, 5],
]

engines = [56, 57, 58, 59, 60, 61, 51, 52, 53, 54, 55, 45, 46, 47, 48, 49, 50]
banks = [34, 35, 36, 37, 38, 39, 29, 30, 31, 32, 33, 23, 24, 25, 26, 27, 28]
pgms = [11, 12, 13, 14, 15, 16, 6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5]


class Sounds:
	
	def __init__(self,
		outport,
		two_is_connected=lambda: False,
		three_is_connected=lambda: False,
		four_is_connected=lambda: False,
		base_color=Color('purple'),
		click_color=Color('white'),
	):
		self.outport = outport
		self.two_is_connected = two_is_connected
		self.three_is_connected = three_is_connected
		self.four_is_connected = four_is_connected
		self.base_color = xq.to_color(base_color)
		self.click_color = xq.to_color(click_color)
		self.engine = 0
		self.bank = 0
		self.pgm = 0
		
		self.n_engines = len(engine_banks_pgms)
		self.n_banks = 0
		self.n_pgms = 0
	
	def select(self, msg):
		
		if xq.is_sysex(msg, [xq.click, xq.sounds, xq.pressed])
			
			for key in xq.keys:
				xq.send(self.outport, [xq.key_to_note, key, key])
			for i, key in enumerate(engines):
				if i < self.n_engines:
					xq.send(self.outport, xq.sysex(xq.color_key, key, self.base_color))
				else:
					break
			for key in range(i,61):
				xq.send(self.outport, [xq.color_key, key, xq.to_color('black')])
			for button in [xq.octave_up, xq.octave_down, xq.page_left, xq.page_right]:
				xq.send(self.outport, xq.sysex(xq.color_button, button, xq.to_color('black')
			
			xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob1, self.click_color))
			xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, self.click_color if self.two_is_connected() else xq.to_color('black')))
			xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, self.click_color if self.three_is_connected() else xq.to_color('black')))
			xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, self.click_color if self.four_is_connected() else xq.to_color('black')))
			
			self.n_banks = 0
			self.n_pgms = 0
					
		elif msg.type == 'note_on':
			
			if msg.note in engines:
				i = engines.index(msg.note)
				if i < self.n_engines:
					xq.send(self.outport, xq.sysex(xq.color_key, msg.note, self.click_color))
					self.engine = i
					self.n_banks = len(engine_banks_pgms[self.engine][1])
					self.n_pgms = 0
					if self.n_banks <= 1:
						return Outport(name=engine_banks_pgms[self.engine][0], client_name=self.client_name), mido.Message('control_change', control=0, value=0), mido.Message('program_change', 0)
					for j, key in enumerate(banks):
						if j <= self.n_banks:
							xq.send(self.outport, [xq.color_key, key, self.base_color])
						else:
							break
			
			elif msg.note in banks and self.n_banks > 0:
				i = banks.index(msg.note)
				if i < self.n_banks:
					xq.send(self.outport, xq.sysex(xq.color_key, msg.note, self.click_color))
					self.bank = i
					self.n_pgms = round(engine_banks_pgms[self.engine][1][self.bank])
					if self.n_pgms <= 1:
						return Outport(name=engine_banks_pgms[self.engine][0], client_name=self.client_name), mido.Message('control_change', control=0, value=0), mido.Message('program_change', self.bank)
					for j, key in enumerate(self.pgms):
						if j < self.n_pgms:
							xq.send(self.outport, xq.sysex(xq.color_key, key, self.base_color))
						else:
							break 
			
			elif msg.note in pgms and self.n_pgms > 0:
				i = programs.index(msg.note)
				if i <= engine_banks_pgms[self.engine][1][self.bank]:
					xq.send(self.outport, xq.sysex(xq.color_key, msg.note, self.click_color))
					self.pgm = i
					return Outport(name=engine_banks_pgms[self.engine][0], client_name=self.client_name), mido.Message('control_change', control=0, value=self.bank), mido.Message('program_change', self.pgm)
				
		return None
		
		
	def two(self, msg):
		if self.two_is_connected():
			if xq.is_sysex(msg, [xq.clockwise, xq.knob2, None]):
				return True
			elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob2, None]):
				return False
		else:
			return None
			
		
		
