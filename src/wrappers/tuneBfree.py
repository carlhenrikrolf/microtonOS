import subprocess
import mido
import mtsespy as mts
from time import sleep
from midi_implementation.gm2 import control_change as cc
from utils import Inport, Outport, handle_terminations

client_name = 'tuneBfree Wrapper'
pause = 0.001
startup = 0.3
commandline = [
	'sudo',
	'--user',
	'pi',
	'/home/pi/microtonOS/third_party/tuneBfree/build/tuneBfree',
	'--config',
	'home/pi/microtonOS/config/tuneBfree.cfg',
]

class Leslie:
	
	def __init__(self, control=1):
		self.control = control
		self.horn_val = 0
		self.drum_val = 0
		
	def translate(self, horn_value=None, drum_value=None):
		if horn is not None:
			self.horn_val = horn_value
		if drum is not None:
			self.drum_val = drum_value
		if self.horn_val in range(0,42):
			if self.drum_val in range(0,42):
				print('horn off, drum off')
				return mido.Message('control_change', control=self.control, value=8)
			elif self.drum_val in range(42, 84):
				print('horn off, drum slow')
				return mido.Message('control_change', control=self.control, value=22)
			else:
				print('horn off, drum fast')
				return mido.Message('control_change', control=self.control, value=36)
		elif self.horn_val in range(42, 84):
			if self.drum_val in range(0,42):
				print('horn slow, drum off')
				return mido.Message('control_change', control=self.control, value=50)
			elif self.drum_val in range(42, 84):
				print('horn slow, drum slow')
				return mido.Message('control_change', control=self.control, value=64)
			else:
				print('horn slow, drum fast')
				return mido.Message('control_change', control=self.control, value=78)
		else:
			if self.drum_val in range(0,42):
				print('horn fast, drum off')
				return mido.Message('control_change', control=self.control, value=92)
			elif self.drum_val in range(42, 84):
				print('horn fast, drum slow')
				return mido.Message('control_change', control=self.control, value=106)
			else:
				print('horn fast, drum fast')
				return mido.Message('control_change', control=self.control, value=120)

class Vibrato:
	
	def __init__(self, control=92):
		self.control = control
		self.depth_val = 0
		self.is_chorus_val = 0
		
	def translate(self, depth=None, is_chorus=None):
		if depth is not None:
			self.depth_val = depth
		if is_chorus is not None:
			self.is_chorus_val = is_chorus
		if self.depth_val in range(0,42):
			if self.is_chorus_val in range(0,64):
				print('v1')
				return mido.Message('control_change', control=self.control, value=11)
			else:
				print('c1')
				return mido.Message('control_change', control=self.control, value=32)
		elif self.depth_val in range(42,84):
			if self.is_chorus_val in range(0,64):
				print('v2')
				return mido.Message('control_change', control=self.control, value=53)
			else:
				print('c2')
				return mido.Message('control_change', control=self.control, value=74)
		else:
			if self.is_chorus_val in range(0,64):
				print('v3')
				return mido.Message('control_change', control=self.control, value=95)
			else:
				print('c3')
				return mido.Message('control_change', control=self.control, value=116)

class Percussion:
	
	def __init__(self, control=66):
		self.control = control
		self.depth_val = 0
		self.is_on_val = 0
		
	def translate(self, depth=None, is_on=None):
		if depth is not None:
			self.depth_val = depth
		if is_on is not None:
			self.is_on_val = is_on
		if self.is_on_val in range(0,64):
			print('percussion off')
			return mido.Message('control_change', control=self.control, value=0)
		else:
			if self.depth_val in range(0,64):
				print('soft percussion')
				return mido.Message('control_change', control=self.control, value=63)
			else:
				print('normal_percussion')
				return mido.Message('control_change', control=self.control, value=16)

leslie = Leslie(control=1)
vibrato = Vibrato(control=92)	
percussion = Percussion(control=66)

def drive(msg):
	if msg.is_cc(cc.detune):
		if msg.value > 0:
			to_tuneBfree.send(mido.Message('control_change', control=65, value=127))
		else:
			to_tuneBfree.send(mido.Message('control_change', control=65, value=0))
		sleep(pause)
		to_tuneBfree.send(mido.Message('control_change', control=94, value=msg.value))
		print('drive', msg.value)
	
def horn(msg):
	if msg.is_cc(cc.tremolo):
		if msg.value in range(0,64):
			to_tuneBfree.send(leslie.translate(horn_value=0))
	elif msg.is_cc(cc.undefined[0]):
		to_tuneBfree.send(mido.Message('control_change', control=2, value=msg.value))
		print('horn acceleration', msg.value)
	elif msg.is_cc(cc.undefined[1]):
		to_tuneBfree.send(leslie.translate(horn_value=msg.value))
			
