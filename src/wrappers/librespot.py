import subprocess
from utils import handle_terminations

path = "/usr/bin/librespot" # "/home/pi/.cargo/bin/librespot"
cache_path = "."
name = "Librespot microtonOS"

command = [
	"/usr/bin/pw-jack",
	path,
	"--name=" + name, 
	"--backend=" + "jackaudio",
	"--cache=" + cache_path,
	"--system-cache=" + cache_path,
	"--enable-oauth",
]

with subprocess.Popen(command) as process:
	handle_terminations(process)
