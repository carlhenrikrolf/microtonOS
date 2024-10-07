#! /home/pi/.venv/bin/python3

# reminder: make halberstadt port on mtsesp depend on channels with 0 as master channel (with clickable keys oand octave shift)

# parameters
client_name = 'Router'
engines = [
	'Pianoteq Wrapper',
	'tuneBfree Wrapper',
	'Surge XT Wrapper',
	'Reface CP Wrapper',
]
pianoteq_presets = [6, 4, 5, 2]
surge_xt_presets = [3, 6, 5, 6]
tuneBfree_presets = [6, 6, 6]
reface_cp_presets = [0]

# modules
import mido
import subprocess
import time
from utils import Inport, Outport, make_threads
from utils import NewEngine as Engine
from midi_implementation.exquis import exquis as xq
from midi_implementation.reface_cp import reface_cp as cp

# definitions
def is_connected(name):
	is_input = max([name in n for n in mido.get_input_names()])
	is_output = max([name in n for n in mido.get_output_names()])
	return is_input or is_output

class Sounds:
	exquis = xq.button1
	reface_cp = xq.button2
	
	def __init__(self):
		self.current_device = None
		self.banks = None
		self.current_bank = None
		self.presets = None
		self.programs = None
		self.volumes = [127]*len(engines)
		
	def reset(self):
		xq.recolor_keys(to_exquis, xq.blank)
		xq.send(to_exquis, xq.sysex(xq.color_button, xq.sounds, xq.blue))
		xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.exquis), xq.blue))
		if is_connected('reface CP MIDI 1'):
			xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.reface_cp), xq.blue))
		self.current_device = None
		self.banks = None
		self.current_bank = None
		self.presets = None
		self.programs = None
		
	def reset_engines(self):
		for key in range(0, 55+6):
			xq.send(to_exquis, xq.sysex(xq.color_key, key, xq.blank))
		for i, engine in enumerate(engines):
			if engine == 'Reface CP Wrapper' and not is_connected('reface CP MIDI 1'):
				continue
			else:
				xq.send(to_exquis, xq.sysex(xq.color_key, i+55, xq.blue))
				
	def reset_banks(self):
		for key in range(0, 44+6):
			xq.send(to_exquis, xq.sysex(xq.color_key, key, xq.blank))
		if len(self.banks) > 1:
			for bank in self.banks:
				xq.send(to_exquis, xq.sysex(xq.color_key, 44+bank, xq.blue))
				
	def reset_programs(self):
		for key in range(0, 33+6):
			xq.send(to_exquis, xq.sysex(xq.color_key, key, xq.blank))
		if self.programs > 1:
			for program in range(self.programs):
				xq.send(to_exquis, xq.sysex(xq.color_key, 33+program, xq.blue))
				
	def menu(self, msg):
		if xq.is_sysex(msg, [xq.click, xq.sounds, xq.pressed]):
			self.reset()
		elif xq.is_sysex(msg, [xq.click, self.exquis, xq.pressed]):
			self.reset()
			xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.exquis), xq.white))
			self.current_device = self.exquis
			self.reset_engines()
		elif xq.is_sysex(msg, [xq.click, self.reface_cp, xq.pressed]):
			if is_connected('reface CP MIDI 1'):
				self.reset()
				xq.send(to_exquis, xq.sysex(xq.color_key, xq.to_knob(self.reface_cp), xq.white))
				self.current_device = self.reface_cp
				self.reset_engines()
				
		elif xq.is_sysex(msg, [xq.clockwise, xq.to_knob(self.exquis), any]):
			_, louder = xq.is_sysex(msg, [xq.clockwise, xq.to_knob(self.exquis), any])
			previous_volume = self.volumes[engines.index(exquis_to_engine.name)]
			current_volume = min([127, previous_volume + louder])
			self.volumes[engines.index(exquis_to_engine.name)] = current_volume
			exquis_to_engine.send(mido.Message('control_change', control=7, value=current_volume))
			color = xq.white if self.current_device == self.exquis else xq.blue
			new_color = [int(current_volume*color[rgb]*1.0/127) for rgb in range(3)] 
			xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.exquis), new_color))
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.to_knob(self.exquis), any]):
			_, quieter = xq.is_sysex(msg, [xq.counter_clockwise, xq.to_knob(self.exquis), any])
			previous_volume = self.volumes[engines.index(exquis_to_engine.name)]
			current_volume = max([0, previous_volume - quieter])
			self.volumes[engines.index(exquis_to_engine.name)] = current_volume
			exquis_to_engine.send(mido.Message('control_change', control=7, value=current_volume))
			color = xq.white if self.current_device == self.exquis else xq.blue
			new_color = [int(current_volume*color[rgb]*1.0/127) for rgb in range(3)] 
			xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.exquis), new_color))
			
		elif xq.is_sysex(msg, [xq.clockwise, xq.to_knob(self.reface_cp), any]):
			_, louder = xq.is_sysex(msg, [xq.clockwise, xq.to_knob(self.reface_cp), any])
			previous_volume = self.volumes[engines.index(reface_cp_to_engine.name)]
			current_volume = min([127, previous_volume + louder])
			self.volumes[engines.index(reface_cp_to_engine.name)] = current_volume
			reface_cp_to_engine.send(mido.Message('control_change', control=7, value=current_volume))
			color = xq.white if self.current_device == self.reface_cp else xq.blue
			new_color = [int(current_volume*color[rgb]*1.0/127) for rgb in range(3)] 
			xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.reface_cp), new_color))
		elif xq.is_sysex(msg, [xq.counter_clockwise, xq.to_knob(self.reface_cp), any]):
			_, quieter = xq.is_sysex(msg, [xq.counter_clockwise, xq.to_knob(self.reface_cp), any])
			previous_volume = self.volumes[engines.index(reface_cp_to_engine.name)]
			current_volume = max([0, previous_volume - quieter])
			self.volumes[engines.index(reface_cp_to_engine.name)] = current_volume
			reface_cp_to_engine.send(mido.Message('control_change', control=7, value=current_volume))
			color = xq.white if self.current_device == self.reface_cp else xq.blue
			new_color = [int(current_volume*color[rgb]*1.0/127) for rgb in range(3)] 
			xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.reface_cp), new_color))
		
		elif msg.type == 'note_on':
			if (self.current_device is not None) and msg.note in range(55, 55+len(engines)):
				engine = engines[msg.note - 55]
				if self.current_device == self.exquis:
					self.reset_engines()
					xq.send(to_exquis, xq.sysex(xq.color_key, msg.note, xq.white))
					exquis_to_engine.change(engine)
				elif self.current_device == self.reface_cp:
					self.reset_engines()
					xq.send(to_exquis, xq.sysex(xq.color_key, msg.note, xq.white))
					reface_cp_to_engine.change(engine)
				if exquis_to_engine.name == reface_cp_to_engine.name:
					if exquis_to_engine.name != 'Reface CP Wrapper' or is_connected('reface CP MIDI 1'):
						xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.exquis), xq.white))
						xq.send(to_exquis, xq.sysex(xq.color_knob, xq.to_knob(self.reface_cp), xq.white))
				if engine == 'Pianoteq Wrapper':
					self.banks = range(len(pianoteq_presets))
					self.presets = pianoteq_presets
				elif engine == 'tuneBfree Wrapper':
					self.banks = range(len(tuneBfree_presets))
					self.presets = tuneBfree_presets
				elif engine == 'Surge XT Wrapper':
					self.banks = range(len(surge_xt_presets))
					self.presets = surge_xt_presets
				elif engine == 'Reface CP Wrapper':
					self.banks = range(len(reface_cp_presets))
					self.presets = reface_cp_presets
				self.reset_banks()
			elif (self.banks is not None) and msg.note in range(44, 44+len(self.banks)):
				bank = msg.note - 44
				self.programs = self.presets[bank]
				self.reset_banks()
				xq.send(to_exquis, xq.sysex(xq.color_key, msg.note, xq.white))
				self.current_bank = bank
				self.reset_programs()
			elif (self.programs is not None) and msg.note in range(33, 33+self.programs):
				program = msg.note - 33
				self.reset_programs()
				xq.send(to_exquis, xq.sysex(xq.color_key, msg.note, xq.white))
				if self.current_device == self.exquis:
					exquis_to_engine.send(mido.Message('control_change', control=0, value=self.current_bank))
					exquis_to_engine.send(mido.Message('program_change', program=program))
				elif self.current_device == self.reface_cp:
					reface_cp_to_engine.send(mido.Message('control_change', control=0, value=self.current_bank))
					reface_cp_to_engine.send(mido.Message('program_change', program=program))
