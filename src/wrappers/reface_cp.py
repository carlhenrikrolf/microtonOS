#! /home/pi/.venv/bin/python3

# parameters
client_name = 'Reface CP Wrapper'
verbose = True

# modules
import mido
from utils import Outport, Inport

# definitions
class Script:
	def process(self, msg):
		if msg.type == 'program_change' and msg.program < 6:
			outport.send(mido.Message('control_change', control=80, value=int(127/6*msg.program+127/6/2)))
		elif msg.type in ['aftertouch', 'polytouch']:
			outport.send(mido.Message('control_change', control=1, value=msg.value))
		elif msg.is_cc(74):
			outport.send(mido.Message('control_change', control=11, value=msg.value))
		else:
			outport.send(msg)

# run script
outport = Outport(client_name)
script = Script()
inport = Inport(script.process, client_name)
inport.open()
