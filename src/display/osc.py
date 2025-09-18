# external libs
import psutil
from pythonosc.udp_client import SimpleUDPClient
import subprocess
import time

# internal libs
from utils import load_config

# config
config = load_config(__file__, "../../config/microtonOS.toml")
loopback_ip = "127.0.0.1"


# main
class Display:
    def __init__(self, query_rate=0.3):
        self.osc_client = SimpleUDPClient(
            loopback_ip, config["Open Stage Control"]["port"]
        )
        self.query_rate = query_rate
        self.osc_client.send_message("/name", "")
        self.osc_client.send_message("/value", "")
        self.osc_client.send_message("/flipside", "")
        self.system()

    def show(self, name=None, value=None, flipside=None, **kwargs):
        if value is not None:
            self.osc_client.send_message("/name", str(name))
        if value is not None:
            self.osc_client.send_message("/value", str(value))
        if flipside is not None:
            self.osc_client.send_message("/flipside", str(flipside))
        for osc_address, osc_value in kwargs.items():
            self.osc_client.send_message(osc_address, osc_value)

    def run(self):
        while True:
            self.system()
            time.sleep(self.query_rate)

    def system(self):
        cpu_output = psutil.cpu_percent()
        cpu = cpu_output
        self.osc_client.send_message("/cpu", cpu)
        temperature_output = subprocess.check_output(
            ["vcgencmd", "measure_temp"]
        ).decode()
        temperature = float(temperature_output.split("=")[1].split("'")[0])
        self.osc_client.send_message("/temperature", temperature)
