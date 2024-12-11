import mido
import mtsespy as esp
from numpy import log2

client_name='Monitor'

with esp.Client() as esp_client:
	with mido.open_input('to '+client_name, client_name=client_name) as inport:
		for msg in inport:
			print(msg)
			if hasattr(msg, 'note'):
				f = esp.note_to_frequency(esp_client, msg.note, 0)
				print('frequency =', f)
				c = 1200 * log2(f/440.0)
				print(c, 'cents from A440')
