import subprocess
from utils import handle_terminations

path = "/usr/bin/librespot"  # "/home/pi/.cargo/bin/librespot"
cache_path = "."  # run from tmp directory preferably
name = "Librespot microtonOS"
initial_volume = 20  # default 50, between 0 and 100

command = [
    "/usr/bin/pw-jack",
    path,
    "--name=" + name,
    "--backend=" + "jackaudio",
    "--cache=" + cache_path,
    "--system-cache=" + cache_path,
    "--enable-oauth",
    "--initial-volume=" + str(initial_volume),
]

with subprocess.Popen(command) as process:
    handle_terminations(process)
