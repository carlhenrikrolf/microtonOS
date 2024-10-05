import mido
import threading
import time
import signal
import sys

def is_expression(msg):
	if msg.type in ['aftertouch', 'polytouch', 'pitchwheel']:
		return True
	elif msg.is_cc(74):
		return True
	else:
		return False

class Outport:
	def __init__(self, client_name, name=None, verbose=True):
		self.name = name
		self.verbose = verbose
		if self.name is None:
			self.output = mido.open_output('from '+client_name, client_name=client_name)
		else:
			self.output = mido.open_output(self.name+' from '+client_name, client_name=client_name)
	def send(self, msg):
		self.output.send(msg)
		if self.verbose and not is_expression(msg):
			if self.name is None:
				print('Send:', msg)
			else:
				print('Send (to '+self.name+'):', msg)

class Inport:
	def __init__(self, process, client_name, name=None, verbose=True, length=None):
		self.process = process
		self.client_name=client_name
		self.name=name
		self.verbose = verbose
		self.length = length
	def open(self):
		if self.name is None:
			with mido.open_input('to '+self.client_name, client_name=self.client_name) as inport:
				if self.length is None:
					for msg in inport:
						if self.verbose and not is_expression(msg):
							print('Receive:', msg)
						self.process(msg)
				else:
					pending = list(inport.iter_pending())
					for i, msg in enumerate(pending):
						if self.verbose and not is_expression(msg):
							print('Receive:', msg)
						if not (msg.type in ['aftertouch', 'polytouch']) and i<len(pending):
							self.process(msg)
					time.sleep(self.length)
		else:
			with mido.open_input(self.name+' to '+self.client_name, client_name=self.client_name) as inport:
				for msg in inport:
					if self.length is None:
						if self.verbose and not is_expression(msg):
							print('Receive (from '+self.name+'):', msg)
						self.process(msg)
					else:
						pending = list(inport.iter_pending())
						for i, msg in enumerate(pending):
							if self.verbose and not is_expression(msg):
								print('Receive:', msg)
							if not (msg.type in ['aftertouch', 'polytouch']) and i<len(pending):
								self.process(msg)
						time.sleep(self.length)

				
def make_threads(functions, args=None):
	n = len(functions)
	args = [()]*n if args is None else args
	threads = [None]*n
	for i in range(n):
		threads[i] = threading.Thread(target=functions[i], args=args[i], daemon=True)
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
		
		
		
def handle_terminations(processes):
	def signal_handler(signum, frame):
		if type(processes) is list or type(processes) is tuple:
			for process in processes:
				process.terminate()
		else:
			processes.terminate()
		sys.exit(0)
	signal.signal(signal.SIGTERM, signal_handler)
				
				
			
			

			
			

		