class Script:
	
	def __init__(self):
		#self.last_exquis_note = 127
		#self.last_reface_cp_note = 0
		self.menu = None
		self.menu_latched = False
		self.reface_cp_is_local = True
	def from_exquis(self, msg):
		#if msg.type == 'note_on':
		#	self.last_exquis_note = msg.note
		if xq.is_menu(msg, xq.pressed):
			if not self.menu_latched:
				self.menu_latched = True
				self.menu = None
			exquis_to_engine.send(mido.Message('control_change', control=120))
			reface_cp_to_engine.send(mido.Message('control_change', control=120))
			xq.all_lights_off(to_exquis)
			xq.set_map(to_exquis, xq.equals_keys_map, xq.no_crop)
			for button in xq.menu:
				if xq.is_sysex(msg, [xq.click, button, xq.pressed]):
					break
			if self.menu == button:
				self.menu_latched = not self.menu_latched
			self.menu = button
		if self.menu_latched:
			if self.menu == xq.sounds:
				sounds.menu(msg)
		#elif (msg.type == 'pitchwheel' or msg.is_cc(74)) and self.last_exquis_note <= self.last_reface_cp_note:
		#	pass
		#else:
		#	if exquis_to_engine.name == 'Reface CP Wrapper' and (xq.is_sysex(msg, [xq.clockwise, xq.knob1, any]) or xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, any])):
		#		exquis_to_mtsesp.send(xq.sysex(xq.click, xq.button1, xq.pressed))
		else:
			exquis_to_mtsesp.send(msg)
			
	def from_reface_cp(self, msg):
		if reface_cp_to_engine.name != 'Reface CP Wrapper':
			if self.reface_cp_is_local:
				to_reface_cp.send(cp.local_control(cp.off))
			self.reface_cp_is_local = False
			if msg.type == 'control_change':
				to_reface_cp.send(msg)
			if hasattr(msg, 'channel'):
				msg.channel = 0
			if msg.type in ['note_on', 'note_off']:
				halberstadt_to_mtsesp.send(msg)
				#if msg.type == 'note_on':
				#	self.last_reface_cp_note = msg.note
			else:
				reface_cp_to_engine.send(msg)
				if msg.is_cc(64) and exquis_to_engine.name != reface_cp_to_engine.name:
						exquis_to_engine.send(msg)
		else:
			if not self.reface_cp_is_local:
				to_reface_cp.send(cp.local_control(cp.on))
			self.reface_cp_is_local = True
		
	def exquis_from_mtsesp(self, msg):
		if xq.is_sysex(msg): # also keep sending active sensing in mts
			if xq.is_active_sensing(msg) or not self.menu_latched:
				to_exquis.send(msg)
		else:
			exquis_to_engine.send(msg)
	def halberstadt_from_mtsesp(self,msg):
		if hasattr(msg, 'channel'):
			if msg.channel == 0:
				reface_cp_to_engine.send(msg)
		
		
	
# run script
to_exquis = Outport(client_name, name='Exquis', verbose=False)
to_reface_cp = Outport(client_name, name='Reface CP', verbose=False)
exquis_to_mtsesp = Outport(client_name, name='MTS-ESP (Exquis)', verbose=False)
halberstadt_to_mtsesp = Outport(client_name, name='MTS-ESP (Halberstadt)', verbose=False)
exquis_to_engine = Engine(engines[0])
reface_cp_to_engine = Engine(engines[0])
sounds = Sounds()
script = Script()
from_exquis = Inport(script.from_exquis, client_name, name='Exquis')
from_reface_cp = Inport(script.from_reface_cp, client_name, name='Reface CP')
exquis_from_mtsesp = Inport(script.exquis_from_mtsesp, client_name, name='MTS-ESP (Exquis)', verbose=False)
halberstadt_from_mtsesp = Inport(script.halberstadt_from_mtsesp, client_name, name='MTS-ESP (Halberstadt)', verbose=False)
initialised = [
	from_exquis.open,
	from_reface_cp.open,
	exquis_from_mtsesp.open,
	halberstadt_from_mtsesp.open,
]
make_threads(initialised)

