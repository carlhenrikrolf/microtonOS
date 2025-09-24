import mido
from midi_implementation import mts

msg = mts.keybased_dump('hej', [i for i in range(128)], [33 if i % 2 else 67 for i in range(128)], 0)

mac_input_name = "MacBookAirM3:MacBookAirM3 Bluetooth"
port = mido.open_output(mac_input_name)
test = mido.Message('note_off', note=69, velocity=32, channel=15)
port.send(test)
port.send(msg)