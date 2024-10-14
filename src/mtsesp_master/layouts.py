import numpy as np


def hexagonal(height, width, up, right, bottom_crop=False, top_right=69, bottom_right=None, bottom_left=None, top_left=None):
	layout = np.zeros([height,width],int)
	for row in range(height):
		for col in range(width):
			term = right*((height-row+int(bottom_crop))//2)
			layout[row,col] = up*(height-row) + term + right*col
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


def rectangular(height, width, up, right, bottom_crop=None, top_right=69, bottom_right=None, bottom_left=None, top_left=None):
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
	
	
def backslash(height, width):
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
	flipped_separator = [(y,width-1-x) for (y,x) in separator]
	return flipped_separator
	
	
def slash(height, width):
	separator = backslash(height, width)
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
	
		
def split(height, width, up, right, grid, separation, kind, top_right=69, overlap=1):
	"""
		Used to create a split layout.
		grid is either rectangular or square from above
		The separator can be a dash, a slash, or a backslash.
		The kind is either 'parallel', meaning that
		going past the left side on the lower takes you to right side of the higher.
		Or, the kind is 'sequential', meaning that
		going up the upper right corner on lower takes you to the lower left corner on higher.
	"""
	layout = grid(height, width, up, right, top_right=top_right)
	separator = separation(height, width)
	left_end, right_end = endpoints(separator)
	if kind == 'parallel':
		bottom_height = height - right_end[0] - 1
		bottom = grid(bottom_height, width, up, right, top_right=layout[0,0+overlap])
	elif kind == 'sequential':
		bottom_height = height - right_end[0]
		bottom = grid(bottom_height, width, up, right, top_right=layout[left_end[0],left_end[1]+overlap])
	else:
		raise Warning("kind must be either 'parallel' or 'sequential'. (If both, 'parallel takes precedence.)")
	mid_height = height - bottom_height + 1
	overlap_crop = False if bottom_height % 2 > 0 else True
	mid = grid(mid_height, width, up, right, bottom_crop=overlap_crop, bottom_right=bottom[0,-1])
	lower = np.concatenate([mid[:-1,:], bottom])
	for (y,x) in separator:
		for i in range(y+1, height):
			layout[i,x] = lower[i,x]
	for i in separator:
		layout[i] = -1
	return layout
	
	
def clean(layout):
	clean_layout = layout.tolist()
	for i, row in enumerate(clean_layout):
		for j, note in enumerate(row):
			if note not in range(0,128):
				clean_layout[i][j] = -1
	return clean_layout
	
	
def crop(layout):
	n = len(layout)
	for i, row in enumerate(layout):
		if (n-i) % 2 == 0:
			row.pop(-1)
	return layout
	
	
class BaseLayout:
	
	def __init__(self,
		height,
		width,
		kind,
		dilation=3,
		is_left_right=False,
		is_up_down=False,
		top_right=69,
	):
		self.height = height
		self.width = width
		assert kind in ['rectangular', 'hexagonal']
		self.kind = kind
		self.dilation = dilation
		self.is_left_right = is_left_right
		self.is_up_down = is_up_down
		self.top_right = top_right
		
	def layout(self,
		dilation=None,
		is_left_right=None,
		is_up_down=None,
		top_right=None,
	):
		self.dilation = self.dilation if dilation is None else dilation
		self.is_left_right = self.is_left_right if is_left_right is None else is_left_right
		self.is_up_down = self.is_up_down if is_up_down is None else is_up_down
		self.top_right = self.top_right if top_right is None else top_right
		if self.dilation not in self.dilation_range():
			raise Warning('Dilation is not in range')
		if self.kind == 'hexagonal':
			layout = self.hexagonal()
			layout = clean(np.flipud(layout)) if self.is_up_down else clean(layout)
			layout = crop(layout)
		elif self.kind == 'rectangular':
			layout = self.rectangular().tolist()
			layout = clean(np.flipud(layout)) if self.is_up_down else clean(layout)
		if self.is_left_right:
			for i, row in enumerate(layout):
				layout[i] = np.flipud(row).tolist() # flipud because single column in np
		return layout


class Exquis(BaseLayout):
	
	def generalization(self):
		up = self.dilation
		right = 1
		return up, right

	def dilation_range(self):
		return range(1, 17)

	def hexagonal(self):
		up, right = self.generalization()
		if self.dilation <= 5:
			layout = hexagonal(
				self.height, self.width+1,
				up, right,
				top_right=self.top_right,
			)
		else:
			layout = split(
				self.height,
				self.width+1,
				up, right,
				hexagonal,
				dash,
				kind='parallel',
				top_right=self.top_right,
			)
		return layout

class HarmonicTable(BaseLayout):
	
	def generalization(self):
		up = -self.dilation
		right = 2*self.dilation + 1
		return up, right

	def dilation_range(self):
		return range(1,17)

	def hexagonal(self):
		up, right = self.generalization()
		if self.dilation <= 5:
			layout = hexagonal(
				self.height, self.width+1,
				up, right,
				top_right=self.top_right,
			)
		else:
			layout = split(
				self.height, self.width+1,
				up, right,
				hexagonal,
				dash,
				kind='sequential',
				overlap=0,
			)
		return layout


def f3(d):
	if d % 3 > 0:
		out = round(d/3)
	else:
		out = 0
		for i in range(1,int(d/3)+1):
			if i > out and i % 2 > 0:
				out = i
	return out
	

class WickiHayden(BaseLayout):
	
	def generalization(self):
		up = -(2*self.dilation - f3(self.dilation))
		right = 3*self.dilation - 2*f3(self.dilation)
		return up, right

	def dilation_range(self):
		return range(1,17)

	def hexagonal(self):
		up, right = self.generalization()
		if self.dilation <= 5:
			layout = hexagonal(
				self.height, self.width+1,
				up, right,
				top_right=self.top_right,
			)
		else:
			layout = split(
				self.height, self.width+1,
				up, right,
				hexagonal,
				backslash,
				kind='parallel',
				top_right=self.top_right,
			)
		return layout
				


class Janko(BaseLayout):
	
	def generalization(self):
		up = self.dilation - 2*f3(self.dilation)
		right = f3(self.dilation)
		return up, right

	def dilation_range(self):
		return range(1,17)
	
	def hexagonal(self):
		up, right = self.generalization()
		if self.dilation <= 5:
			layout = hexagonal(
				self.height, self.width+1,
				up, right,
				top_right=self.top_right
			)
		else:
			layout = split(
				self.height, self.width+1,
				up, right,
				hexagonal,
				slash,
				kind='sequential',
				top_right=self.top_right,
			)
		return layout


