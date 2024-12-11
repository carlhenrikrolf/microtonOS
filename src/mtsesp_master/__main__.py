"""
	MTS-ESP Master.
"""

# parameters
client_name = 'MTS-ESP master'

# imports
import mido
import mtsespy as mts
from midi_implementation.mpe import MPE, is_polyexpression
from mtsesp_master.presets import tuning_presets, init_tuning, layout_presets, init_layout
from mtsesp_master.encoders import Encoders
from mtsesp_master.active_sensing import ActiveSensing
from mtsesp_master.isomorphic import isomorphic
from utils import Outport, Inport, make_threads

# script
class Script:
	
	def __init__(self):
		
		self.equave = 0
		self.is_left_right = False
		self.is_up_down = False
		self.transposition = 69
		self.n_tunings = len(tuning_presets)
		self.tuning_pgm = init_tuning
		self.dilation = 3
		self.n_layouts = len(layout_presets)
		self.layout_pgm = init_layout
		self.is_split = False
		self.different_manuals = False
		self.encoders = Encoders(to_isomorphic,
			equave=self.equave,
			transposition=self.transposition,
			n_tunings=self.n_tunings,
			tuning_pgm=self.tuning_pgm,
			dilation=self.dilation,
			n_layouts=self.n_layouts,
			layout_pgm=self.layout_pgm)
		self.is_init = True
		
	def init_touch(self):
		self.encoders.reset()
		self.layout_preset = layout_presets[self.layout_pgm]
		layout = self.layout_preset.layout(dilation=self.dilation,
			is_left_right=self.is_left_right,
			is_up_down=self.is_up_down,
			top_right=self.transposition,
			is_split=self.is_split)
		self.tuning_preset = tuning_presets[self.tuning_pgm]
		coloring = self.tuning_preset.tuning(mts, equave=self.equave)
		isomorphic.send(to_isomorphic, layout=layout, coloring=coloring)
		
	def isomorphic(self, msg):
				
		# initial touch
		if self.is_init:
			self.init_touch()
			self.is_init = False
		
		# encoders
		if self.encoders.refresh(msg):
			layout = self.layout_preset.layout()
			coloring = self.tuning_preset.tuning(mts)
			isomorphic.send(to_isomorphic, layout=layout, coloring=coloring)
		
		# bottom encoders
		equave = self.encoders.change_equave(msg, self.equave)
		if equave is not None:
			self.equave = equave
			coloring = self.tuning_preset.tuning(mts, equave=self.equave)
			isomorphic.send(to_isomorphic, coloring=coloring)
		
		left_right = self.encoders.flip_left_right(msg)
		if left_right is not None:
			self.is_left_right = left_right
			layout = self.layout_preset.layout(is_left_right=self.is_left_right)
			isomorphic.send(to_isomorphic, layout=layout)
		up_down = self.encoders.flip_up_down(msg)
		if up_down is not None:
			self.is_up_down = up_down
			layout = self.layout_preset.layout(is_up_down=self.is_up_down)
			isomorphic.send(to_isomorphic, layout=layout)
		
		# knobs
		transposition = self.encoders.transpose(msg, self.transposition)
		if transposition is not None:
			self.transposition = transposition
			layout = self.layout_preset.layout(top_right=self.transposition)
			isomorphic.send(to_isomorphic, layout=layout)
		reset_keyswitches = self.encoders.reset_keyswitches(msg)
		if reset_keyswitches is not None:
			self.tuning_preset.reset()
		
		tuning_pgm = self.encoders.tuning_preset(msg, self.tuning_pgm)
		if tuning_pgm is not None:
			self.tuning_pgm = tuning_pgm
			self.tuning_preset = tuning_presets[self.tuning_pgm]
			coloring = self.tuning_preset.tuning(mts, equave=self.equave)
			isomorphic.send(to_isomorphic, coloring=coloring)
		different_manuals = self.encoders.differentiate_manuals(msg, self.different_manuals)
		if different_manuals is not None:
			self.different_manuals = different_manuals
		
		dilation = self.encoders.dilate(msg, self.dilation)
		if dilation is not None:
			self.dilation = dilation
			layout = self.layout_preset.layout(dilation=self.dilation)
			isomorphic.send(to_isomorphic, layout=layout)
		dilation = self.encoders.reset_dilation(msg, self.tuning_preset.dilation)
		if dilation is not None:
			self.dilation = dilation
			layout = self.layout_preset.layout(dilation=self.dilation)
			isomorphic.send(to_isomorphic, layout=layout)
		
		layout_pgm = self.encoders.layout_preset(msg, self.layout_pgm)
		if layout_pgm is not None:
			self.layout_pgm = layout_pgm
			self.layout_preset = layout_presets[self.layout_pgm]
			layout = self.layout_preset.layout(dilation=self.dilation,
				is_left_right=self.is_left_right,
				is_up_down=self.is_up_down,
				top_right=self.transposition,
				is_split=self.is_split)
			isomorphic.send(to_isomorphic, layout=layout)
		split = self.encoders.split(msg, self.is_split)
		if split is not None:
			self.is_split = split
			layout = self.layout_preset.layout(is_split=self.is_split)
			isomorphic.send(to_isomorphic, layout=layout)
		
		# notes
		if not isomorphic.ignore(msg): # filter null note (e.g. splitting line)
			if not self.tuning_preset.ignore(msg): # filter nonpositive frequencies
				mpe.dispatch(msg)
			
			
	def halberstadt(self, msg):
		
		if self.is_init:
			self.init_touch()
		
		coloring = None
		if hasattr(msg, 'channel'):
			msg.channel = 13 if is_polyexpression(msg) else 0
		if msg.is_cc(69):
			coloring = self.tuning_preset.footswitch(msg)
		elif hasattr(msg, 'note'):
			if msg.note < 12*3:
				coloring = self.tuning_preset.keyswitches(to_microtonOS, msg, manual=1 if self.different_manuals else 2)
			else:
				self.tuning_preset.halberstadtify(to_microtonOS, msg, manual=1 if self.different_manuals else 2)
		else:
			to_microtonOS.send(msg)
		if coloring is not None:
			isomorphic.send(to_isomorphic, coloring=coloring)
		
		
	def manual2(self,msg):
		
		if self.is_init:
			self.init_touch()
		
		if hasattr(msg, 'channel'):
			msg.channel = 14 if is_polyexpression(msg) else 15
		self.tuning_preset.halberstadtify(to_microtonOS, msg, manual=2)
			


to_isomorphic = Outport(client_name, name='isomorphic', verbose=False)
to_microtonOS = Outport(client_name, name='microtonOS', verbose=False)
mpe = MPE(outport=to_microtonOS, zone='lower', polyphony=12)
active_sensing = ActiveSensing(to_isomorphic)
script = Script()
from_isomorphic = Inport(script.isomorphic, client_name, name='isomorphic', verbose=False)
from_halberstadt = Inport(script.halberstadt, client_name, name='Halberstadt', verbose=False)
from_manual2 = Inport(script.manual2, client_name, name='manual 2', verbose=False)
with mts.Master():
	make_threads([from_isomorphic.open, from_halberstadt.open, from_manual2.open, active_sensing.open])
