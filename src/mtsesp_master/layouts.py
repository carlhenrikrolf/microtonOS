import numpy as np


def generate(height, width, up, right, top_right=69, bottom_right=None, bottom_left=None, top_left=None):
    """
        Generate a layout with number of steps up and number of steps right.
        The function produces a rectangular layout,
        For a hexagonal layout, width and hight should be picked slightly larger,
        so that the matrix can be cropped.
    """
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
    """
        Used for splitting the layout lengthwise.
        Produces a list of coordinates forming a straight line.
    """
    separator = []
    for col in range(width):
        separator.append((round(height/2)-1, col))
    return separator
    
    
def slash(height, width):
    """
        Used for splitting the layout lengthwise.
        Produces a list of coordinates forming a diagonal line.
        the diagonal lines goes from low left to high right.
    """
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
    return separator
    
    
def backslash(height, width):
    """
        Used for splitting the layout lengthwise.
        Produces a list of coordinates forming a diagonal line.
        the diagonal lines goes from high left to low right.
        That is, the reverse of the slash function.
    """
    separator = slash(height, width)
    mid = round(height/2)-1
    n = len(separator)
    inverted = []
    for i in range(n):
        x = separator[i][1]
        y = mid + (mid - separator[i][0])
        inverted.append((y,x))
    return inverted
    
    
def endpoints(separator): # potential add-on. add overlaps
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
    
        
def split(height, width, up, right, separator, kind, top_right=69): # potential addon. add overlap
    """
        Used to create a split layout. The separator can be a dash, a slash, or a backslash.
        The kind is either 'parallel', meaning that
        going past the left side on the lower takes you to right side of the higher.
        Or, the kind is 'sequential', meaning that
        going up the upper right corner on lower takes you to the lower left corner on higher.
    """
    layout = generate(height, width, up, right, top_right=top_right)
    left_end, right_end = endpoints(separator)
    if kind == 'parallel':
        bottom_height = height - right_end[0] - 1
        bottom = generate(bottom_height, width, up, right, top_right=layout[0,0])
    elif kind == 'sequential':
        bottom_height = height - right_end[0]
        bottom = generate(bottom_height, width, up, right, top_right=layout[left_end])
    else:
        raise Warning("kind must be either 'parallel' or 'sequential'. (If both, 'parallel takes precedence.)")
    mid_height = height - bottom_height + 1
    mid = generate(mid_height, width, up, right, bottom_right=bottom[0,-1])
    lower = np.concatenate([mid[:-1,:], bottom])
    for (y,x) in separator:
        for i in range(y+1, height):
            layout[i,x] = lower[i,x]
    for i in separator:
        layout[i] = -1
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
