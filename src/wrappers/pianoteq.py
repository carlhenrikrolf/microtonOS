# external modules
import subprocess
import os

# internal modules
from utils import (
    Outport,
    Inport,
    handle_terminations,
    load_config,
)
from midi_implementation.midi1 import control_change as cc

# configurations
config = {
    "general_settings": load_config(__file__, "../../config/general_settings.toml"),
    "programs": load_config(__file__, "../../config/programs.toml"),
}
path = config["general_settings"]["Pianoteq"]["path"]
standalone = config["general_settings"]["Pianoteq"]["standalone"]
headless = config["general_settings"]["Pianoteq"]["headless"]
midimapping = config["general_settings"]["Pianoteq"]["midimapping"]
preset0 = config["general_settings"]["Pianoteq"]["preset0"]
files = config["general_settings"]["Pianoteq"]["files"]
directories = config["general_settings"]["Pianoteq"]["directories"]

for index, engine in enumerate(config["programs"]["engine"]):
    if engine["name"] == "Pianoteq":
        break

pwjack = "/usr/bin/pw-jack"
# path = "/usr/bin/" + version
all_files = list(files)
extensions = (".fxp", ".mfxp", ".ptm", ".scl", ".kbm")
for dir in directories:
    for ext in extensions:
        ls = os.listdir(dir)
        for file in ls:
            if file.endswith(extensions):
                all_files.append(dir + file)


# definitions
client_name = "Pianoteq Wrapper"
commandline = [
    pwjack,
    path,
    "--fxp" if preset0.endswith(".fxp") else "--preset",
    preset0,
    "--midimapping",
    midimapping,
]
if headless:
    commandline.append("--headless")
if len(files) > 0:
    commandline.append("--open")
for file in files:
    commandline.append(file)
if len(files) > 0 and preset0.endswith(".fxp"):
    commandline.append(
        preset0
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
if standalone:
    with subprocess.Popen(commandline) as process:
        handle_terminations(process)
        outport = Outport(client_name, verbose=False)
        script = Script()
        inport = Inport(script.run, client_name, verbose=False)
        inport.open()
else:
    outport = Outport(client_name, verbose=False)
    script = Script()
    inport = Inport(script.run, client_name, verbose=False)
    inport.open()
