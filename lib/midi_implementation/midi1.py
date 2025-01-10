class ControlChange:
	
	effect_controller = [None]*2
	general_purpose_controller = [None]*8
	sound_controller = [None]*10
	effect_depth = [None]*5
	
	bank_select = [0, 32]
	modulation_wheel = [1, 33]
	breath_controller = [2, 34]
	foot_controller = [4, 36]
	portamento_time = [5, 37]
	data_entry = [6, 38]
	volume = [7, 39]
	balance = [8, 40]
	pan = [10, 42]
	expression_controller = [11, 43]
	effect_controller[0] = [12, 44]
	effect_controller[1] = [13, 45]
	general_purpose_controller[0] = [16, 48]
	general_purpose_controller[1] = [17, 49]
	general_purpose_controller[2] = [18, 50]
	general_purpose_controller[3] = [19, 51]
	damper_pedal = 64
	portamento = 65
	sostenuto = 66
	soft_pedal = 67
	legato_footswitch = 68
	hold2 = 69
	sound_controller[0] = sound_variation = 70
	sound_controller[1] = timbre = 71
	sound_controller[2] = release_time = 72
	sound_controller[3] = attack_time = 73
	sound_controller[4] = brightness = 74
	sound_controller[5] = decay_time = 75
	sound_controller[6] = vibrato_rate = 76
	sound_controller[7] = vibrato_depth = 77
	sound_controller[8] = vibrato_delay = 78
	sound_controller[9] = 79
	general_purpose_controller[4] = 80
	general_purpose_controller[5] = 81
	general_purpose_controller[6] = 82
	general_purpose_controller[7] = 83
	portamento_control = 84
	high_resolution_velocity_prefix = 88
	effect_depth[0] = reverb = 91
	effect_depth[1] = tremolo = 92
	effect_depth[2] = chorus = 93
	effect_depth[3] = detune = celeste = 94
	effect_depth[4] = phaser = 95
	data_increment = 96
	data_decrement = 97
	nrpn = [99, 98]
	rpn = [101, 100]
	
	undefined_msb = [ 3,  9, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31]
	undefined_lsb = [35, 41, 46, 47, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63]
	undefined_14bit = [list(i) for i in zip(undefined_msb, undefined_lsb)]
	undefined_7bit = [85, 86, 87, 89, 90, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119]
	undefined = [*undefined_msb, *undefined_7bit]
	
	assignable = [
		*[i for i in range(1, 32)],
		*[i for i in range(64, 88)],
		*[i for i in range(89, 96)],
	]
	
	channel_mode_message = [None]*8
	
	channel_mode_message[0] = all_sound_off = 120
	channel_mode_message[1] = reset_all_controllers = 121
	channel_mode_message[2] = local_onoff_switch = 122
	channel_mode_message[3] = all_notes_off = 123
	channel_mode_message[4] = omni_mode_off = 124
	channel_mode_message[5] = omni_mode_on = 125
	channel_mode_message[6] = mono_mode = 126
	channel_mode_message[7] = poly_mode = 127

control_change = ControlChange()

class SystemExclusive:
	
	non_commercial = 0x7D
	device_inquiry = [0x7E, 0x7F, 0x06, 0x01]

system_exclusive = SystemExclusive()

	
