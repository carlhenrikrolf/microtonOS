# external modules
import subprocess
import os

# internal modules
from utils import Outport, Inport, handle_terminations, load_config
from midi_implementation.midi1 import control_change as cc

# configurations
config = {
    "microtonOS": load_config(__file__, "../../config/microtonOS.toml"),
}
pw_jack = config["microtonOS"]["pw-jack"]["path"]
for index, engine in enumerate(config["microtonOS"]["engine"]):
    if engine["name"] == "Pianoteq":
        break
headless = engine["headless"]
path = engine["path"]
preset = engine["preset"]
midimapping = engine["midimapping"]
files = list(engine["files"])
extensions = (".fxp", ".mfxp", ".ptm", ".scl", ".kbm")
for dir in engine["directories"]:
    for ext in extensions:
        ls = os.listdir(dir)
        for file in ls:
            if file.endswith(extensions):
                files.append(dir + file)


# definitions
client_name = "Pianoteq Wrapper"
commandline = [
    pw_jack,
    path,
    "--fxp" if preset.endswith(".fxp") else "--preset",
    preset,
    "--midimapping",
    midimapping,
]
if headless:
    commandline.append("--headless")
if len(files) > 0:
    commandline.append("--open")
for file in files:
    commandline.append(file)
if len(files) > 0 and preset.endswith(".fxp"):
    commandline.append(
        preset
    )  # --preset or --fxp options are not active after other .fxp files are loaded


class Script:
    def __init__(self):
        self.is_on = index == 0
        self.bank = 0

    def run(self, msg):
        if msg.is_cc(cc.bank_select[0]):
            self.bank = msg.value if msg.value < 11 else 0
        elif msg.is_cc(cc.bank_select[1]):
            self.is_on = msg.value == index
        elif self.is_on:
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
