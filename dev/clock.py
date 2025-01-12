import mido

client_name = "CLOCK"
i = 0

with mido.open_input("to "+client_name, client_name=client_name) as inport:
	for msg in inport:
		if msg.type == "clock":
			print(msg, "(tick "+str(i)+")")
			i += 1
		elif msg.type in ["reset", "start", "stop"]:
			print(msg)
