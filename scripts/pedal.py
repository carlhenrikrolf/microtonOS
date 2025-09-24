from modulation.pedals import Assign
from utils import Inport

class P:
	def send(self, msg):
		print(msg)
p = P()
assign = Assign(p)
assign.ignored.append(80)

def run(msg):
	assigned = assign.onoff(msg, 80)
	targeted = assign.target(msg)
	assign.source(msg, 64)

inport = Inport(run, client_name='test pedals')
inport.open()
