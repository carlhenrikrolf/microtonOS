# parameters
client_name = 'WiDi Wrapper'

# modules
import mido
from utils import Outport, Inport

# definitions
class Script:
	def run(self, msg):
		to_widi.send(msg)

# run script
to_widi = Outport(client_name)
script = Script()
from_microtonOS = Inport(script.run, client_name)
from_microtonOS.open()
