import subprocess
from midi_implementation.midi1 import control_change as cc
from utils import handle_terminations, Outport, Inport

headless = False
thru_on_init = True
switch = cc.local_onoff_switch

client_name = "XentoTune Wrapper"
pipewire = "/usr/bin/pw-jack"
carla = "/home/pi/microtonOS/third_party/Carla/source/frontend/carla-jack-multi"
config_path = "/home/pi/microtonOS/config/"
xentotune = [
    pipewire,
    carla,
    config_path + "xentotune.carxp",
    "--cnprefix=Thru",
]
thru = [
    pipewire,
    carla,
    config_path + "thru.carxp",
    "--cnprefix=Thru",
]
if headless:
    xentotune.append("--no-gui")
    thru.append("--no-gui")

class Script:
    def __init__(self):
        self.is_on = not thru_on_init
        command = xentotune if self.is_on else thru
        self.process = subprocess.Popen(command)
        handle_terminations(self.process)

    def switch(self, msg):
        is_on = True if msg.value >= 64 else False
        if is_on != self.is_on:
            self.process.terminate()
            command = xentotune if is_on else thru
            self.process = subprocess.Popen(command)
            self.is_on = is_on

    def run(self, msg):
        if msg.is_cc(switch):
            self.switch(msg)
        else:
            to_xentotune.send(msg)


to_xentotune = Outport(client_name)
script = Script()
from_microtonOS = Inport(script.run, client_name)
from_microtonOS.open()
