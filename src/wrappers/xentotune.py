import subprocess
from midi_implementation.midi1 import control_change as cc
from utils import handle_terminations, Outport, Inport

headless = False
switch = cc.local_onoff_switch

client_name = "XentoTune Wrapper"
pipewire = "/usr/bin/pw-jack"
bin_path = "/home/pi/microtonOS/third_party/Carla/source/frontend/carla-jack-single"
config_path = "/home/pi/microtonOS/config/"
xentotune = [
    pipewire,
    bin_path,
    config_path + "xentotune.carxp",
    "--no-gui" if headless else "",
]
thru = [
    pipewire,
    bin_path,
    config_path + "thru.carxp",
    "--no-gui" if headless else "",
]


class Script:
    def __init__(self):
        self.process = subprocess.Popen(thru)
        handle_terminations(self.process)
        self.is_on = False

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
