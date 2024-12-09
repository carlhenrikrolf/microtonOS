import mido

no_change = [0x7F, 0x7F, 0x7F]
universal_non_realtime = 0x7E
universal_realtime = 0x7F
all_devices = 0x7F
midi_tuning = 0x08
note_change = 0x02
resolution = 0.0061


def single_note_tuning_change(
    keys, notes, cents, tuning_program, device_number=all_devices
):
    if not hasattr(keys, "__len__"):
        keys = [keys]
        notes = [notes]
        cents = [cents]
    ll = len(keys)
    yy = [0] * ll
    zz = [0] * ll
    for i, c in enumerate(cents):
        tmp = round(c / resolution)
        yy[i] = tmp // 128
        zz[i] = tmp % 128
    data = [universal_realtime, device_number, midi_tuning, note_change, tuning_program, ll]
    for i in range(ll):
        data.append(keys[i])
        data.append(notes[i])
        data.append(yy[i])
        data.append(zz[i])
    return mido.Message("sysex", data=data)


class OmniOff:
    pass
