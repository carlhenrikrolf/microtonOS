from midi_implementation.gm2 import control_change as cc

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

def pgm_change:

def drive:

def tremolo_chorale:
	
def vibrato_chorus:
	
def percussion:
	









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

