import numpy as np

def generate(height, width, up, right, top_right=69, bottom_right=None, bottom_left=None, top_left=None):
    layout = np.zeros([height,width],int)
    for row in range(height):
        for col in range(width):
            layout[row,col] = up*(height-row) + right*col
    if top_left is not None:
        diff = top_left - layout[0, 0]
    elif bottom_left is not None:
        diff = bottom_left - layout[-1, 0]
    elif bottom_right is not None:
        diff = bottom_right - layout[-1, -1]
    else:
        diff = top_right - layout[0,-1]
    layout += diff
    return layout
    
def dash(height, width):
    separator = []
    for col in range(width):
        separator.append((round(height/2), col))
    return separator
    
def slash(height, width):
    separator = []
    separator.append((round(height/2), round(width/2))
    while True:
        x = separator[-1][1] # up
        y = separator[-1][0] - 1
        if y not in range(height):
            break
        separator.append((y,x))
        x = separator[-1][1] + 1 # right
        #y = separator[-1][0]
        if x not in range(width):
            break
        separator.append((y,x))
        x = separator[-1][1] + 1 # right
        #y = separator[-1][0]
        if x not in range(width):
            break
        separator.append((y,x))
        x = separator[-1][1] + 1 # up right
        y = separator[-1][0] - 1
        if x not in range(width) or y not in range(height):
            break
        separator.append((y,x))
    while True:
        x = separator[0][1] - 1 # down left
        y = separator[0][0] + 1
        if x not in range(width) or y not in range(height):
            break
        separator.insert(0,(y,x))
        x = separator[0][1] - 1 # left
        #y = separator[0][0]
        if x not in range(width):
            break
        separator.insert(0,(y,x))
        x = separator[0][1] - 1 # left
        #y = separator[0][0]
        if x not in range(width):
            break
        separator.insert(0,(y,x))
        #x = separator[0][1] # down
        y = separator[0][0] + 1
        if x not in range(width):
            break
        separator.insert(0,(y,x))
    return separator
    
def backslash(height, width):
    separator = slash(height, width)
    mid = round(height/2)
    n = len(slash)
    for i in range(n):
        separator[i][0] = mid + (mid - separator[i][0])
    return separator
    
        
def split(height, width, up, right, separator, kind, top_right=69):
    layout = generate(height, width, up, right, top_right=top_right)
    side =  max([y for i[0] in separator])
    if kind = 'parallel':
        lower = generate(height-side, width, up, right, top_right=layout[0,0])
        mid = generate(side+1, width, up, right, bottom_left=lower[0,0])
        mid[:-2,:].concatenate(lower)
        for (y,x) in separator:
            for i in range(y+1, height):
                layout[i,x] = mid[i,x]
        for (y,x) in separator:
            layout[y,x] = None
    elif kind = 'sequential':
        ...
    else:
        raise Warning('kind must be parallel or sequential')
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
