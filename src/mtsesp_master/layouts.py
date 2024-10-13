import numpy as np


def hexagonal(height, width, up, right, bottom_crop=False, top_right=69):
	layout = np.zeros([height,width],int)
	for row in range(height):
		for col in range(width):
			term = right*((height-row+int(bottom_crop))//2)
			layout[row,col] = up*(height-row) + term + right*col
	diff = top_right - layout[0,-1]
	layout += diff
	return layout


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
	
	
def clean(layout):
	layout[np.argwhere(layout < 0)] = -1
	layout[np.argwhere(layout >= 128)] = -1
	return layout.tolist()
	
	
class BaseLayout:
	
	def __init__(self,
		height,
		width,
		kind,
		dilation=3,
		left_right=False,
		up_down=False,
		top_right=69,
	):
		self.height = height
		self.width = width
		assert kind in ['rectangular', 'hexagonal']
		self.kind = kind
		self.dilation = dilation
		self.left_right = left_right
		self.up_down = up_down
		self.top_right = top_right
		
	def layout(self,
		dilation=None,
		left_right=None,
		up_down=None,
		top_right=None,
	):
		self.dilation = self.dilation if dilation is None else dilation
		self.left_right = self.left_right if left_right is None else left_right
		self.up_down = self.up_down if up_down is None else up_down
		self.top_right = self.top_right if top_right is None else top_right
		if self.dilation not in self.dilation_range():
			raise Warning('Dilation is not in range')
		if self.kind == 'hexagonal':
			layout = self.hexagonal()
			layout = clean(np.flipud(layout)) if self.up_down else clean(layout)
			for i in range(self.height): # crop
				if i % 2 != 0:
					layout[i].pop(-1)
		elif self.kind == 'rectangular':
			layout = self.rectangular().tolist()
			layout = clean(np.flipud(layout)) if self.up_down else clean(layout)
		if self.left_right:
			for i, row in enumerate(layout):
				layout[i] = np.flipud(row).tolist() # flipud because single column in np
		return layout


class Exquis(BaseLayout):
	
	def generalization(self):
		up = self.dilation
		right = 1
		return up, right

	def dilation_range(self):
		return range(1, self.width*2 - 1)

	def hexagonal(self):
		up, right = self.generalization()
		return hexagonal(self.height, self.width+1, up, right, top_right=self.top_right)

	def rectangular(self):
		up, right = self.generalization()
		if self.dilation <= self.width - 1:
			return generate(self.height, self.width, up, right, top_right=self.top_right)
		else:
			separator = dash(self.height, self.width)
			return split(self.height, self.width, up, right, separator, kind='parallel', top_right=self.top_right)

class HarmonicTable(BaseLayout):
	
	def generalization(self):
		up = -self.dilation
		right = 2*self.dilation + 1
		return up, right

	def dilation_range(self):
		return range(0,42) # dummy value

	def hexagonal(self):
		up, right = self.generalization()
		return hexagonal(self.height, self.width+1, up, right, top_right=self.top_right)

	def rectangular(self):
		up, right = self.generalization()
		if self.dilation < self.height/2 + (self.width-1)*5/2: # prel
			return generate(self.height,self.width,up,right,top_right=self.top_right)
		else:
			separator = dash(self.height,self.width)
			return split(self.height,self.width,up,right,separator,kind='sequential',top_right=self.top_right)


def f3(d):
	if d % 3 > 0:
		out = round(d/3)
	else:
		out = 0
		for i in range(1,int(d/3)):
			if i > out and i % 2 > 0:
				out = i
	return out
	

class WickiHayden(BaseLayout):
	
	def generalization(self):
		up = -(2*self.dilation - f3(self.dilation))
		right = 3*self.dilation - 2*f3(self.dilation)
		return up, right

	def dilation_range(self):
		return range(0,42) # dummy value

	def hexagonal(self):
		up, right = self.generalization()
		return hexagonal(self.height, self.width+1, up, right, top_right=self.top_right)

	def rectangular(self):
		up, right = self.generalization()
		if self.dilation < np.sqrt(self.height**2 + self.width**2): # guess
			return generate(self.height,self.width,up,right,top_right=self.top_right)
		else:
			separator = slash(self.height, self.width)
			return split(self.height,self.width,up,right,separator,kind='parallel',top_right=self.top_right)


class Janko(BaseLayout):
	
	def generalization(self):
		up = self.dilation - 2*f3(self.dilation)
		right = f3(self.dilation)
		return up, right

	def dilation_range(self):
		return range(0,42)
	
	def hexagonal(self):
		up, right = self.generalization()
		return hexagonal(self.height, self.width+1, up, right, top_right=self.top_right)
	
	def rectangular(self):
		up, right = self.generalization()
		if self.dilation < np.sqrt(self.height**2 + self.width**2): # guess
			return generate(self.height,self.width,up,right,top_right=self.top_right)
		else:
			separator = backslash(self.height, self.width)
			return split(self.height,self.width,up,right,separator,kind='sequential',top_right=self.top_right)


