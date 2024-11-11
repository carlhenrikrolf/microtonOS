import mido
import time

class MPE:
	
	def __init__(self,
		masters=[0],
		members=range(1,16),
		zone='lower',
		polyphony=14,
	):
		assert all([i not in members for i in masters])
		self.masters = masters
		self.members = members
		self.polyphony = polyphony
		if zone == 'lower':
			self.manager_channel = 0
			self.member_channels = range(1,polyphony+1)
		else:
			raise Warning('upper zones not yet implemented')
		self.active = [False]*polyphony
		self.note_on = [0]*polyphony
		self.note_off = [False]*polyphony
		self.note = [-1]*polyphony
		self.mapping = [-1]*polyphony
			
	def dispatch(self, msg):
		if not hasattr(msg, 'channel'):
			return msg
		elif msg.channel in self.members:
			if msg.type == 'note_on' and msg.velocity > 0:
				if all(self.active):
					i = self.polyphony - 1
					top = max(self.note)
					bottom = min(self.note)
					for j in range(self.polyphony):
						if self.note[j] in [top, bottom]:
							continue
						elif self.note_on[j] < self.note_on[i]:
							i = j
					self.mapping[i] = msg.channel
					self.note[i] = msg.note
					self.note_on[i] = time.perf_counter_ns()
					msg.channel = i + 1
				else:
					i = self.active.index(False)
					self.mapping[i] = msg.channel
					self.note[i] = msg.note
					self.note_on[i] = time.perf_counter_ns()
					self.active[i] = True
					msg.channel = i + 1
			elif msg.type in ['note_on', 'note_off']:
				if msg.channel not in self.mapping or msg.note != self.note[self.mapping.index(msg.channel)]:
					return self.panic()
				i = self.mapping.index(msg.channel)
				self.note_off[i] = True
				msg.channel = i + 1
			elif msg.type == 'polytouch':
				msg.channel = self.manager_channel
			else:
				if msg.channel not in self.mapping:
					return self.panic() # maybe I shouldn't panic here but simply activate a new channel?
				i = self.mapping.index(msg.channel)
				msg.channel = i + 1
		elif msg.channel in self.masters:
			msg.channel = self.manager_channel
			if msg.is_cc(120):
				return self.panic()
		return msg
		
		def panic(self):
			self.active = [False]*self.polyphony
			return mido.Message('control_change', control=120, value=0, channel=self.manager_channel)
			
				
			
