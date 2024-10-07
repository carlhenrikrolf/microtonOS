from midi_implementation import exquis as xq

def check_input(layout):
    assert len(layout) == xq.length
    assert all([len(row) == max(xq.widths) for row in layout])

def crop(layout):
    for i in range(xq.length):
        if i % 2 != 0:
            layout[i].pop(0)
        cropped_layout = layout
    return cropped_layout

def linearize(layout):
    mapping = []
    for i in range(10,-1,-1):
        mapping.append(cropped_layout[i])
    return mapping

def remap(outport, layout):
    check_input(layout)
    cropped_layout = crop(layout)
    mapping = linearize(cropped_layout)
    xq.set_map(outport, mapping)

def recolor(outport, note_to_color):
    ...
