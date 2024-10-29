

import mido




class RefaceCP:
	
	## sysex
	yamaha_id = 0x43
	device_number = 0x10 # could be any between 0x10 and 0x1F
	group_number_high = 0x7F
	group_number_low = 0x1C
	model_id = 0x04
	
	prefix = [yamaha_id, device_number, group_number_high, group_number_low]
	
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
	def __init__(self, ignore=False):
		self.ignore	= ignore
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
		self.digital_analog:_time_value = 0
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
	def sustain(self, port=None, msg=None, new=sustain_control):
		if not self.ignore:
			is_sustain = False
			if msg is not None:
				is_sustain = msg.is_cc(self.sustain_control)
				if is_sustain:
					self.sustain_value = msg.value
			if port is not None:
				port.send(msg.Message('control_change', control=control, value=self.sustain_value, channel=msg.channel))
			return is_sustain
				

		
reface_cp = RefaceCP()

ignore_cp = RefaceCP(ignore=True)
