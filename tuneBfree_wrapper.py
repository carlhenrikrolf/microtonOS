#! /home/pi/.venv/bin/python3

# parameters
client_name = 'tuneBfree Wrapper'

# import
import mido
import mtsespy as mts
import numpy as np
import time
import threading
import signal
import sys
import subprocess
from utils import Inport, Outport

# definitions

			
def drawbar_presets(msg):
	power_chord = [
			'--upper',
			'088000000',
		]
	bossa = [
			'--upper',
			'800000008',
		]
	jimmy_smith = [
			'--upper',
			'888000008',
		]
	full_organ = [
			'--upper',
			'888888888',
		]
	squabble = [
			'--upper',
			'8000008888',
		]
	percussion = [
			'--upper',
			'000000008',
		]
	green_onions = [
			'--upper',
			'8888000000',
		]
		
	if msg.type == 'control_change' and msg.control == 80:
		if msg.value == 0:
			return power_chord
		elif msg.value == 25:
			return jimmy_smith
		elif msg.value == 51:
			return full_organ
		elif msg.value == 76:
			return squabble
		elif msg.value == 102:
			return percussion
		else:
			return bossa
	else:
		return None
		


class Tremolo2:
	
	depth_in = 18
	toggle_in = 17
	up_position = 64
	middle_position = 0
	down_position = 127
	rate_in = 19
	
	horn_off_drum_off = mido.Message('control_change', control=1, value=8)
	horn_off_drum_slow = mido.Message('control_change', control=1, value=22)
	horn_off_drum_fast = mido.Message('control_change', control=1, value=36)
	horn_slow_drum_off = mido.Message('control_change', control=1, value=50)
	horn_slow_drum_slow = mido.Message('control_change', control=1, value=64)
	horn_slow_drum_fast = mido.Message('control_change', control=1, value=78)
	horn_fast_drum_off = mido.Message('control_change', control=1, value=92)
	horn_fast_drum_slow = mido.Message('control_change', control=1, value=106)
	horn_fast_drum_fast = mido.Message('control_change', control=1, value=120)
	
	def __init__(
			self,
			outport,
			footswitch,
			channel: int,
		):
			
		self.outport = outport
		self.footswitch = footswitch
		self.channel = channel
		
		self.depth = 0
		self.toggle = 0
		self.rate = 0
		
	def send(self,out):
		for o in out:
			o.channel = self.channel
			self.outport.send(o)
			
	def leslie_switch(self):
		out = []
		if self.toggle == self.up_position:
			if self.depth < 44:
				if self.rate < 44:
					out = [self.horn_off_drum_off]
				elif self.rate < 86:
					out = [self.horn_slow_drum_off]
				else:
					out = [self.horn_fast_drum_off]
			elif self.depth < 86:
				if self.rate < 44:
					out = [self.horn_off_drum_slow]
				elif self.rate < 86:
					out = [self.horn_slow_drum_slow]
				else:
					out = [self.horn_fast_drum_slow]
			else:
				if self.rate < 44:
					out = [self.horn_off_drum_fast]
				elif self.rate < 86:
					out = [self.horn_slow_drum_fast]
				else:
					out = [self.horn_fast_drum_fast]
		elif self.toggle == self.down_position:
			if self.depth < 64:
				if self.rate < 64:
					out = [self.horn_off_drum_off]
				else:
					out = [self.horn_slow_drum_off]
			else:
				if self.rate < 64:
					out = [self.horn_off_drum_slow]
				else:
					out = [self.horn_slow_drum_slow]
		else:
			out = [self.horn_off_drum_off]
		return out
		
	def remap(self,msg):
		if not footswitch.is_pressed:
			if msg.control == self.toggle_in:
				if msg.value == self.middle_position:
					self.toggle = self.middle_position
					out = self.leslie_switch()
					self.send(out)
				elif msg.value == self.down_position:
					self.toggle = self.down_position
					out = self.leslie_switch()
					self.send(out)
				else:
					self.toggle = self.up_position
					out = self.leslie_switch()
					self.send(out)
			elif msg.control == self.depth_in:
				self.depth = msg.value
				out = self.leslie_switch()
				self.send(out)
			elif msg.control == self.rate_in:
				self.rate = msg.value
				out = self.leslie_switch()
				self.send(out)
		else:
			pass
			
	def resend(self):
		out = self.leslie_switch()
		self.send(out)


		
