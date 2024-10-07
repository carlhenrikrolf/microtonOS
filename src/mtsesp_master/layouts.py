import numpy as np

def generate(height, width, up, right):
    layout = [[0]*width]*height
    last_i = last_j = 0
    for i in range(height-1,-1,-1):
        for j in range(width):
            layout[i][j] = last_j + last_i
            last_j += right
        last_i += up
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
