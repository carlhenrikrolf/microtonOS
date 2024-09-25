#! /home/pi/.venv/bin/python3

# parameters
client_name = 'Pianoteq Wrapper'
verbose = True
pianoteq_path = '/home/pi/Pianoteq 8 STAGE/arm-64bit/Pianoteq 8 STAGE'

# modules
import mido
import subprocess
from utils import Outport, Inport, handle_terminations

# definitions
class Script:
	def __init__(self):
		self.bank = 0
		#self.pianoteq = subprocess.Popen(['sudo','-u', 'pi', pianoteq_path]) # option --headless yields noise
		#handle_terminations(self.pianoteq)
	def process(self, msg):
		if msg.type == 'reset':
			subprocess.run(['systemctl', 'restart', 'pianoteq.service'])
		elif msg.is_cc(0):
			self.bank = msg.value if msg.value < 8 else 0
		else:
			if msg.type == 'program_change':
				msg.program = 16*self.bank + msg.program
			outport.send(msg)

# run script
outport = Outport(client_name)
script = Script()
inport = Inport(script.process, client_name)
inport.open()
