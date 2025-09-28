import mido
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq

port_name = "Exquis:Exquis MIDI 1"
for from_xq in mido.get_output_names():
    if port_name in from_xq:
        break
for to_xq in mido.get_input_names():
    if port_name in to_xq:
        break

outport = mido.open_output(to_xq)
devmode = xq.developer_mode("exit")
outport.send(devmode)
devmode = xq.developer_mode("enter", settings=False, sound=False, pads=False)
outport.send(devmode)
request = xq.get_snapshot()
outport.send(request)
with mido.open_input(from_xq) as inport:
    for msg in inport:
        # print(msg)
        d = msg.data
        if d[4] == 9:
            print("prefix:", d[0], d[1], d[2], d[3])
            print("msg type:", d[4])
            print("unknown 1:", d[5])
            print("mpe:", d[6])  # 1 if mpe else polyphonic aftertouch, default 1
            print("pb range:", d[7])  # default 1, values [0,12], 24, 48
            print("mpe channels:", d[8])
            print("midi channel if polytouch:", d[9])
            print("note layout:", d[10])  # these are numbered from 1 though
            print("unknown 7 (1 if note layoot in 0,1, or 2 else 0):", d[11])
            print("unknown 8 (1 if note layoot in 0 or 2 else 0):", d[12])
            print("unknown 9:", d[13])
            print("unknown 10:", d[14])
            print("unknown 11:", d[15])
            break