class Vibrato:
	
	depth_in = 86
	toggle_in = 85
	up_position = 64
	middle_position = 0
	down_position = 127
	rate_in = 87
	
	vibrato_on = mido.Message('control_change', control=95, value=96)
	vibrato_off = mido.Message('control_change', control=95, value=0)
	v1 = mido.Message('control_change', control=92, value=11) #0
	c1 = mido.Message('control_change', control=92, value=32) #22
	v2 = mido.Message('control_change', control=92, value=53) #44
	c2 = mido.Message('control_change', control=92, value=74) #66
	v3 = mido.Message('control_change', control=92, value=95) #88
	c3 = mido.Message('control_change', control=92, value=116) #110
	drum_acceleration = mido.Message('control_change', control=14)
	drum_deceleration = mido.Message('control_change', control=15)
	horn_acceleration = mido.Message('control_change', control=16)
	horn_deceleration = mido.Message('control_change', control=17)

	
	def __init__(
			self,
			outport,
			footswitch,
			channel: int,
		):
			
		self.outport = outport
		self.footswitch = footswitch
		self.channel = channel
		
		self.depth = 0
		self.toggle = 0
		self.rate = 0
		
	def send(self,out):
		for o in out:
			o.channel = self.channel
			self.outport.send(o)
		
	def vibrato_knob(self):
		out = []
		if self.toggle == self.up_position:
			if self.rate < 64:
				if self.depth < 44:
					out = [self.v1]
				elif self.depth < 86:
					out = [self.v2]
				else:
					out = [self.v3]	
			else:
				if self.depth < 44:
					out = [self.c1]
				elif self.depth < 86:
					out = [self.c2]
				else:
					out = [self.c3]	
		return out
		
	def vibrato_switch(self):
		out = []
		if self.toggle == self.up_position:
			out = [self.vibrato_on]
		else:
			out = [self.vibrato_off]
		return out
		
	def drum_knob(self):
		out = []
		if self.toggle == self.down_position:
			self.drum_acceleration.value = self.depth
			self.drum_deceleration.value = self.depth
			out = [self.drum_acceleration, self.drum_deceleration]
		return out
		
	def horn_knob(self):
		out = []
		if self.toggle == self.down_position:
			self.horn_acceleration.value = self.rate
			self.horn_deceleration.value = self.rate
			out = [self.horn_acceleration, self.horn_deceleration]
		return out
		
	
	def remap(self,msg):
		if not footswitch.is_pressed:
			if msg.control == self.toggle_in:
				if msg.value == self.middle_position:
					self.toggle = self.middle_position
					out = self.vibrato_switch()
					self.send(out)
				elif msg.value == self.down_position:
					self.toggle = self.down_position
					out = [*self.drum_knob(), *self.horn_knob()]
					self.send(out)
				else:
					self.toggle = self.up_position
					out = [*self.vibrato_switch(), *self.vibrato_knob()]
					self.send(out)
			elif msg.control == self.depth_in:
				self.depth = msg.value
				out = [*self.vibrato_knob(), *self.drum_knob()]
				self.send(out)
			elif msg.control == self.rate_in:
				self.rate = msg.value
				out = [*self.vibrato_knob(), *self.horn_knob()]
				self.send(out)
		else:
			pass
			
	def resend(self):
		out = [*self.vibrato_switch() *self.vibrato_knob(), *self.drum_knob(), *self.horn_knob()]
		self.send(out)
		
		
		


		
