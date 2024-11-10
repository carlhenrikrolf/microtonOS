import mido
import time

n_channels = 16

class MPE:
	
	def __init__(self, indim, outdim):
		
		self.indim = indim
		self.outdim = outdim
		
		self.note = [-1]*outdim
		self.note_on = [-1]*outdim
		self.note_off = [-1]*outdim
		self.sustain = [0]*outdim
	
	def rescale(msg):
		if self.indim in range(3,n_channels):
			if self.outdim in range(3,n_channels):
				if msg.type == 'note_on':
					if msg.channel > 0:
						if self.note[msg.channel] < 0:
							self.note[msg.channel] = msg.note
							self.note_on[msg.channel] = time.ns_...()
							return msg
						elif -1 in self.note:
							i = self.note[1:].index(-1)
							...
					else:
						return msg
						
				
			elif self.outdim in range(-3,-n_channels,-1):
				
		elif self.indim in range(-3,-n_channels,-1):
			pass
		else:
			raise Warning('small dimensions of zones not yet implemented')
			
