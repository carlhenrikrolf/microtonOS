import subprocess
from utils import handle_terminations

headless = False
helpall = True
kind = 1
config = "xentotune.carxp"

carlas = ["carla", "carla-jack-single", "carla-jack-multi"]
command = [
	"/usr/bin/pw-jack",
        "/home/pi/microtonOS/third_party/Carla/source/frontend/"+carlas[kind],
]
if helpall:
	subprocess.run([*command, "--help"])
args = [""] if config is None else ["/home/pi/microtonOS/config/" + config]
options = ["--cnprefix="+"XentoTune"]
if headless:
	options.append("--nogui")

commandline = [
	*command,
	*args,
	*options,
]

with subprocess.Popen(commandline) as carla:
	handle_terminations(carla)
