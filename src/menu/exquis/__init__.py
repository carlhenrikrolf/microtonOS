from .sounds import Sounds
from .utils import layout, to_key
from colour import Color
from midi_implementation.dualo import Exquis as xq

menu_buttons = [
	xq.settings,
	xq.sounds,
	xq.record,
	xq.tracks,
	xq.scenes,
	xq.play_stop,
]

sounds = Sounds()

class Menu:

	def __init__(self, outport):
		
		self.outport = outport
		self.is_init = True
		self.is_on = False
		self.button_is_pressed = [False]*len(menu_buttons)


	def run(self, msg):
		
		if self.is_init:
			xq.send(self.outport, xq.sysex(xq.color_button, xq.settings, xq.to_color(Color('black')))
			xq.send(self.outport, xq.sysex(xq.color_button, xq.sounds, xq.to_color(Color('chartreuse')))
			xq.send(self.outport, xq.sysex(xq.color_button, xq.record, xq.to_color(Color('black')))
			xq.send(self.outport, xq.sysex(xq.color_button, xq.tracks, xq.to_color(Color('black')))
			xq.send(self.outport, xq.sysex(xq.color_button, xq.scenes, xq.to_color(Color('black')))
			xq.send(self.outport, xq.sysex(xq.color_button, xq.play_stop, xq.to_color(Color('black')))
			self.is_init = False
			
		if self.button_is_pressed[menu_buttons.index(xq.sounds)]:
			sounds.run(msg)
			
			
			
	def reset(self, msg):
		
		for key in xq.keys:
			xq.send(xq.
		
			
		
			
	def is_on(self, msg=None):
		
		if msg is not None:
			for i, menu_button in enumerate(menu_buttons):
				if xq.is_sysex(msg, [xq.click, menu_button, xq.pressed]):
					self.button_is_pressed[i] = True
				elif xq.is_sysex(msg, [xq.click, menu_button, xq.released]):
					self.button_is_pressed[i] = False
		return max(self.button_is_pressed)
		
		
	def is_off(self, msg=None):
		
		if msg is not None:
			for i, menu_button in enumerate(menu_buttons):
				if xq.is_sysex(msg, [xq.click, menu_button, xq.pressed]):
					self.button_is_pressed[i] = True
				elif xq.is_sysex(msg, [xq.click, menu_button, xq.released]):
					self.button_is_pressed[i] = False
					return max(self.button_is_pressed)
		return False
		

