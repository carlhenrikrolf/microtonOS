import subprocess
from utils import load_config

config = load_config(__file__, "../../config/microtonOS.toml")
command = [
    config["pw-jack"]["path"],
    config["node.js"]["path"],
    config["Open Stage Control"]["path"],
    "--load",
    config["Open Stage Control"]["config"],
]
with subprocess.Popen(command) as osc:
    pass
