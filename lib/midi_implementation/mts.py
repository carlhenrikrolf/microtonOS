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
bulk_dump_reply = 0x01
bulk_dump_reply_bank = 0x04
bulk_dump_request = 0x00
bulk_dump_request_bank = 0x03

# utils
resolution = 100 / 2**14
max_cents = 100 - resolution / 2


def checksum(data):  # dont know if rightly understood
    result = int(hex(data[0]), base=16)
    for d in data[1:]:
        result ^= int(hex(d), base=16)
    result &= 0x7F
    result = int(result)
    return [*data, result]


def encode(name: str, length=16, encoding="ascii"):
    null = " ".encode(encoding).hex()
    null = int(null, base=16)
    result = [null] * length
    for i, letter in enumerate(name):
        if i >= length:
            break
        result[i] = letter.encode(encoding, errors="replace").hex()
        result[i] = int(result[i], base=16)
    return result


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
    assert tuning_bank is None or tuning_bank in range(128)
    assert device_number in range(128)
    ll = len(keys)
    yy = [0] * ll
    zz = [0] * ll
    for i, c in enumerate(cents):
        tmp = round(c / resolution)
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


def keybased_dump( 
    name, notes, cents, tuning_program, tuning_bank=None, device_number=all_devices
):
    # something is not quite right.
    # Pianoteq receives dump messages from Korg, but not from me
    # The OG checksum specification ignored the midi tuning byte
    # however, the correction does not.
    assert len(notes) == len(cents) == 128
    assert all([i is None or i in range(128) for i in notes])
    assert all([c is None or 0 <= c < max_cents for c in cents])
    assert tuning_program in range(128)
    assert tuning_bank is None or tuning_bank in range(128)
    assert device_number in range(128)
    xx = notes
    yy = [0] * 128
    zz = [0] * 128
    for i, c in enumerate(cents):
        if c is None or notes[i] is None:
            xx[i] = 0x7F
            yy[i] = 0x7F
            zz[i] = 0x7F
        else:
            tmp = round(c / resolution)
            yy[i] = tmp // 128
            zz[i] = tmp % 128
    if tuning_bank is None:
        data = [
            universal_non_realtime,
            device_number,
            midi_tuning,
            bulk_dump_reply,
            tuning_program,
        ]
    else:
        data = [
            universal_non_realtime,
            device_number,
            midi_tuning,
            bulk_dump_reply_bank,
            tuning_bank,
            tuning_program,
        ]
    data = [*data, *encode(name)]
    for i in range(128):
        data.append(xx[i])
        data.append(yy[i])
        data.append(zz[i])
    return mido.Message("sysex", data=data)


def octave(n_bytes, channels, realtime=True):
    assert n_bytes in [1, 2]
    raise Warning("Not yet implemented")


def octave_dump(name, n_bytes, tuning_program, tuning_bank, device_number=all_devices):
    assert n_bytes in [1, 2]
    raise Warning("Not yet implemented")


def dump_request(tuning_program, tuning_bank=None, device_number=all_devices):
    assert tuning_program in range(128)
    assert tuning_bank is None or tuning_bank in range(128)
    assert device_number in range(128)
    if tuning_bank is None:
        data = [
            universal_non_realtime,
            device_number,
            midi_tuning,
            bulk_dump_request,
            tuning_program,
        ]
    else:
        data = [
            universal_non_realtime,
            device_number,
            midi_tuning,
            bulk_dump_request_bank,
            tuning_bank,
            tuning_program,
        ]
    return mido.Message("sysex", data=data)


def panic():
    sysex = keybased([i for i in range(127)], [i for i in range(127)], [0] * 127, 0)
    return sysex


def parse(sysex, unit="Hertz"):  # not working, segmentation error, not mts tuning
    assert unit in ["ratios", "Hertz", "semitones"]
    result = [[0.0 for _ in range(16)] for _ in range(128)]
    with esp.Client() as esp_client:
        pass
    esp.parse_midi_data(esp_client, sysex.bin())
    for channel in range(16):
        for note in range(128):
            if unit == "Hertz":
                result[note][channel] = esp.note_to_frequency(esp_client, note, channel)
    return result


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

    def query(self, msg=None):
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
        if msg.type in ["note_on", "note_off"]:
            if msg.type == "note_on" and msg.velocity > 0:
                self.is_on[msg.note][msg.channel] = True
                if self.query(msg):
                    sysex = self.sysex()
                    self.outport.send(sysex)
                should_filter = esp.should_filter_note(
                    self.client, msg.note, msg.channel
                )
                if not should_filter:
                    self.is_on[msg.note][msg.channel] = True
                    self.outport.send(msg)
            else:
                self.is_on[msg.note][msg.channel] = False
        else:
            self.outport.send(msg)

    def open(self):
        while True:
            is_on = any(self.is_on)
            if is_on:
                if self.query():
                    raise Warning("Not yet implemented")
                time.sleep(1 / self.query_rate)
