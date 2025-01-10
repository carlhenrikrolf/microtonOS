# modules
from utils import Outport, Inport, make_threads

# parameters
client_name = "Minilogue XD Driver"


# definitions
class Script:
    def minilogue_xd(self, msg):
        to_microtonOS.send(msg)
        if msg.type in ['control_change', 'program_change', 'sysex']:
            to_minilogue_xd.send(msg)

    def microtonOS(self, msg):
        to_minilogue_xd.send(msg)


# run script
to_microtonOS = Outport(client_name, name="microtonOS")
to_minilogue_xd = Outport(client_name, name="Minilogue XD")
script = Script()
from_minilogue_xd = Inport(script.minilogue_xd, client_name, name="Minilogue XD")
from_microtonOS = Inport(script.microtonOS, client_name, name="microtonOS")
make_threads([from_minilogue_xd.open, from_microtonOS.open])
