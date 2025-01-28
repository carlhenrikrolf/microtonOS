import jack
import subprocess
from utils import handle_terminations

headless = True

commandline = [
	"/usr/bin/pw-jack",
	"/usr/bin/sonobus",
	"--group=" + "microtonOS",
	"--username=" + "pi",
	"--load-setup=" + "/home/pi/microtonOS/config/setup.sonobus",
]

if headless:
	commandline.append("--headless")

null = jack.Client("Null")
null.outports.register("out_0")
null.outports.register("out_1")

with null:
	with subprocess.Popen(commandline) as process:
		handle_terminations(process)
