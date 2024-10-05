from midi_implementation.dualo import exquis as xq

class ActiveSensing:
    
    def __init__(self, outport):
        self.outport = outport

    def open(self):
        xq.active_sensing(self.outport)

