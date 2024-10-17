from midi_implementation.dualo import exquis as xq
from colour import Color


height = 11
width = 5
n_keys = 61
    
    
def linearize(layout):
    mapping = []
    for row in layout:
        mapping = [*row, *mapping]
    return mapping
    

class Isomorphic:
	
	null_note = 127
	
	def ignore(self, msg):
		if hasattr(msg, 'note') and msg.note == self.null_note:
			return True
		else:
			return False
			
	def send(self, outport, layout=None, coloring=None):
		if layout is not None:
			assert len(layout) == height
			assert min([len(row) for row in layout]) == width
			mapping = linearize(layout)
			for key, note in enumerate(mapping):
				if note not in range(0,128):
					mapping[key] = self.null_note
			assert len(mapping) == n_keys
			self.mapping = mapping
			for key, note in enumerate(self.mapping):
				xq.send(outport, xq.sysex(xq.map_key_to_note, key, note))
		if coloring is not None:
			assert len(coloring) == 128
			self.coloring = coloring
		for key, note in enumerate(self.mapping):
			if note == self.null_note:
				xq.send(outport, xq.sysex(xq.color_key, key, [32, 32, 32]))
			else:
				xq.send(outport, xq.sysex(xq.color_key, key, xq.to_color(self.coloring[note])))
				

isomorphic = Isomorphic()
		
			
		
