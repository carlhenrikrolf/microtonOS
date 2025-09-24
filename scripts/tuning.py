from midi_implementation import mts
import mtsespy as esp
from debug import P, M

port = P()

with esp.Client() as client:
    mtsesp = mts.MtsEsp(port, client)
    print("first")
    mtsesp.dispatch(M('note_on', note=68, velocity=64))
    print("second")
    mtsesp.dispatch(M('note_on', note=67, velocity=69, channel=4))

