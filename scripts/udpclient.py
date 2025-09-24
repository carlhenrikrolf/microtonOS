from pythonosc.udp_client import SimpleUDPClient
import psutil

from utils import load_config

config = load_config(__file__, "../config/microtonOS.toml")
port = config["Open Stage Control"]["port"]
loopback_ip = "127.0.0.1"
osc_client = SimpleUDPClient(loopback_ip, port)
while True:
    cpu = psutil.cpu_percent(interval=1)
    cpu /= 100
    osc_client.send_message("/cpu", cpu)
    print(cpu)
