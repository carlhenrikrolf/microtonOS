from pythonosc.udp_client import SimpleUDPClient
import subprocess
import psutil
import time

from utils import load_config

ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
ip = ip.decode()
port = 8080

config = load_config(__file__, "../../config/microtonOS.toml")
command = [
    config["pw-jack"]["path"],
    config["node.js"]["path"],
    config["Open Stage Control"]["path"],
    "--load",
    config["Open Stage Control"]["config"],
    "--no-qrcode",
    "--port",
    str(port),
]


with subprocess.Popen(command) as osc_server:
    pass
