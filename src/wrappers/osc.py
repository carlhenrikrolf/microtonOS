import subprocess

from utils import load_config

config = load_config(__file__, "../../config/microtonOS.toml")
command = [
    config["pw-jack"]["path"],
    config["node.js"]["path"],
    config["Open Stage Control"]["path"],
    "--load",
    config["Open Stage Control"]["config"],
    "--no-qrcode",
    "--port",
    str(config["Open Stage Control"]["port"]),
]
if config["Open Stage Control"]["ssl"]:
    command.append("--use-ssl")

with subprocess.Popen(command) as osc_server:
    pass