class Percussion:
	
	def __init__(self,port,toggle_in:int,toggle_out:list,depth_in:int,depth_out:list,rate_in:int,rate_out:list,channel:int):
		self.port = port
		self.toggle_in = toggle_in
		self.toggle_out = toggle_out
		self.depth_in = depth_in
		self.depth_out = depth_out
		self.rate_in = rate_in
		self.rate_out = rate_out
		self.channel = channel
		self.toggle_on = mido.Message('control_change', control=toggle_out[0], value=0, channel=channel)
		self.toggle_kind = mido.Message('control_change', control=toggle_out[0], value=64, channel=channel)
		self.depth_cc = mido.Message('control_change', control=depth_out[1], value=0, channel=channel)
		self.rate_cc = mido.Message('control_change', control=rate_out[1], value=0, channel=channel)
		
	def remap(self,msg):
		if msg.control == self.toggle_in:
			if msg.value == 0:
				self.toggle_on = mido.Message('control_change', control=self.toggle_out[0], value=0, channel=self.channel)
				self.toggle_kind = mido.Message('control_change', control=self.toggle_out[1], value=64, channel=self.channel)
				self.depth_cc.control = self.depth_out[1]
				self.rate_cc.control = self.rate_out[1]
				self.resend()
			elif msg.value == 127:
				self.toggle_on = mido.Message('control_change', control=self.toggle_out[0], value=127, channel=self.channel)
				self.toggle_kind = mido.Message('control_change', control=self.toggle_out[1], value=0, channel=self.channel)
				self.depth_cc.control = self.depth_out[2]
				self.rate_cc.control = self.rate_out[2]
				self.resend()
			else:
				self.toggle_on = mido.Message('control_change', control=self.toggle_out[0], value=127, channel=self.channel)
				self.toggle_kind = mido.Message('control_change', control=self.toggle_out[1], value=127, channel=self.channel)
				self.depth_cc.control = self.depth_out[0]
				self.rate_cc.control = self.rate_out[0]
				self.resend()
		elif msg.control == self.depth_in:
			self.depth_cc.value = 127 - msg.value
			self.port.send(self.depth_cc)
		elif msg.control == self.rate_in:
			self.rate_cc.value = msg.value
			self.port.send(self.rate_cc)
			
	def resend(self):
		self.port.send(self.toggle_on)
		self.port.send(self.toggle_kind)
		time.sleep(0.1)
		self.port.send(self.depth_cc)
		self.port.send(self.rate_cc)








class TuneBFree:
	def __init__(self):
		self.path = '/home/pi/tuneBfree/build/tuneBfree'
		self.cfg = '/home/pi/Scripts/tuneBfree-config/my.cfg'
		self.user = 'pi'
		self.options=['--dumpcc']
	def restart(self):
		self.stop()
		self.process = subprocess.Popen(
			['sudo', '-u', self.user, self.path, '--config', self.cfg, *self.options]
		)
	def stop(self):
		try:
			self.process.terminate()
		except:
			pass
		

class Script:
	
	tuneBfree_path = '/home/pi/tuneBfree/build/tuneBfree'
	cfg_path = '/home/pi/Scripts/tuneBfree-config/my.cfg'
	wait = 0.3
	
	def __init__(self):
		self.commandline = ['sudo', '-u', 'pi', self.tuneBfree_path, '--config', self.cfg_path]
		self.tuneBfree = subprocess.Popen(self.commandline)
		signal.signal(signal.SIGTERM, self.signal_handler)
		self.to_frequency = [0.0]*128
		for note in range(0,128):
			self.to_frequency[note] = mts.note_to_frequency(mts_client, note, 0)
		#self.asleep = False
		#self.last_input = time.perf_counter_ns()
	def signal_handler(self, signum, frame):
		self.tuneBfree.terminate()
		sys.exit(0)
	def process(self, msg):
		#self.last_input = time.perf_counter_ns()
		#if self.asleep:
		#	self.asleep = False
		#	self.tuneBfree = subprocess.Popen(self.commandline)
		#	time.sleep(self.wait)
		if hasattr(msg, 'channel'):
			msg.channel = 0
		if msg.type == 'note_on':
			new_frequency = mts.note_to_frequency(mts_client, msg.note, 0)
			if new_frequency != self.to_frequency[msg.note]:
				for note in range(0,128):
					self.to_frequency[note] = mts.note_to_frequency(mts_client, note, 0)
				self.restart()
		if msg.type in ['aftertouch', 'polytouch']:
			msg = mido.Message('control_change', control=1, value=msg.value)
		#elif msg.is_cc(64):
		#	msg = mido.Message('control_change', control=7, value=int(127-msg.value/2))
		if msg.type == 'reset':
			self.restart()
		else:
			outport.send(msg)
	def restart(self):
		try:
			self.tuneBfree.terminate()
		finally:
			self.tuneBfree = subprocess.Popen(self.commandline)
			time.sleep(self.wait)
	#def goto_sleep(self):
	#	while True:
	#		if time.perf_counter_ns() - self.last_input > 60e9 and not self.asleep:
	#			self.asleep = True
	#			self.tuneBfree.terminate()
	#		time.sleep(60)
		


with mts.Client() as mts_client:
	outport = Outport(client_name)
	script = Script()
	inport = Inport(script.process, client_name)
	inport.open()
	#threads = [
	#	threading.Thread(target=inport.open, daemon=True),
	#	threading.Thread(target=script.goto_sleep, daemon=True),
	#]
	#for thread in threads:
	#	thread.start()
	#for thread in threads:
	#	thread.join()

