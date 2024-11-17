# parameters
client_name = 'Surge XT Wrapper'
verbose = True
surge_path = '/usr/bin/surge-xt-cli'

#audio_name = 'ALSA.default' # cannot connect
#audio_name = 'ALSA.JACK Audio Connection Kit' # sound but weird echo, moogy saw no tone
#audio_name = 'ALSA.Open Sound System' # cannot open
#audio_name = 'ALSA.PipeWire Sound Server' # cannot open
#audio_name = 'ALSA.Plugin using Speex DSP (resample, agc, denoise, echo, dereverb)'
#audio_name = 'ALSA.Plugin for channel upmix (4,6,8)'
#audio_name = 'ALSA.Plugin for channel downmix (stereo) with a simple spacialization' # cannot find
#audio_name = 'ALSA.snd_rpi_hifiberry_dacplusadc, HiFiBerry DAC+ADC HiFi multicodec-0; Direct hardware device without any conversions'
#audio_name = 'ALSA.snd_rpi_hifiberry_dacplusadc, HiFiBerry DAC+ADC HiFi multicodec-0; Direct sample mixing device'
#audio_name = 'ALSA.snd_rpi_hifiberry_dacplusadc; USB Stream Output' # cannot open
audio_name = 'JACK.system' # same problems as alsa jack audio connection kit
#audio_name = 'JACK.gx_head_amp' # no sound
#audio_name = 'JACK.gx_head_fx' # no sound
#audio_name = 'JACK.a2j' # no sound
#audio_name = 'JACK.Pianoteq' # no sound

# modules
import mido
import re
import subprocess
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
		to_surge_xt.send(msg)
		
to_surge_xt = Outport(client_name)
script = Script()
from_microtonOS = Inport(script.run, client_name)
from_microtonOS.open()
