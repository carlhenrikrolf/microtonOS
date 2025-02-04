import subprocess
from utils import handle_terminations

cache_path = "/home/pi/microtonOS/config/.librespot/"

command = [
	"/usr/bin/pw-jack",
	"/home/pi/.cargo/bin/librespot",
	"--backend=" + "jackaudio",
	"--cache=" + cache_path,
	"--system-cache=" + cache_path,
	"--enable-oauth",
]

with subprocess.Popen(command) as process:
	handle_terminations(process)
