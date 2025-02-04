# modules
import mtsespy as esp
from utils import Outport, Inport, make_threads
from midi_implementation.midi1 import control_change as cc
from midi_implementation import mts

# parameters
client_name = "Minilogue XD Driver"


# definitions
class Script:
    def minilogue_xd(self, msg):
        to_microtonOS.send(msg)
        if msg.type in ["control_change", "program_change"]:
            to_minilogue_xd.send(msg)

    def microtonOS(self, msg):
        ignore = hasattr(msg, "channel") and msg.channel == 15
        ignore = ignore or msg.type == "program_change"
        ignore = ignore or cc.is_in(msg, cc.bank_select)
        if not ignore:
            if hasattr(msg, "channel"):
                msg.channel = 0
            if msg.is_cc(74):
                msg.control = 1 if msg.value >= 64 else 2
                msg.value = (
                    (msg.value - 64) * 2 if msg.value >= 64 else (63 - msg.value) * 2
                )
            mts_client.dispatch(msg)


# run script
with esp.Client() as esp_client:
    to_microtonOS = Outport(client_name, name="microtonOS")
    to_minilogue_xd = Outport(client_name, name="Minilogue XD")
    mts_client = mts.MtsEsp(to_minilogue_xd, esp_client)
    script = Script()
    from_minilogue_xd = Inport(script.minilogue_xd, client_name, name="Minilogue XD")
    from_microtonOS = Inport(script.microtonOS, client_name, name="microtonOS")
    make_threads([from_minilogue_xd.open, from_microtonOS.open])
