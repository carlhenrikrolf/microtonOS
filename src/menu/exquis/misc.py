from midi_implementation.dualo import exquis as xq
from colour import Color

class Misc:
	
	def __init__(self,
		outport,
	):
		self.outport = outport

	def reset(self):
		for menu_button in [xq.settings, xq.record, xq.tracks, xq.scenes, xq.play_stop]:
			xq.send(self.outport, xq.sysex(xq.color_button, menu_button, xq.to_color(Color('black'))))

	def onoff(self, msg):
		return False
