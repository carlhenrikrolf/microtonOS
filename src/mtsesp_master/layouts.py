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
    return layout # works
    
def dash(height, width):
    separator = []
    for col in range(width):
        separator.append((round(height/2)-1, col))
    return separator # works
    
def slash(height, width):
    separator = []
    separator.append((round(height/2)-1, round(width/2)))
    while True:
        x = separator[-1][1] # up
        y = separator[-1][0] - 1
        if y not in range(height):
            break
        separator.append((y,x))
        x = separator[-1][1] + 1 # right
        if x not in range(width):
            break
        separator.append((y,x))
        x = separator[-1][1] + 1 # right
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
        if x not in range(width):
            break
        separator.insert(0,(y,x))
        x = separator[0][1] - 1 # left
        if x not in range(width):
            break
        separator.insert(0,(y,x))
        y = separator[0][0] + 1
        if x not in range(width):
            break
        separator.insert(0,(y,x))
    return separator # works
    
def backslash(height, width):
    separator = slash(height, width)
    mid = round(height/2)-1
    n = len(separator)
    inverted = []
    for i in range(n):
        x = separator[i][1]
        y = mid + (mid - separator[i][0])
        inverted.append((y,x))
    return inverted # works
    
def endpoints(separator):
    xmin = min([i[1] for i in separator])
    xmax = max([i[1] for i in separator])
    ymax = max([i[0] for i in separator])
    ymin = min([i[0] for i in separator])
    lefts = []
    rights = []
    for i in separator:
        if i[1] == xmin:
            lefts.append(i)
        if i[1] == xmax:
            rights.append(i)
    left = lefts[0]
    for i in lefts:
        if min(abs(i[0]-ymax),abs(i[0]-ymin)) > min(abs(left[0]-ymax),abs(left[0]-ymin)):
            left = i
    right = rights[0]
    for i in rights:
        if min(abs(i[0]-ymax),abs(i[0]-ymin)) > min(abs(right[0]-ymax),abs(right[0]-ymin)):
            right = i     
    return left, right
    
        
def split(height, width, up, right, separator, kind, top_right=69):
    layout = generate(height, width, up, right, top_right=top_right)
    left_end, right_end = endpoints(separator)
    if kind == 'parallel':
        bottom_height = height - separator[-1][0] - 1
        bottom = generate(bottom_height, width, up, right, top_right=layout[0,0])
        mid_height = height - bottom_height + 1
        mid = generate(mid_height, width, up, right, bottom_right=bottom[0,-1])
        lower = np.concatenate([mid[:-1,:], bottom])
        for (y,x) in separator:
            for i in range(y+1, height):
                layout[i,x] = lower[i,x]
        for i in separator:
            layout[i] = -1 # works
    elif kind == 'sequential':
        bottom_height = height - separator[-1][0]
        bottom = generate(bottom_height, width, up, right, top_right=layout[left_end])
        mid_height = height - bottom_height + 1
        mid = generate(mid_height, width, up, right, bottom_right=bottom[0,-1])
        lower = np.concatenate([mid[:-1,:], bottom])
        for (y,x) in separator:
            for i in range(y+1, height):
                layout[i,x] = lower[i,x]
        for i in separator:
            layout[i] = -1
        
    # else:
        # raise Warning('kind must be parallel or sequential')
    return layout
    

# class BaseLayout:

    # def __init__(self,
        # length,
        # width,
    # ):
        # self.length = length
        # self.width = width
        # self.upper_right_note = 69
        # self.dilation = 3
        # self.is_left_right = False
        # self.is_up_down = False

        # assert hasattr(self, 'layout')
        # assert hasattr(self, 'update')
    
    # def flip_left_right(self):
        # self.layout = np.fliplr(self.layout).tolist()
        # self.is_left_right = not self.is_left_right

    # def flip_up_down(self):
        # self.layout = np.flipud(self.layout).tolist()
        # self.is_up_down = not self.is_up_down

    # def transpose(upper_right_note):
        # difference = upper_right_note - self.upper_right_note
        # layout = np.array(self.layout) + difference
        # assert (layout in range(128)).all()
        # self.layout = layout.tolist()

# class Exquis(BaseLayout):
    
    # def split(...):
        # ...
    
    # def dilate(self, dilation):
        # if dilation in range(...
        # elif ...
        
    
    # self.layout = ...

    # def reset(self):
        # ...

    # def update(self,
        # is_left_right=self.is_left_right,
        # is_up_down=self.is_up_down,
        # upper_right_note=self.upper_right_note,
        # dilation=self.dilation,
    # ):
        # ...




# class HarmonicTable(BaseLayout):
    # ...

# class WickiHayden(BaseLayout):
    # ...

# class Janko(BaseLayout):
    # ...
