# parameters
client_name = 'MTS-ESP master'

# imports
import mido
from midi_implementation.mpe import MPE, is_polyexpression
from mtsesp_master.presets import presets
from mtsesp_master.encoders import Encoders
from mtsesp_master.active_sensing import ActiveSensing
from mtsesp_master.isomorphic import isomorphic
from utils import Outport, Inport, make_threads

# script
class Script:
	
	def __init__(self):
		
		self.is_init = True
		
		self.equave = 0
		self.is_left_right = presets.layout.is_left_right
		self.is_up_down = presets.layout.is_up_down
		self.transposition = presets.layout.top_right
		self.transposition_range = range(0,128)
		self.n_tunings = presets.n_tunings
		self.tuning_pgm = presets.tuning_pgm
		self.dilation = presets.layout.dilation
		self.dilation_range = presets.layout.dilation_range()
		self.n_layouts = presets.n_layouts
		self.layout_pgm = presets.layout_pgm
		self.is_split = False
		
	def isomorphic(self, msg):
		
		if not isomorphic.ignore(msg): # ignore null note
		
			# initial touch
			if self.is_init:
				encoders.reset()
				layout = presets.layout.layout()
				coloring = presets.tuning.coloring()
				isomorphic.send(to_isomorphic, layout=layout, coloring=coloring)
				self.is_init = False
				
			if encoders.refresh(msg):
				layout = presets.layout.layout()
				coloring = presets.tuning.coloring()
				isomorphic.send(to_isomorphic, layout=layout, coloring=coloring)
			
			# bottom encoders
			# change equave
			happened, self.equave = encoders.change_equave(msg, self.equave)
			if happened:
				print('ekvav =', self.equave)
			
			# flip (mirror)
			happened, self.is_left_right = encoders.flip_left_right(msg)
			if happened:
				print('höger--vänster-speglad är', self.is_left_right)
				layout = presets.layout.layout(is_left_right=self.is_left_right)
				isomorphic.send(to_isomorphic, layout=layout)
			happened, self.is_up_down = encoders.flip_up_down(msg)
			if happened:
				print('upp--ner-speglad är', self.is_up_down)
				layout = presets.layout.layout(is_up_down=self.is_up_down)
				isomorphic.send(to_isomorphic, layout=layout)
			
			# knobs
			# transpose
			transpose, self.transposition = encoders.transpose(msg, self.transposition, self.transposition_range)
			if transpose:
				print('transponering =', self.transposition)
			toggle, self.is_split = encoders.toggle_transposition(msg, self.is_split)
			if toggle:
				print('transponering =', self.transposition)
			if transpose: # or toggle
				layout = presets.layout.layout(top_right=self.transposition)
				isomorphic.send(to_isomorphic, layout=layout)
			if toggle:
				layout = presets.layout.layout(is_split=self.is_split)
				isomorphic.send(to_isomorphic, layout=layout)
				
			
			# tuning preset
			happened, self.tuning_pgm = encoders.tuning_preset(msg, self.tuning_pgm)
			if happened:
				print('stämning =', self.tuning_pgm)
			
			# dilate
			dilate, self.dilation = encoders.dilate(msg, self.dilation, self.dilation_range)
			if dilate:
				print('utspädning =', self.dilation)
			toggle, self.dilation = encoders.toggle_dilation(msg, 3)
			if toggle:
				print('utspädning =', self.dilation)
			if dilate or toggle:
				layout = presets.layout.layout(dilation=self.dilation)
				isomorphic.send(to_isomorphic, layout=layout)
			
			# layout preset
			happened, self.layout_pgm = encoders.layout_preset(msg, self.layout_pgm)
			if happened:
				print('layout =', self.layout_pgm)
				presets.change(layout_pgm=self.layout_pgm)
				layout = presets.layout.layout()
				isomorphic.send(to_isomorphic, layout=layout)
			
			# notes
			# sanity check
			if msg.type == 'note_on':
				print('tonen är', msg.note, 'dvs', ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b'][msg.note % 12])
			
			mpe.dispatch(msg)
			
			
	def halberstadt(self, msg):
		
		if hasattr(msg, 'channel'):
			msg.channel = 15 if is_polyexpression(msg) else 0
		to_microtonOS.send(msg)
		
		
	def manual2(self,msg):
		
		if hasattr(msg, 'channel'):
			msg.channel = 14 if is_polyexpression(msg) else 0
		to_microtonOS.send(msg)
			


to_isomorphic = Outport(client_name, name='isomorphic', verbose=False)
to_microtonOS = Outport(client_name, name='microtonOS', verbose=False)
mpe = MPE(outport=to_microtonOS, zone='lower', polyphony=14)
encoders = Encoders(to_isomorphic, # maybe I could move to __init__? or if self.init?
	equave=0,
	equave_range=range(-2,3),
	transposition=presets.layout.top_right,
	n_tunings=presets.n_tunings,
	tuning_pgm=presets.tuning_pgm,
	dilation=presets.layout.dilation,
	n_layouts=presets.n_layouts,
	layout_pgm=presets.layout_pgm,
)
active_sensing = ActiveSensing(to_isomorphic)
script = Script()
from_isomorphic = Inport(script.isomorphic, client_name, name='isomorphic', verbose=False)
from_halberstadt = Inport(script.halberstadt, client_name, name='Halberstadt', verbose=False)
from_manual2 = Inport(script.manual2, client_name, name='manual 2', verbose=False)
make_threads([from_isomorphic.open, from_halberstadt.open, from_manual2.open, active_sensing.open])
