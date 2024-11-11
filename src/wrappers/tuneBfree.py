from midi_implementation.gm2 import control_change as cc
from utils import Inport, Outport

client_name = 'tuneBfree Wrapper'

drive_on = mido.Message('control_change', control=65, value=127)
drive_off = mido.Message('control_change', control=65, value=0)

horn_off_drum_off = mido.Message('control_change', control=1, value=8)
horn_off_drum_slow = mido.Message('control_change', control=1, value=22)
horn_off_drum_fast = mido.Message('control_change', control=1, value=36)
horn_slow_drum_off = mido.Message('control_change', control=1, value=50)
horn_slow_drum_slow = mido.Message('control_change', control=1, value=64)
horn_slow_drum_fast = mido.Message('control_change', control=1, value=78)
horn_fast_drum_off = mido.Message('control_change', control=1, value=92)
horn_fast_drum_slow = mido.Message('control_change', control=1, value=106)
horn_fast_drum_fast = mido.Message('control_change', control=1, value=120)

drum_acceleration = mido.Message('control_change', control=14)
drum_deceleration = mido.Message('control_change', control=15)
horn_acceleration = mido.Message('control_change', control=16)
horn_deceleration = mido.Message('control_change', control=17)

vibrato_on = mido.Message('control_change', control=95, value=96)
vibrato_off = mido.Message('control_change', control=95, value=0)
v1 = mido.Message('control_change', control=92, value=11) #0
c1 = mido.Message('control_change', control=92, value=32) #22
v2 = mido.Message('control_change', control=92, value=53) #44
c2 = mido.Message('control_change', control=92, value=74) #66
v3 = mido.Message('control_change', control=92, value=95) #88
c3 = mido.Message('control_change', control=92, value=116) #110

percussion_soft = mido.Message('control_change', control=66, value=63)
percussion_normal = mido.Message('control_change', control=66, value=16)
percussion_off = mido.Message('control_change', control=66, value=0)

class Leslie:
	
	def __init__(self, control=1):
		self.control = control
		self.horn_speed = 0
		self.drum_speed = 0
		
	def translate(self, horn=horn_speed, drum=drum_speed):
		self.horn_speed = horn
		self.drum_speed = drum
		if msg.drum_speed in range(0,42):
			if self.drum_speed in range(0,42):
				print('horn off, drum off')
				return mido.Message('control_change', control=self.control, value=8)
			elif self.drum_speed in range(42, 84):
				print('horn off, drum slow')
				return mido.Message('control_change', control=self.control, value=22)
			else:
				print('horn off, drum fast')
				return mido.Message('control_change', control=self.control, value=36)
		elif mself.drum_speed in range(42, 84):
			if self.drum_speed in range(0,42):
				print('horn slow, drum off')
				return mido.Message('control_change', control=self.control, value=50)
			elif self.drum_speed in range(42, 84):
				print('horn slow, drum slow')
				return mido.Message('control_change', control=self.control, value=64)
			else:
				print('horn slow, drum fast')
				return mido.Message('control_change', control=self.control, value=78)
		else:
			if self.drum_speed in range(0,42):
				print('horn fast, drum off')
				return mido.Message('control_change', control=self.control, value=92)
			elif self.drum_speed in range(42, 84):
				print('horn fast, drum slow')
				return mido.Message('control_change', control=self.control, value=106)
			else:
				print('horn fast, drum fast')
				return mido.Message('control_change', control=self.control, value=120)

class Vibrato:
	
	def __init__(self, control=92):
		self.control = control
		self.depth_value = 0
		self.is_chorus_value = 0
		
	def translate(self, depth=depth_value, is_chorus=is_chorus_value):
		self.depth_value = depth
		self.is_chorus_value = is_chorus
		if self.depth_value in range(0,42):
			if self.is_chorus_value in range(0,64):
				print('v1')
				return mido.Message('control_change', control=self.control, value=11)
			if else:
				print('c1')
				return mido.Message('control_change', control=self.control, value=32)
		elif self.depth_value in range(42,84):
			if self.is_chorus_value in range(0,64):
				print('v2')
				return mido.Message('control_change', control=self.control, value=53)
			else:
				print('c2')
				return mido.Message('control_change', control=self.control, value=74)
		else:
			if self.is_chorus_value in range(0,64):
				print('v3')
				return mido.Message('control_change', control=self.control, value=95)
			else:
				print('c3')
				return mido.Message('control_change', control=self.control, value=116)

class Percussion:
	
	def __init__(self, control=66):
		self.control = control
		self.depth_value = 0
		self.is_on_value = 0
		
	def translate(self, depth=depth_value, is_on=is_on_value):
		self.depth_value = depth
		self.is_on_value = is_on
		if self.is_on in range(0,64):
			print('percussion off')
			return mido.Message('control_change', control=self.control, value=0)
		else:
			if self.depth_value in range(0,64):
				print('soft percussion')
				return mido.Message('control_change', control=self.control, value=63)
			else:
				print('normal_percussion')
				return mido.Message('control_change', control=self.control, value=16)

leslie = Leslie(control=1)
vibrato = Vibrato(control=92)	
percussion = Percussion(control=66)

def drive(msg):
	if msg.is_cc(94): # detune
		if msg.value > 0:
			to_tuneBfree.send(mido.Message('control_change', control=65, value=127))
		else:
			to_tuneBfree.send(mido.Message('control_change', control=65, value=0))
		print('drive', msg.value)
	
def horn(self, msg):
	if msg.is_cc(cc.tremolo):
		if msg.value in range(0,64):
			to_tuneBfree.send(leslie.translate(horn=0))
	elif msg.is_cc(cc.undefined[0]):
		to_tuneBfree.send(mido.Message('control_change', control=2, value=msg.value))
		print('horn acceleration', msg.value)
	elif msg.is_cc(cc.undefined[1]):
		to_tuneBfree.send(leslie.translate(horn=msg.value))
			
def filter(msg):
	pass
	
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
		to_tuneBree.send(vibrato.translate(is_chorus=msg.value))
	
def drum:
	if msg.is_cc(cc.phaser):
		if msg.value in range(0,64):
			print('drum off')
			to_tuneBfree.send(leslie.translate(drum=0)
	elif msg.is_cc(cc.undefined[6]):
		print('drum acceleration', msg.value)
		to_tuneBfree.send(mido.Message('control_change', control=21, value=msg.value))
	elif msg.is_cc(cc.undefined[7]):
		to_tuneBfree(leslie.translate(drum=msg.value))
	
def harmonic2:
	if msg.is_cc(cc.effect_controller[0][0]):
		...
	elif msg.is_cc(cc.undefined[8]):
		...
	elif msg.is_cc(cc.undefined[9]):
		...
	
def harmonic3:
	if msg.is_cc(cc.effect_controller[1][0]):
		...
	elif msg.is_cc(cc.undefined[8]):
		...
	elif msg.is_cc(cc.undefined[9]):









class TuneBFree:
	def __init__(self):
		self.path = '/home/pi/tuneBfree/build/tuneBfree'
		self.cfg = '/home/pi/microtonOS/tuneBfree-config/my.cfg'
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
	cfg_path = '/home/pi/microtonOS/tuneBfree-config/my.cfg'
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

