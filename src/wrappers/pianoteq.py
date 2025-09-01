# external modules
import subprocess

# internal modules
from utils import Outport, Inport, handle_terminations, load_config
from midi_implementation.midi1 import control_change as cc

# configurations
config = {
    "microtonOS": load_config(__file__, "../../config/microtonOS.toml"),
}
pw_jack = config["microtonOS"]["pw-jack"]["path"]
for i, engine in enumerate(config["microtonOS"]["engine"]):
    if engine["name"] == "Pianoteq":
        break
headless = engine["headless"]
path = engine["path"]
preset = engine["preset"]
midimapping = engine["midimapping"]
files = engine["files"]

# definitions
client_name = "Pianoteq Wrapper"
commandline = [
    pw_jack,
    path,
    "--preset",
    preset,
    "--midimapping",
    midimapping,
]
if headless:
    commandline.append("--headless")
commandline.append("--open")
commandline.append(files)


class Script:
    def __init__(self):
        self.bank = 0

    def run(self, msg):
        if msg.is_cc(cc.bank_select[0]):
            self.bank = msg.value if msg.value < 11 else 0
        else:
            if msg.type == "program_change":
                msg.program = min([127, 11 * self.bank + msg.program])
            outport.send(msg)


# run script
process = subprocess.Popen(commandline)
handle_terminations(process)
outport = Outport(client_name, verbose=False)
script = Script()
inport = Inport(script.run, client_name, verbose=False)
inport.open()