def wah(msg):
	if msg.is_cc(cc.undefined[2]):
		to_tuneBfree.send(mido.Message('control_change', control=14, value=msg.value))
	elif msg.is_cc(cc.undefined[3]):
		to_tuneBfree.send(mido.Message('control_change', control=15, value=msg.value))
	
def chorus(msg):
	if msg.is_cc(cc.chorus):
		if msg.value in range(0,64):
			print('chorus off')
			to_tuneBfree.send(mido.Message('control_change', control=95, value=0))
		else:
			print('chorus on')
			to_tuneBfree.send(mido.Message('control_change', control=95, value=96))
	elif msg.is_cc(cc.undefined[4]):
		to_tuneBfree.send(vibrato.translate(depth=msg.value))
	elif msg.is_cc(cc.undefined[5]):
		to_tuneBfree.send(vibrato.translate(is_chorus=msg.value))
	
def drum(msg):
	if msg.is_cc(cc.phaser):
		if msg.value in range(0,64):
			print('drum off')
			to_tuneBfree.send(leslie.translate(drum_value=0))
	elif msg.is_cc(cc.undefined[6]):
		print('drum acceleration', msg.value)
		to_tuneBfree.send(mido.Message('control_change', control=21, value=msg.value))
	elif msg.is_cc(cc.undefined[7]):
		to_tuneBfree.send(leslie.translate(drum_value=msg.value))
	
def harmonic2(msg):
	if msg.is_cc(cc.effect_controller[0][0]):
		to_tuneBfree.send(percussion.translate(is_on=msg.value))
		sleep(pause)
		to_tuneBfree.send(mido.Message('control_change', control=83, value=127))
	elif msg.is_cc(cc.undefined[8]):
		to_tuneBfree.send(percussion.translate(depth=msg.value))
	elif msg.is_cc(cc.undefined[9]):
		to_tuneBfree.send(mido.Message('control_change', control=82, value=msg.value))
	
def harmonic3(msg):
	if msg.is_cc(cc.effect_controller[1][0]):
		to_tuneBfree.send(percussion.translate(is_on=msg.value))
		sleep(pause)
		to_tuneBfree.send(mido.Message('control_change', control=83, value=0))
	elif msg.is_cc(cc.undefined[8]):
		to_tuneBfree.send(percussion.translate(depth=msg.value))
	elif msg.is_cc(cc.undefined[9]):
		to_tuneBfree.send(mido.Message('control_change', control=82, value=msg.value))

def reverb(msg):
	if msg.is_cc(cc.reverb):
		to_tuneBfree.send(mido.Message('control_change', control=91, value=msg.value))

def expression(msg):
	if msg.is_cc(cc.expression_controller[0]):
		to_tuneBfree.send(mido.Message('control_change', control=11, value=msg.value))
	elif msg.is_cc(cc.soft_pedal):
		value = 127 - round(msg.value/2)
		to_tuneBfree.send(mido.Message('control_change', control=11, value=value))
		
		
		
		
		
class Script:
	
	def __init__(self):
		self.process = subprocess.Popen(commandline)
		handle_terminations(self.process)
		self.to_frequency = [0.0]*128
		for note in range(0,128):
			self.to_frequency[note] = mts.note_to_frequency(mts_client, note, 0)
	
	def run(self, msg):
		if msg.is_cc(cc.bank_select[0]):
			pass
		elif msg.type == 'control_change':
			drive(msg)
			horn(msg)
			wah(msg)
			chorus(msg)
			drum(msg)
			harmonic2(msg)
			harmonic3(msg)
			reverb(msg)
			expression(msg)
		elif hasattr(msg, 'channel'):
			if msg.type == 'note_on':
				new_frequency = mts.note_to_frequency(mts_client, msg.note, 0)
				if new_frequency != self.to_frequency[msg.note]:
					for note in range(0,128):
						self.to_frequency[note] = mts.note_to_frequency(mts_client, note, 0)
					self.restart()
			to_tuneBfree.send(msg.copy(channel=0))
		else:
			to_tuneBfree.send(msg)
			
	def restart(self):
		try:
			self.process.terminate()
		finally:
			self.process = subprocess.Popen(commandline)
			sleep(startup)

with mts.Client() as mts_client:
	to_tuneBfree = Outport(client_name, verbose=True)
	script = Script()
	from_microtonOS = Inport(script.run, client_name, verbose=True)
	from_microtonOS.open()

