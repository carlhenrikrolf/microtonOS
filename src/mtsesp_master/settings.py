from mtsesp_master.layouts import Exquis, HarmonicTable, WickiHayden, Janko
from mtsesp_master.tunings import Default


	
layout_presets = [
	Exquis(11,5,'hexagonal'),
	HarmonicTable(11,5,'hexagonal'),
	WickiHayden(11,5,'hexagonal'),
	Janko(11,5,'hexagonal'),
]

tuning_presets = [
	Default(),
]
	
	

class Init:
	
	equave = 0
	equave_range = range(-2, 3)
	is_left_right = False
	is_up_down = False
	transposition = 69
	transposition_range = range(69,128)
	n_tunings = 24 # len()
	tuning_pgm = 0
	dilation = 3
	dilation_range = range(1,9)
	n_layouts = 4 # len()
	layout_pgm = 0
	
init = Init()
	
	
