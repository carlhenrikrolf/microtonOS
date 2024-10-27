from colour import Color
from midi_implementation.dualo import exquis as xq
from menu import config
from utils import layout, to_key


layout = [
    [0, 1, 2, 3, 4, 5],
   	[6, 7, 8, 9, 10],
	[11, 12, 13, 14, 15, 16],
	[17, 18, 19, 20, 21],
	[23, 24, 25, 26, 27, 28],
	[29, 30, 31, 32, 33],
	[34, 35, 36, 37, 38, 39],
	[40, 41, 42, 43, 44],
	[45, 46, 47, 48, 49, 50],
	[51, 52, 53, 54, 55],
	[56, 57, 58, 59, 60, 61],
]

def to_key(n):
	key = 0
	for i, row in enumerate(layout):
		for j, val in enumerate(row):
			key += 1
			if n == val:
				return key

engines = range(0,17) # rows 1,2,3
banks = range(23,40) # rows 5,6,7
pgms = range(45,62) # rows 9,10,11


class Sounds:
	
	def __init__(self,
		outport,
		base_color=Color('purple'),
		click_color=Color('white'),
	):
		self.outport = outport
		self.base_color = base_color
		self.click_color = click_color
	
	def select(self, msg):
		
		if xq.is_sysex(msg, [xq.click, xq.sounds, xq.pressed])
		
			for key in xq.keys:
				...
				
			self.is_bank = False
			self.is_pgm = False
		
		elif msg.type == 'note_on':
			
			if msg.note in engines:
				
				self.is_pgm = False
				self.is_bank = True
			
			elif msg.note in banks and self.is_bank:
				
				self.is_pgm = True
			
			elif msg.note in pgms and self.is_pgm:
				
				return port (engine bank pgm)
				
		return None
			
		
		
