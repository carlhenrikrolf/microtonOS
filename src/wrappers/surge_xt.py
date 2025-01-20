# modules
import re
import subprocess
#import jack
from midi_implementation.mpe import set_mpe_mode  # , set_pitchbend_sensitivity
from utils import Inport, Outport, handle_terminations, warmup

client_name = "Surge XT Wrapper"
#vocoder_name = "Surge Vocoder Wrapper"
surge_path = ["/usr/bin/pw-jack", "/usr/bin/surge-xt-cli"]
audio_name = "JACK.SonoBus" #"JACK.Built-in Audio Stereo"
#audio_input_name = "JACK."+vocoder_name

list_devices_command = [
    *surge_path,
    "--list-devices",
]



def get_midi_id(name):
    output = subprocess.check_output(list_devices_command).decode()
    pattern = "\[(\d+)\] : " + name
    match = re.search(pattern, output)
    if match:
        return str(match.group(1))
    else:
        return None


def get_audio_id(name, kind=""):
    output = subprocess.check_output(list_devices_command).decode()
    pattern = kind + ": " + "\[(\d+)\.(\d+)\] : " + name
    match = re.search(pattern, output)
    if match:
        return str(match.group(1)) + "." + str(match.group(2))
    else:
        return None
    

#vocoder = jack.Client(vocoder_name)
#
#@vocoder.set_process_callback
#def process(frames):
#    for inport, outport in zip(vocoder.inports, vocoder.outports):
#        inport.get_buffer()[:] = outport.get_buffer()
#
#for channel in 1, 2:
#    vocoder.inports.register('in_'+str(channel))
#    vocoder.outports.register('out_'+str(channel))


class Script:
    def __init__(self):
        self.is_init = True
        self.commandline = [
            *surge_path,
            "--audio-interface=" + get_audio_id(audio_name, "Input Audio Device"),
            "--audio-ports=0,1",
            #"--audio-input-interface=" + get_audio_id(audio_input_name, "Output Audio Device"),
            #"--audio-input-ports=0,1",
            "--midi-input=" + get_midi_id("from " + client_name),
            "--no-stdin",
        ]
        self.process = subprocess.Popen(self.commandline)
        handle_terminations(self.process)

    def run(self, msg):
        if self.is_init:
            set_mpe_mode(to_surge_xt, polyphony=13, zone="lower")
            set_mpe_mode(to_surge_xt, polyphony=1, zone="upper")
            # set_pitchbend_sensitivity(to_surge_xt, 2, 2, polyphony=13, zone='lower')
            # set_pitchbend_sensitivity(to_surge_xt, 2, 2, polyphony=1, zone='upper')
            self.is_init = False
        if msg.type == "pitchwheel":
            if msg.channel in range(1, 15):
                msg.pitch = round(msg.pitch / 24)
        to_surge_xt.send(msg)


#with vocoder:
warmup.client()
to_surge_xt = Outport(client_name, verbose=False)
script = Script()
from_microtonOS = Inport(script.run, client_name, verbose=False)
from_microtonOS.open()
