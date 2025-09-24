#! /home/pi/microtonOS/.venv/bin/python3

import mtsespy as esp

with esp.Client() as c:
	print("<result1>" + str(esp.get_scale_name(c)) + "</result1>")
print("<result2>" + str(esp.get_num_clients()) + "</result2>")
