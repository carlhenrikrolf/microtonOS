# external modules
import subprocess

# internal modules
from utils import (
    Outport,
    Inport,
    handle_terminations,
    load_config,
)

config = {
    "general_settings": load_config(__file__, "../../config/general_settings.toml")
}
path = config["general_settings"]["DecentSampler"]["path"]
standalone = config["general_settings"]["DecentSampler"]["standalone"]
drumkit = config["general_settings"]["DecentSampler"]["drumkit"]

client_name = "DecentSampler Wrapper"
pwjack = "/usr/bin/pw-jack"
commandline = [pwjack, path, drumkit]


class Drumkit:
    def run(self, msg):
        from_rhythm.send(msg)


# run script
if standalone:
    with subprocess.Popen(commandline) as process:
        handle_terminations(process)
        from_rhythm = Outport(client_name, name="Rhythm", verbose=False)
        drumkit = Drumkit()
        to_drumkit = Inport(drumkit.run, client_name, verbose=False)
        to_drumkit.open()
else:
    from_rhythm = Outport(client_name, name="Rhythm", verbose=False)
    drumkit = Drumkit()
    to_drumkit = Inport(drumkit.run, client_name, verbose=False)
    to_drumkit.open()
