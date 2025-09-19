import mido

manufacturer_id = 0x42


class MinilogueXD:
    version = [None] * 4
    device_id = [0x51, 0x01, 0x00, 0x00, *version]

    # nrpn
    program_name_nrpm = [i for i in range(1, 13)]  # ascii

    voice_mode_type_nrpn = 0x10  # 0~4
    multi_select_noise_nrpn = 0x11  # 0~3
    multi_select_vpm_nrpn = 0x12  # 0~15
    multi_select_user_nrpn = 0x13  # 0~15
    # for 0~1023, lower 3 bits are first sent cia cc63, followed by the remaining 7 in cc6 (data entry msb)
    multi_shape_noise_nrpn = 0x14  # 0~1023
    multi_shape_vpm_nrpn = 0x15  # 0~1023
    multi_shape_user_nrpn = 0x16  # 0~1023
    multi_shift_shape_noise_nrpn = 0x17  # 0~1023
    multi_shift_shape_vpm_nrpn = 0x18  # 0~1023
    multi_shift_shape_user_nrpn = 0x19  # 0~1023

    bend_range_plus_nrpn = 0x20  # 0~12 = Off,1Note~12Note
    bend_range_minus_nrpn = 0x21  # 0~12 = Off,1Note~12Note
    # for -100%~+100%, lower 3 bits are first sent via cc63, followed by the remaining 5 in cc6 (data entry msb)
    joystick_assign_plus_nrpn = 0x22  # 0~28
    joystick_range_plus_nrpn = 0x23  # 0~200 = -100%~+100%
    joystick_assign_minus_nrpn = 0x24  # 0~28
    joystick_range_minus_nrpn = 0x25  # 0~200 = -100%~+100%
    CVin_mode_nrpn = 0x28  # 0~2
    CVin1_assign_nrpn = 0x29  # 0~28
    CVin1_range_nrpn = 0x2A  # 0~200 = -100%~+100%
    CVin2_assign_nrpn = 0x2B  # 0~28
    CVin2_range_nrpn = 0x2C  # 0~200 = -100%~+100%

    micro_tuning_nrpn = (
        0x30  # 0~127, 0~22 factory, 112~117 user scale, 118~123 user octave
    )
    scale_key_nrpn = 0x31  # 0~24 = -12Note~+12Note
    program_tuning_nrpn = 0x32  # 0~100 = -50Cent~+50Cent
    lfo_key_sync_nrpn = 0x34  # 0,1 = Off,On
    lfo_voice_sync_nrpn = 0x35  # 0,1 = Off,On
    lfo_target_osc_nrpn = 0x36  # 0~3
    eg_velocity_nrpn = 0x38  # 0~127
    amp_velocity_nrpn = 0x39  # 0~127
    multi_octave_nrpn = 0x3A  # 0-3 = 16',8',4',2'
    multi_routing_nrpn = 0x3B  # 0,1 = Pre VCF, Post VCF
    eg_legato_nrpn = 0x3C  # 0,1 = Off, On
    portamento_mode_nrpn = 0x3D  # 0,1 = Auto, On
    portamento_bpm_sync_nrpn = 0x3E  # 0,1 = Off, On
    program_level_nrpn = 0x3F  # 0~120 = -18dB~+6dB

    # for -100%~+100%, lower 3 bits are first sent via cc63, followed by the remaining 5 in cc6 (data entry msb)
    vpm_feedback_nrpn = 0x40  # 0~200 = -100%~+100%
    vpm_noise_depth_nrpn = 0x41  # 0~200 = -100%~+100%
    vpm_shape_mod_int_nrpn = 0x42  # 0~200 = -100%~+100%
    vpm_mod_attack_nrpn = 0x43  # 0~200 = -100%~+100%
    vpm_mod_decay_nrpn = 0x44  # 0~200 = -100%~+100%
    vpm_mod_key_track = 0x45  # 0~200 = -100%~+100%
    user_param_1_nrpn = 0x48
    user_param_2_nrpn = 0x49
    user_param_3_nrpn = 0x4A
    user_param_4_nrpn = 0x4B
    user_param_5_nrpn = 0x4C
    user_param_6_nrpn = 0x4C

    program_transpose_nrpn = 0x50  # 1~25 = -12Note~+12Note
    master_volume_nrpn = 0x7F  # 0~16383

    # cc
    continuous = [-1] * 36
    bank_select_control = [0, 32]
    continuous[0] = Yplus_control = 1
    continuous[1] = Yminus_control = 2
    continuous[2] = portamento_time_control = 5
    data_entry_control = 6
    continuous[3] = amp_eg_attack_control = 16
    continuous[4] = amp_eg_decay_control = 17
    continuous[5] = amp_eg_sustain_control = 18
    continuous[6] = amp_eg_release_control = 29
    continuous[7] = eg_attack_control = 20
    continuous[8] = eg_decay_control = 21
    continuous[9] = eg_int_control = 22
    eg_target_control = 23  # 0, 64, or 127
    continuous[10] = lfo_rate_control = 24
    continuous[11] = lfo_int__control = 26
    continuous[12] = voice_mode_depth_control = 27
    continuous[13] = mod_fx_time_control = 28
    continuous[14] = mod_fx_depth_control = 29
    continuous[15] = multi_level_control = 33
    continuous[16] = vco1_pitch_control = 34
    continuous[17] = vco2_pitch_control = 35
    continuous[18] = vco1_shape_control = 36
    continuous[19] = vco2_shape_control = 37
    continuous[20] = vco1_level_control = 39
    continuous[21] = vco2_level_control = 40
    continuous[22] = cross_mod_depth_control = 41
    continuous[23] = cutoff_control = 43
    continuous[24] = resonance_control = 44
    vco1_octave_control = 48  # 0,42,84,127
    vco2_octave_control = 49
    vco1_wave_control = 50  # 0,64,127
    vco2_wave_control = 51
    multi_type_control = 53  # 0,64,127
    continuous[25] = multi_shape_control = 54
    lfo_target_control = 56  # 0,64,127
    lfo_wave_control = 57
    lfo_mode_control = 58
    continuous[26] = voice_mode_depth_control = 59
    lsb_control = 63
    hold_control = 64  # 0 or 127
    sync_control = 80  # 0 or 127
    ring_control = 81  # 0 or 127
    cutoff_keytrack_control = 83  # 0,64,127
    cutoff_drive_control = 84
    mod_fx_type_control = 88  # 0,38,64,84,127
    delay_sub_type_control = (
        89  # 0,7,13,20,26,32, 39,45,52,58,64,71,77,84,90,96,103,109,116,127
    )
    reverb_sub_type_control = (
        90  # 0,8,15,22,29,36,43,50,57,64,72,79,86,93,100,107,117,127
    )
    mod_fx_onoff_control = 92
    delay_onoff_control = 93
    reverb_onoff_control = 94
    mod_fx_subtype_control = 96
    # CHORUS(vv=0,16,32,48,64,80,96,127)
    # ENSEMBLE(vv=0,64,127)
    # PHASER(vv=0,16,32,48,64,80,96,127)
    # FLANGER(vv=0,16,32,48,64,80,96,127)
    # USER(vv=0,8,16,24,32,40,48,56,64,72,8088,96,104,112,128)
    nrpn_control = [99, 98]
    multi_subtype_select_control = 103
    # NOISE(vv=0,42,84,127)
    # VPM(vv=0,8,16,24,32,40,48,56,64,72,80,88,96,104,112,127)
    # USER(vv=0,8,16,24,32,40,48,56,64,72,80,88,96,104,112,127)
    continuous[27] = multi_shift_shape_control = 104
    continuous[28] = delay_time_control = 105
    continuous[29] = delay_depth_control = 106
    continuous[30] = delay_dry_wet_control = 107
    continuous[31] = reverb_time_control = 108
    continuous[32] = reverb_depth_control = 109
    continuous[33] = reverb_dry_wet_control = 110
    continuous[34] = CVin1_control = 118
    continuous[35] = CVin2_control = 119

    def __init__(self):
        self.CVin1_value = 64
        self.CVin2_value = 64

    def is_continuous(self, msg):
        if msg.type == "control_change":
            if msg.control in self.continuous:
                return True
        return False

    def CVin1(self, msg=None, bimodal=True, value=64, channel=0):
        """Bimodal means that 64 is the middle value."""
        if msg is None:
            self.CVin1_value = value
            if not bimodal:
                value = value // 2 + 64
            return mido.Message(
                "control_change",
                control=self.CVin1_control,
                value=value,
                channel=channel,
            )
        else:
            if msg.is_cc(self.CVin1_control):
                self.CVin1_value = msg.value
                if bimodal:
                    return self.CVin1_value
                else:
                    return 2 * self.CVin1_value - 127
            return None

    def CVin2(self, msg=None, bimodal=True, value=64, channel=0):
        """Bimodal means that 64 is the middle value."""
        if msg is None:
            self.CVin2_value = value
            if not bimodal:
                value = value // 2 + 64
            return mido.Message(
                "control_change",
                control=self.CVin2_control,
                value=value,
                channel=channel,
            )
        else:
            if msg.is_cc(self.CVin2_control):
                self.CVin2_value = msg.value
                if bimodal:
                    return self.CVin2_value
                else:
                    return 2 * self.CVin2_value - 127
            return None

    # USER SCALE DATA DUMP REQUEST
    # xd receives it
    # specify scale number
    # USER OCTAVE DATA DUMP REQUEST
    # simile
    # USER SCALE DATA DUMP
    # xd can receive or send it
    # xd sends it when choosing "All Dump"
    # specify scale number and all pitches
    # USER SCALE DATA DUMP (CURRENT)
    # xd receives it
    # specify scale number and all pitches
    # xd sends it when receiving REQUEST?
    # USER OCTAVE DATA DUMP
    # xd can receive or send it
    # xd sends it when choosing "All Dump"
    # specify scale number and pitches for an octave
    # USER SCALE DATA DUMP (CURRENT)
    # not sure what the difference is
    # this one is hex45 while the other was hex44
    # this is in response to OCTAVE DATA DUMPR REQUEST,
    # so maybe typo

    def header(self, channel):
        assert channel in range(16)
        data = [0x42]
        data.append(0x30 + channel)
        data.append(0x00)
        data.append(0x01)
        data.append(0x44)
        return data

    def user_scale_data_dump_request(self, channel, scale_number):
        assert scale_number in range(8)
        data = self.header(channel)
        data.append(0x14)
        data.append(scale_number)
        sysex = mido.Message("sysex", data=data)
        return sysex

    def user_scale_data_dump_current(self, channel, notes, cents, scale_number=None):
        data = self.header(channel)
        data.append(0x44)
        if scale_number is None:
            current = 0x7F
            data.append(current)
        else:
            assert scale_number in range(8)
            data.append(scale_number)
        resolution = resolution = 100 / 2**14
        yy = [0] * 128
        zz = [0] * 128
        for i, c in enumerate(cents):
            tmp = round(c / resolution)
            yy[i] = tmp // 128
            zz[i] = tmp % 128
        for i in range(128):
            data.append(notes[i])
            data.append(yy[i])
            data.append(zz[i])
        sysex = mido.Message("sysex", data=data)
        return sysex


minilogue_xd = MinilogueXD()
