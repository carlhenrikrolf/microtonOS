# modules
from utils import Outport, Inport, make_threads

# parameters
client_name = "widi Driver"


# definitions
class Script:
    def widi(self, msg):
        to_microtonOS.send(msg)

    def microtonOS(self, msg):
        pass


# run script
to_microtonOS = Outport(client_name, name="microtonOS")
to_widi = Outport(client_name, name="widi")
script = Script()
from_widi = Inport(script.widi, client_name, name="widi")
from_microtonOS = Inport(script.microtonOS, client_name, name="microtonOS")
make_threads([from_widi.open, from_microtonOS.open])