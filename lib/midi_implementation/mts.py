import mido
import mtsespy as esp
import time

# sysex bytes
ignore = 0x7F
universal_non_realtime = 0x7E
universal_realtime = 0x7F
all_devices = 0x7F  # i.e. 127. scala2mts uses 0 instead
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
ensure_7bit = 0b01111111


def checksum(data):
    result = data[0]
    for d in data[1:]:
        result ^= d
    result &= ensure_7bit
    return result


def error_correction(sysex):
    """True if correct False otherwise"""
    check = checksum(sysex.data[:-1])
    return check == sysex.data[-1]


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
    yy = [0] * ll
    zz = [0] * ll
    for i, c in enumerate(cents):
        tmp = round(c / resolution)
        yy[i] = tmp // 128
        zz[i] = tmp % 128
    for i in range(ll):
        data.append(keys[i])
        data.append(notes[i])
        data.append(yy[i])
        data.append(zz[i])
    return mido.Message("sysex", data=data)


def keybased_dump(
    name, notes, cents, tuning_program, tuning_bank=None, device_number=all_devices
):
    print("NOT working as intended! Under development")
    assert len(notes) == len(cents) == 128
    assert all([i is None or i in range(128) for i in notes])
    assert all([c is None or 0 <= c < max_cents for c in cents])
    assert tuning_program in range(128)
    assert tuning_bank is None or tuning_bank in range(128)
    assert device_number in range(128)
    data_length = 16 + 128 * 3 + 1
    if tuning_bank is None:
        header_length = 5
        message_length = header_length + data_length
        data=[-1] * message_length
        data[:header_length] = [
            universal_non_realtime,
            device_number,
            midi_tuning,
            bulk_dump_reply,
            tuning_program,
        ]
    else:
        header_length = 6
        message_length = header_length + data_length
        data=[-1] * message_length
        data[:header_length] = [
            universal_non_realtime,
            device_number,
            midi_tuning,
            bulk_dump_reply_bank,
            tuning_bank,
            tuning_program,
        ]
    data[header_length : header_length + 16] = encode(name)
    xx = notes
    yy = [0] * 128
    zz = [0] * 128
    for i, c in enumerate(cents):
        if c is None or notes[i] is None:
            xx[i] = ignore
            yy[i] = ignore
            zz[i] = ignore
        else:
            tmp = round(c / resolution)
            yy[i] = tmp // 128
            zz[i] = tmp % 128
    words = range(header_length + 16, message_length-1, 3)
    for key, i in enumerate(words):
        data[i : i + 3] = [xx[key], yy[key], zz[key]]
    data[message_length-1] = checksum(data[:-1])
    return mido.Message('sysex', data=data)


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


def parse(sysex, unit="Hertz"):
    print("NOT working as intended! Under development")
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
        rx_channel=None,
        tx_channel=None,
        tuning_program=0,
        tuning_bank=None,
        realtime=True,
        device_number=all_devices,
        query_rate=None,
    ):
        self.outport = outport
        self.client = client
        # self.rx_channel = -1 if rx_channel is None else rx_channel
        self.tx_channel = tx_channel
        self.tuning_program = tuning_program
        self.tuning_bank = tuning_bank
        self.realtime = realtime
        self.device_number = device_number
        self.query_rate = query_rate

        self.tuning = [[0 for _ in range(16)] for _ in range(128)]
        self.is_on = [[False for _ in range(16)] for _ in range(128)]
        # self.in_range = [True] * 128

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

    def convert(self, fraction):
        whole = int(fraction + resolution / (2 * 100))
        in_range = False
        if whole >= 128:
            semitones = 127
            cents = max_cents - 1
        elif whole < 0:
            semitones = 0
            cents = 0
        else:
            semitones = max([0, whole])
            cents = max([0, (fraction - whole) * 100])
            in_range = True
        return semitones, cents, in_range

    def send_single_change(self, msg):
        retuning = self.tuning[msg.note][msg.channel]
        fraction = msg.note + retuning
        semitones, cents, in_range = self.convert(fraction)
        sysex = keybased(
            msg.note,
            semitones,
            cents,
            self.tuning_program,
            tuning_bank=self.tuning_bank,
            realtime=self.realtime,
            device_number=self.device_number,
        )
        self.outport.send(sysex)
        return in_range

    def send_dump(self):
        semitones = [i for i in range(128)]
        cents = [0] * 128
        for note in range(128):
            retuning = esp.retuning_in_semitones(
                self.client, note, -1
            )  # self.tuning[note][self.rx_channel]
            fraction = note + retuning
            semitones[note], cents[note], _ = self.convert(fraction)
            # self.in_range[note] = _
        lower = keybased(
            [i for i in range(0, 64)],
            semitones[0:64],
            cents[0:64],
            self.tuning_program,
            tuning_bank=self.tuning_bank,
            realtime=self.realtime,
            device_number=self.device_number,
        )
        self.outport.send(lower)
        upper = keybased(
            [i for i in range(64, 128)],
            semitones[64:128],
            cents[64:128],
            self.tuning_program,
            tuning_bank=self.tuning_bank,
            realtime=self.realtime,
            device_number=self.device_number,
        )
        self.outport.send(upper)

    def dispatch(self, msg):
        if hasattr(msg, "channel"):
            tx_channel = msg.channel if self.tx_channel is None else self.tx_channel
            if msg.type in ["note_on", "note_off"]:
                if msg.type == "note_on" and msg.velocity > 0:
                    self.is_on[msg.note][msg.channel] = True
                    queried = self.query(msg)
                    if queried:
                        self.send_dump()
                    in_range = self.send_single_change(msg)
                    should_filter = esp.should_filter_note(
                        self.client, msg.note, msg.channel
                    )
                    should_filter = (
                        should_filter or not in_range
                    )  # self.in_range[msg.note]
                    if not should_filter:
                        self.is_on[msg.note][msg.channel] = True
                        note_on = msg.copy(channel=tx_channel)
                        self.outport.send(note_on)
                else:
                    self.is_on[msg.note][msg.channel] = False
                    note_off = msg.copy(channel=tx_channel)
                    self.outport.send(note_off)
            else:
                misc = msg.copy(channel=tx_channel)
                self.outport.send(misc)
        else:
            self.outport.send(msg)

    def open(self):
        while True:
            is_on = any(self.is_on)
            if is_on:
                queried = self.query()
                if queried:
                    raise Warning("Not yet implemented")
                time.sleep(1 / self.query_rate)
