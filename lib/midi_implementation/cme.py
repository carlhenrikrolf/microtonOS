import mido

class WidiMaster:

    client_name = "WIDI Master"
    inports = ["WIDI Master Bluetooth"]
    outports = ["WIDI Master Bluetooth"]

    def is_connected(self):
        out = 0
        for outport in mido.get_output_names():
            out += max([port in self.client_name+':'+outport for port in self.outports])
        for inport in mido.get_input_names():
            out += max([port in self.client_name+':'+inport for port in self.inports])
        return bool(out)

widi_master = WidiMaster()