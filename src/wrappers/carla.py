import subprocess
from utils import handle_terminations, Outport, Inport

# parameters
headless = False
pipewire = "/usr/bin/pw-jack"

# definitions
client_name = "Carla Wrapper"
carla_path = "/home/pi/microtonOS/third_party/Carla/source/frontend/"
carlas = ["carla", "carla-jack-single", "carla-jack-multi"]
config_path = "/home/pi/microtonOS/config/"
command = [
    pipewire,
    carla_path + carlas[2],
    config_path + "carla.carxp",
]
if headless:
    command.append("--no-gui")


class Script:
    def __init__(self):
        self.process = subprocess.Popen(command)
        handle_terminations(self.process)

    def run(self, msg):
        out.send(msg)


# run script
out = Outport(client_name)
script = Script()
from_microtonOS = Inport(script.run, client_name)
from_microtonOS.open()
