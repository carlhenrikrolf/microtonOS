import mido
print('apis =', mido.backend.module.get_api_names())
default_api = 'LINUX_ALSA'
experimental_api = 'UNIX_JACK'
a = mido.Backend('mido.backends.rtmidi/LINUX_ALSA')
b = mido.set_backend('mido.backends.rtmidi/UNIX_JACK')
c = mido.Backend('mido.backends.rtmidi/UNIX_JACK')
print(a, b, c)
with mido.open_input('testport', client_names='testclient') as inport:
	for msg in inport:
		print(msg)
