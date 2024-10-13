from .layouts import init_layout, layout_presets
from .tunings import init_tuning, tuning_presets

class Presets:

	def __init__(self):
		self.layout_pgm = init_layout
		self.tuning_pgm = init_tuning
		self.layout = layout_presets[self.layout_pgm]
		self.tuning = tuning_presets[self.tuning_pgm]
		self.n_layouts = len(layout_presets)
		self.n_tunings = len(tuning_presets)
		
	def change(self, layout_pgm=None, tuning_pgm=None):
		if layout_pgm is not None:
			self.layout_pgm = layout_pgm
			top_right = self.layout.top_right
			is_left_right = self.layout.is_left_right
			is_up_down = self.layout.is_up_down
			dilation = self.layout.dilation
			self.layout = layout_presets[self.layout_pgm]
			self.layout.top_right = top_right
			self.layout.is_left_right = is_left_right
			self.layout.is_up_down = is_up_down
			self.layout.dilation = dilation
			
presets = Presets()
