import mido

client_name='Monitor'

with mido.open_input('to '+client_name, client_name=client_name) as inport:
    for msg in inport:
        print(msg)
