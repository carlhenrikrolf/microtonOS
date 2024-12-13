import mido
import mtsespy as esp
from numpy import log2

client_name='Monitor'
has_ipc = esp.has_ipc()
with esp.Client() as esp_client:
	scale_name = esp.get_scale_name(esp_client)
	print('can' if esp.can_register_master() else 'cannot', 'register MTS-ESP master')
	print('MTS-ESP master', 'has' if has_ipc else 'dooes not have', 'IPC')
	print('has' if esp.has_master(esp_client) else 'does not have', 'MTS-ESP master')
	print(esp.get_num_clients(), 'MTS-ESP clients connected')
	print('tuning is', 'not yet set' if scale_name == "microtonOS is warming up ..." else scale_name)
	with mido.open_input('to '+client_name, client_name=client_name) as inport:
		for msg in inport:
			print(msg)
			if hasattr(msg, 'note'):
				f = esp.note_to_frequency(esp_client, msg.note, -1)
				c = float(1200 * log2(f/440.0))
				n = esp.get_scale_name(esp_client)
				print('frequency =', f, 'which is', round(c), 'cents from A440 in', n)
