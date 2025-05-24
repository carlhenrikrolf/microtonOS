# external libs
from pythonosc.udp_client import SimpleUDPClient

# internal libs
from utils import load_config

# configs
config = load_config(__file__, "../../config/microtonOS.toml")

# initialisation
loopback_ip = "127.0.0.1"
osc_client = SimpleUDPClient(loopback_ip, config["Open Stage Control"]["port"])


# main
def display(address, value):
    osc_client.send_message(address, value)
