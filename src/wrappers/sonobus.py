import jack
import subprocess
from utils import handle_terminations

# paramters
headless = True
n_inputs = 5

# definitions
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
for i in range(n_inputs):
	null.outports.register("out_" + str(i))
	null.inports.register("in_" + str(i))

with null:
	with subprocess.Popen(commandline) as process:
		handle_terminations(process)
