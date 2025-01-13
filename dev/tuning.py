from midi_implementation import mts
import mtsespy as esp
from debug import P, M

port = P()

with esp.Client() as client:
    mtsesp = mts.MtsEsp(port, client)
    mtsesp.dispatch(M('note_on', note=68, velocity=64))

