from midi_implementation.dualo import exquis as xq


height = 11
width = 6
n_keys = 61


def crop(layout):
    for i in range(height):
        if i % 2 != 0:
            layout[i].pop(0)
    return layout
    
    
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
			for i in range(height):
				for j in range(width):
					if layout[i][j] not in range(0,128):
						layout[i][j] = self.null_note
			cropped_layout = crop(layout)
			mapping = linearize(cropped_layout)
			assert len(mapping) == n_keys
			self.mapping = mapping
			for key, note in enumerate(self.mapping):
				xq.send(outport, xq.sysex(xq.map_key_to_note, key, note))
		if coloring is not None:
			assert len(coloring) == 128
			self.coloring = coloring
		for key, note in enumerate(self.mapping):
			xq.send(outport, xq.sysex(xq.color_key, key, xq.to_color(self.coloring[note])))
			
			
				

isomorphic = Isomorphic()
		
			
		
