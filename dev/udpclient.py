from pythonosc.udp_client import SimpleUDPClient
import subprocess
import psutil

ip = subprocess.check_output(["hostname", "--all-ip-addresses"])
ip = ip.decode()
port = 8080

all_ip = "192.168.50.132"
ip = "127.0.0.1"

osc_client = SimpleUDPClient(all_ip, 8080)
while True:
    cpu = psutil.cpu_percent(interval=1)
    cpu /= 100
    osc_client.send_message("/root/instrument/cc", str(cpu))
    print(cpu)
