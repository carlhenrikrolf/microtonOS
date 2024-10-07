import numpy as np

def generate(height, width, up, right, upper_right_note=69):
    layout = np.zeros([height,width],int)
    for row in range(height):
        for col in range(width):
            layout[row,col] = up*(height-row) + right*col
    diff = upper_right_note - layout[0,-1]
    layout += diff
    return layout
    

class BaseLayout:

    def __init__(self,
        length,
        width,
    ):
        self.length = length
        self.width = width
        self.upper_right_note = 69
        self.dilation = 3
        self.is_left_right = False
        self.is_up_down = False

        assert hasattr(self, 'layout')
        assert hasattr(self, 'update')
    
    def flip_left_right(self):
        self.layout = np.fliplr(self.layout).tolist()
        self.is_left_right = not self.is_left_right

    def flip_up_down(self):
        self.layout = np.flipud(self.layout).tolist()
        self.is_up_down = not self.is_up_down

    def transpose(upper_right_note):
        difference = upper_right_note - self.upper_right_note
        layout = np.array(self.layout) + difference
        assert (layout in range(128)).all()
        self.layout = layout.tolist()

class Exquis(BaseLayout):
    
    def split(...):
        ...
    
    def dilate(self, dilation):
        if dilation in range(...
        elif ...
        
    
    self.layout = ...

    def reset(self):
        ...

    def update(self,
        is_left_right=self.is_left_right,
        is_up_down=self.is_up_down,
        upper_right_note=self.upper_right_note,
        dilation=self.dilation,
    ):
        ...




class HarmonicTable(BaseLayout):
    ...

class WickiHayden(BaseLayout):
    ...

class Janko(BaseLayout):
    ...
