import mido
import mtsespy as esp
import time

# sysex bytes
no_change = [0x7F, 0x7F, 0x7F]
universal_non_realtime = 0x7E
universal_realtime = 0x7F
all_devices = 0x7F
midi_tuning = 0x08
note_change = 0x02
note_change_bank = 0x07

# utils
resolution = 100 / 2**14
max_cents = 100 - resolution / 2


# sysex messages
def keybased(
    keys,
    notes,
    cents,
    tuning_program,
    tuning_bank=None,
    realtime=True,
    device_number=all_devices,
):
    if not hasattr(keys, "__len__"):
        keys = [keys]
        notes = [notes]
        cents = [cents]
    assert 0 < len(keys) == len(notes) == len(cents) <= 127
    assert all([i in range(128) for i in keys])
    assert all([i in range(128) for i in notes])
    assert all([0 <= c < max_cents for c in cents])
    assert tuning_program in range(128)
    ll = len(keys)
    yy = [0] * ll
    zz = [0] * ll
    for i, c in enumerate(cents):
        tmp = round(c / resolution)
        # tmp = min(2**14 - 1, tmp)
        # tmp = max(0, tmp)
        yy[i] = tmp // 128
        zz[i] = tmp % 128
    if tuning_bank is None:
        data = [
            universal_realtime,
            device_number,
            midi_tuning,
            note_change,
            tuning_program,
            ll,
        ]
        if not realtime:
            raise Warning("Please assign tuning_bank for non-real time")
    elif realtime:
        data = [
            universal_realtime,
            device_number,
            midi_tuning,
            note_change_bank,
            tuning_bank,
            tuning_program,
            ll,
        ]
    else:
        data = [
            universal_non_realtime,
            device_number,
            midi_tuning,
            note_change_bank,
            tuning_bank,
            tuning_program,
            ll,
        ]
    for i in range(ll):
        data.append(keys[i])
        data.append(notes[i])
        data.append(yy[i])
        data.append(zz[i])
    return mido.Message("sysex", data=data)


def keybased_dump(name, tuning_program, tuning_bank=None):
    pass


def octave(n_bytes, channels, realtime=True):
    assert n_bytes in [1, 2]


def octave_dump(name, n_bytes, tuning_program, tuning_bank, device_number=all_devices):
    assert n_bytes in [1, 2]


def dump_request(tuning_program, tuning_bank=None, device_number=all_devices):
    pass


# clients
class MtsEsp:

    def __init__(
        self,
        outport,
        client,
        in_channel=0,
        out_channel=0,  # todo
        tuning_program=0,
        tuning_bank=None,
        realtime=True,
        device_number=all_devices,
        query_rate=None,
    ):
        self.outport = outport
        self.client = client
        self.in_channel = in_channel
        self.tuning_program = tuning_program
        self.tuning_bank = tuning_bank
        self.realtime = realtime
        self.device_number = device_number
        self.query_rate = query_rate
        self.tuning = [[0 for _ in range(16)] for _ in range(128)]
        self.is_on = [[False for _ in range(16)] for _ in range(128)]

    def query(self, msg):
        run = True if msg is None else False
        if not run and msg.type == "note_on":
            tuning = esp.retuning_in_semitones(self.client, msg.note, msg.channel)
            run = abs(tuning - self.tuning[msg.note][msg.channel]) > resolution / (
                2 * 100
            )
        if run:
            for channel in range(16):
                for note in range(128):
                    retuning = esp.retuning_in_semitones(self.client, note, channel)
                    self.tuning[note][channel] = retuning
        return run

    def sysex(self):
        semitones = [i for i in range(128)]
        cents = [0] * 128
        for note in range(128):
            retuning = self.tuning[note][self.in_channel]
            fraction = note + retuning
            whole = int(fraction + resolution / (2 * 100))
            if whole >= 128:
                semitones[note] = 127
                cents[note] = max_cents - 1
            elif whole < 0:
                semitones[note] = 0
                cents[note] = 0
            else:
                semitones[note] = max([0, whole])
                cents[note] = max([0, (fraction - whole) * 100])
        sysex = keybased(
            [i for i in range(127)],
            semitones[:-1],
            cents[:-1],
            self.tuning_program,
            tuning_bank=self.tuning_bank,
            realtime=self.realtime,
            device_number=self.device_number,
        )
        return sysex

    def dispatch(self, msg):
        if msg.type == "note_on":
            self.is_on[msg.note][msg.channel] = True
            if self.query(msg):
                sysex = self.sysex()
                self.outport.send(sysex)
            should_filter = esp.should_filter_note(self.client, msg.note, msg.channel)
            if not should_filter:
                self.is_on[msg.note][msg.channel] = True
                self.outport.send(msg)
        else:
            if msg.type == "note_off":
                self.is_on[msg.note][msg.channel] = False
            self.outport.send(msg)

    def open(self):
        while True:
            is_on = any(self.is_on)
            if is_on:
                self.query()
                time.sleep(1 / self.query_rate)
