import mido
import mtsespy as esp
import time


class ControlChange:
    effect_controller = [None] * 2
    general_purpose_controller = [None] * 8
    sound_controller = [None] * 10
    effect_depth = [None] * 5

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

    undefined_msb = [3, 9, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31]
    undefined_lsb = [35, 41, 46, 47, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63]
    undefined_14bit = [list(i) for i in zip(undefined_msb, undefined_lsb)]
    undefined_7bit = [
        85,
        86,
        87,
        89,
        90,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
    ]
    undefined = [*undefined_msb, *undefined_7bit]

    assignable = [
        *[i for i in range(1, 32)],
        *[i for i in range(64, 88)],
        *[i for i in range(89, 96)],
    ]

    channel_mode_message = [None] * 8

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


class MtsEsp:
    def __init__(
        self, outport, client, pitchbend_range=2, tx_channel=None, query_rate=0
    ):
        self.outport = outport
        self.client = client
        self.pitchbend_range = pitchbend_range
        self.tx_channel = tx_channel
        self.query_rate = query_rate

        self.resolution = 2 * self.pitchbend_range / 2**14
        self.queue = []
        self.tuning = [[0 for _ in range(16)] for _ in range(128)]
        self.is_on = [[False for _ in range(16)] for _ in range(128)]

    def query(self, msg=None):
        run = True if msg is None else False
        if not run and msg.type == "note_on":
            tuning = esp.retuning_in_semitones(self.client, msg.note, msg.channel)
            run = abs(tuning - self.tuning[msg.note][msg.channel]) > self.resolution / 2
        if run:
            for channel in range(16):
                for note in range(128):
                    retuning = esp.retuning_in_semitones(self.client, note, channel)
                    self.tuning[note][channel] = retuning
        return run

    def standard_tuning(self):
        for note in range(127):
            step = esp.retuning_in_semitones(self.client, note + 1, -1)
            step -= esp.retuning_in_semitones(self.client, note, -1)
            is_semitone = abs(step - 1.0) < self.resolution / 2
            if not is_semitone:
                return False
        _, pitch, _ = self.note_pitch([69,0])
        tx_channel = 0 if self.tx_channel is None else self.tx_channel
        pitchwheel = mido.Message("pitchwheel", pitch=pitch, channel=tx_channel)
        self.outport.send(pitchwheel)
        return True

    def note_pitch(self, note_channel):
        rx_note, rx_channel = note_channel
        note = round(self.tuning[rx_note][rx_channel])
        note += rx_note
        note = max([0, min([127, note])])
        pitch = self.tuning[rx_note][rx_channel] - note
        pitch /= self.resolution
        in_range = (-(2**14)/2 <= pitch < 2**14/2)
        pitch = max([-(2**14) / 2, min([2**14 / 2 - 1, pitch])])
        pitch = int(pitch)
        return note, pitch, in_range

    def enqueue(self, msg, tx_channel):
        note, _, in_range = self.note_pitch([msg.note, msg.channel])
        if in_range:
            if len(self.queue) >= 1:
                note_off = mido.Message(
                    "note_off", note=note, velocity=msg.velocity, channel=tx_channel
                )
                self.outport.send(note_off)
            self.queue.append([msg.note, msg.channel])

    def dequeue(self, msg, tx_channel):
        if len(self.queue) > 0:
            if [msg.note, msg.channel] == self.queue[-1]:
                self.queue.pop()
                self.bend_note(self.queue[-1], tx_channel, msg.velocity)
            elif [msg.note, msg.channel] in self.queue:
                self.queue.remove([msg.note, msg.channel])

    def bend_note(self, note_channel, tx_channel, velocity):
        note, pitch, in_range = self.note_pitch(note_channel)
        if in_range:
            pitchwheel = mido.Message("pitchwheel", pitch=pitch, channel=tx_channel)
            self.outport.send(pitchwheel)
            note_on = mido.Message(
                "note_on",
                note=note,
                velocity=velocity,
                channel=tx_channel,
            )
            self.outport.send(note_on)

    def dispatch(self, msg):
        if hasattr(msg, "channel"):
            tx_channel = msg.channel if self.tx_channel is None else self.tx_channel
            if msg.type in ["note_on", "note_off"]:
                if msg.type == "note_on" and msg.velocity > 0:
                    self.is_on[msg.note][msg.channel] = True
                    self.enqueue(msg, tx_channel)
                    queried = self.query(msg)
                    if queried:
                        self.queue = []
                    self.bend_note([msg.note, msg.channel], tx_channel, msg.velocity)
                else:
                    self.is_on[msg.note][msg.channel] = False
                    note, _, _ = self.note_pitch([msg.note, msg.channel])
                    note_off = msg.copy(note=note, channel=tx_channel)
                    self.outport.send(note_off)
                    self.dequeue(msg, tx_channel)
            else:
                misc = msg.copy(channel=tx_channel)
                self.outport(misc)
        else:
            self.outport.send(msg)

    def open(self):
        while True:
            is_on = any(self.is_on)
            if is_on:
                if self.query():
                    raise Warning("Not yet implemented")
                time.sleep(1 / self.query_rate)
