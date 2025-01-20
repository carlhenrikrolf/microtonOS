import subprocess
from utils import handle_terminations

commandline = [
	"/usr/bin/pw-jack",
	"/usr/bin/sonobus",
	"--group=microtonOS",
	"--username=pi",
	"--load-setup=/home/pi/microtonOS/config/setup.sonobus",
	#"--headless",
]

with subprocess.Popen(commandline) as sonobus:
	handle_terminations(sonobus)
