#! /home/pi/microtonOS/.venv/bin/python3

# parameters
client_name = 'Pianoteq Wrapper'

# modules
import mido
import subprocess
from utils import Outport, Inport
from midi_implementation.gm2 import control_change as cc

# definitions
class Script:
	def __init__(self):
		self.bank = 0
	def run(self, msg):
		if msg.type == 'reset':
			subprocess.run(['systemctl', 'restart', 'pianoteq.service'])
		elif msg.is_cc(cc.bank_select[0]):
			self.bank = msg.value if msg.value < 17 else 0
		else:
			if msg.type == 'program_change':
				msg.program = min([127, 17*self.bank + msg.program])
			outport.send(msg)

# run script
outport = Outport(client_name, verbose=False)
script = Script()
inport = Inport(script.run, client_name, verbose=False)
inport.open()
