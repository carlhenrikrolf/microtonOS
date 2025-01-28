import subprocess
from utils import handle_terminations

headless = False
bank = "D:2"

commandline = [
    "/usr/bin/pw-jack",
    "/usr/bin/guitarix",
    "--bank=" + bank,
    "--auto-save",
]
if headless:
    commandline.append("--nogui")

with subprocess.Popen(commandline) as process:
    handle_terminations(process)