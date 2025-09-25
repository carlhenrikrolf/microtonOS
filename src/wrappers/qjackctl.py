import subprocess

from utils import handle_terminations, load_config

config = {
    "general_settings": load_config(__file__, "../../config/general_settings.toml"),
}
patchbay = config["general_settings"]["QjackCtl"]["patchbay"]
pwjack = "/usr/bin/pw-jack"
command = [
    pwjack,
    "/usr/bin/qjackctl",
    "--start",
    "--active-patchbay",
    patchbay,
]

with subprocess.Popen(command) as process:
    handle_terminations(process)
