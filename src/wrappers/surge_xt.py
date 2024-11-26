# parameters
client_name = 'Surge XT Wrapper'
surge_path = '/usr/bin/surge-xt-cli'
audio_name = 'JACK.system' 

# modules
import mido
import re
import subprocess
from midi_implementation.mpe import set_mpe_mode
from utils import Inport, Outport, handle_terminations

list_devices_command = [
	#'sudo',
	#'-u',
	#'pi',
	surge_path,
	'--list-devices',
]

# definitions
def get_input_id(name):
	output = subprocess.check_output(list_devices_command).decode()
	pattern = '\[(\d+)\] : '+name
	match = re.search(pattern, output)
	if match:
		return str(match.group(1))
	else:
		return None

def get_output_id(name):
	output = subprocess.check_output(list_devices_command).decode()
	pattern = '\[(\d+)\.(\d+)\] : '+name
	match = re.search(pattern, output)
	if match:
		return str(match.group(1))+'.'+str(match.group(2))
	else:
		return None
		

class Script:
	def __init__(self):
		self.is_init = True
		self.commandline = [
			#'sudo',
			#'-u',
			#'pi',
			surge_path,
			'--audio-interface='+get_output_id(audio_name),
			'--audio-ports=0,1',
			'--midi-input='+get_input_id('from '+client_name),
			'--no-stdin',
		]
		self.process = subprocess.Popen(self.commandline)
		handle_terminations(self.process)
	def run(self, msg):
		if self.is_init:
			set_mpe_mode(to_surge_xt, polyphony=13, zone='lower')
			set_mpe_mode(to_surge_xt, polyphony=1, zone='upper')
			self.is_init = False
		to_surge_xt.send(msg)
		
to_surge_xt = Outport(client_name, verbose=False)
script = Script()
from_microtonOS = Inport(script.run, client_name, verbose=False)
from_microtonOS.open()
