# modules
import subprocess
from utils import Outport, Inport, handle_terminations, warmup
from midi_implementation.midi1 import control_change as cc

# parameters
client_name = "Pianoteq Wrapper"
commandline = [
    "/usr/bin/pw-jack",
    "/home/pi/Pianoteq 8 STAGE/arm-64bit/Pianoteq 8 STAGE",
    "--preset",
    "NY Steinway D Classical",
]


# definitions
class Script:
    def __init__(self):
        self.bank = 0

    def run(self, msg):
        if msg.is_cc(cc.bank_select[0]):
            self.bank = msg.value if msg.value < 17 else 0
        else:
            if msg.type == "program_change":
                msg.program = min([127, 17 * self.bank + msg.program])
            outport.send(msg)


# run script
warmup.client()
process = subprocess.Popen(commandline)
handle_terminations(process)
outport = Outport(client_name, verbose=False)
script = Script()
inport = Inport(script.run, client_name, verbose=False)
inport.open()
