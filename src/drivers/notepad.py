import subprocess
import time

command = ["sudo", "soundcraft_ctl", "--no-dbus", "-s", "0"]
sleep = 2
while True:
    subprocess.run(command)
    time.sleep(sleep)
