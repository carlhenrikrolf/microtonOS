import mido

M = mido.Message

class P:
	def send(self, msg):
		print('send', msg)
p = P()
