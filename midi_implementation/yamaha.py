import mido

manufacturer_id = 0x43

class RefaceCP:
	
	## sysex
	device_number = 0x10 # could be any between 0x10 and 0x1F
	group_number_high = 0x7F
	group_number_low = 0x1C
	model_id = 0x04
	
	prefix = [manufacturer_id, device_number, group_number_high, group_number_low]
	
	on = 0x01
	off = 0x00
	
	## cc
	sustain_control = 64
	type_control = 80
	drive_control = 81
	tremolo_wah_control = 17
	tremolo_wah_depth_control = 18
	tremolo_wah_rate_control = 19
	chorus_phaser_control = 85
	chorus_phaser_depth_control = 86
	chorus_phaser_speed_control = 87
	digital_analog_control = 88
	digital_analog_depth_control = 89
	digital_analog_time_control = 90
	reverb_depth_control = 91
	
	up = 64
	middle = 0
	down = 127
	
	client_name = 'reface CP'
	inports = ['reface CP MIDI 1']
	outports = ['reface CP MIDI 1']
	
	## init
	def __init__(self):
		self.sustain_value = 0
		self.type_value = 0
		self.drive_value = 0
		self.tremolo_wah_value = 0
		self.tremolo_wah_depth_value = 0
		self.tremolo_wah_rate_value = 0
		self.chorus_phaser_value = 0
		self.chorus_phaser_depth_value = 0
		self.chorus_phaser_speed_value = 0
		self.digital_analog_value = 0
		self.digital_analog_depth_value = 0
		self.digital_analog_time_value = 0
		self.reverb_depth_value = 0
		
	def is_connected(self):
		out = 0
		for outport in mido.get_output_names():
			out += max([port in self.client_name+':'+outport for port in self.outports])
		for inport in mido.get_input_names():
			out += max([port in self.client_name+':'+inport for port in self.inports])
		return bool(out)
		
	## sysex
	def parameter_change(self, address, data):
		if type(data) is list:
			return mido.Message('sysex', data=[*self.prefix, self.model_id, *address, *data])
		else:
			return mido.Message('sysex', data=[*self.prefix, self.model_id, *address, data])
	
	def local_control(self,state):
		return self.parameter_change(address=[0x00, 0x00, 0x06], data=state)
		
	## cc
	def instrument_type(self, msg):
		if msg.is_cc(self.type_control):
			self.type_value = msg.value
			if self.type_value in range(0,22):
				return 'Rd I'
			elif self.type_value in range(22,43):
				return 'Rd II'
			elif self.type_value in range(43,65):
				return 'Wr'
			elif self.type_value in range(65,86):
				return 'Clv'
			elif self.type_value in range(86,107):
				return 'Toy'
			else:
				return 'CP'
		return None
		
	def drive(self, msg):
		if msg.is_cc(self.drive_control):
			self.drive_value = msg.value
			return self.drive_value
		return None
			
	def tremolo(self, msg):
		if msg.is_cc(self.tremolo_wah_control):
			if msg.value == self.up:
				self.tremolo_wah_value = msg.value
				return True, self.tremolo_wah_depth_value, self.tremolo_wah_rate_value
			elif self.tremolo_wah_value == self.up and msg.value == self.middle:
				self.tremolo_wah_value = msg.value
				return False, None, None
		elif msg.is_cc(self.tremolo_wah_depth_control):
			self.tremolo_wah_depth_value = msg.value
			if self.tremolo_wah_value == self.up:
				return None, self.tremolo_wah_depth_value, None
		elif msg.is_cc(self.tremolo_wah_rate_control):
			self.tremolo_wah_rate_value = msg.value
			if self.tremolo_wah_value == self.up:
				return None, None, self.tremolo_wah_rate_value
		return None, None, None
		
	def wah(self, msg):
		if msg.is_cc(self.tremolo_wah_control):
			if msg.value == self.down:
				self.tremolo_wah_value = msg.value
				return True, self.tremolo_wah_depth_value, self.tremolo_wah_rate_value
			elif self.tremolo_wah_value == self.down and msg.value == self.middle:
				self.tremolo_wah_value = msg.value
				return False, None, None
		elif msg.is_cc(self.tremolo_wah_depth_control):
			self.tremolo_wah_depth_value = msg.value
			if self.tremolo_wah_value == self.down:
				return None, self.tremolo_wah_depth_value, None
		elif msg.is_cc(self.tremolo_wah_rate_control):
			self.tremolo_wah_rate_value = msg.value
			if self.tremolo_wah_value == self.down:
				return None, None, self.tremolo_wah_rate_value
		return None, None, None
		
	def chorus(self, msg):
		if msg.is_cc(self.chorus_phaser_control):
			if msg.value == self.up:
				self.chorus_phaser_value = msg.value
				return True, self.chorus_phaser_depth_value, self.chorus_phaser_speed_value
			elif self.chorus_phaser_value == self.up and msg.value == self.middle:
				self.chorus_phaser_value = msg.value
				return False, None, None
		elif msg.is_cc(self.chorus_phaser_depth_control):
			self.chorus_phaser_depth_value = msg.value
			if self.chorus_phaser_value == self.up:
				return None, self.chorus_phaser_depth_value, None
		elif msg.is_cc(self.chorus_phaser_speed_control):
			self.chorus_phaser_speed_value = msg.value
			if self.chorus_phaser_value == self.up:
				return None, None, self.chorus_phaser_speed_value
		return None, None, None
		
	def phaser(self, msg):
		if msg.is_cc(self.chorus_phaser_control):
			if msg.value == self.down:
				self.chorus_phaser_value = msg.value
				return True, self.chorus_phaser_depth_value, self.chorus_phaser_speed_value
			elif self.chorus_phaser_value == self.down and msg.value == self.middle:
				self.chorus_phaser_value = msg.value
				return False, None, None
		elif msg.is_cc(self.chorus_phaser_depth_control):
			self.chorus_phaser_depth_value = msg.value
			if self.chorus_phaser_value == self.down:
				return None, self.chorus_phaser_depth_value, None
		elif msg.is_cc(self.chorus_phaser_speed_control):
			self.chorus_phaser_speed_value = msg.value
			if self.chorus_phaser_value == self.down:
				return None, None, self.chorus_phaser_speed_value
		return None, None, None
		
	def digital_delay(self, msg):
		if msg.is_cc(self.digital_analog_control):
			if msg.value == self.up:
				self.digital_analog_value = msg.value
				return True, self.digital_analog_depth_value, self.digital_analog_time_value
			elif self.digital_analog_value == self.up and msg.value == self.middle:
				self.digital_analog_value = msg.value
				return False, None, None
		elif msg.is_cc(self.digital_analog_depth_control):
			self.digital_analog_depth_value = msg.value
			if self.digital_analog_value == self.up:
				return None, self.digital_analog_depth_value, None
		elif msg.is_cc(self.digital_analog_time_control):
			self.digital_analog_time_value = msg.value
			if self.digital_analog_value == self.up:
				return None, None, self.digital_analog_time_value
		return None, None, None
		
	def analog_delay(self, msg):
		if msg.is_cc(self.digital_analog_control):
			if msg.value == self.down:
				self.digital_analog_value = msg.value
				return True, self.digital_analog_depth_value, self.digital_analog_time_value
			elif self.digital_analog_value == self.down and msg.value == self.middle:
				self.digital_analog_value = msg.value
				return False, None, None
		elif msg.is_cc(self.digital_analog_depth_control):
			self.digital_analog_depth_value = msg.value
			if self.digital_analog_value == self.down:
				return None, self.digital_analog_depth_value, None
		elif msg.is_cc(self.digital_analog_time_control):
			self.digital_analog_time_value = msg.value
			if self.digital_analog_value == self.down:
				return None, None, self.digital_analog_time_value
		return None, None, None
				
	def reverb(self, msg):
		if msg.is_cc(self.reverb_depth_control):
			self.reverb_depth_value = msg.value
			return self.reverb_depth_value
		return None
		
	def sustain(self, msg):
		if msg.is_cc(self.sustain_control):
			self.sustain_value = msg.value
			return self.sustain_value
		return None

		
reface_cp = RefaceCP()
