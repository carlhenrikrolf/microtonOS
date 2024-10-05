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
					
class NewEngine:
	def __init__(self, name, verbose=True):
		self.name = name
		self.verbose = verbose
		while True:
			try:
				self.output = mido.open_output('to '+self.name)
				self.error = False
				break
			except:
				self.error = True
				print('Failed to connect to port', self.name, 'Trying again.')
				time.sleep(1)
	def change(self, new):
		self.name = new
		self.output.close()
		try:
			self.output = mido.open_output('to '+self.name)
			self.error = False
		except:
			self.output = mido.open_output()
			self.error = True
			print('Failed to connect to port', self.name, 'Connected to default port.')
	def send(self, msg):
		self.output.send(msg)
		if self.verbose and not is_expression(msg):
			if self.error:
				print('Not sending (no connection):', msg)
			else:
				if self.name is None:
					print('Send:', msg)
				else:
					print('Send (to '+self.name+'):', msg)
			
		
					
class Engine:
	ids = ['']*5
	ids[0] = 'to Acoustic Pianoteq Wrapper'
	ids[1] = 'to Electric Pianoteq Wrapper'
	ids[2] = 'to tuneBfree Wrapper'
	ids[3] = 'to Surge XT Wrapper'
	ids[4] = 'to Reface CP Wrapper'
	def __init__(self, verbose=True):
		self.verbose = verbose
		self.current_engine = self.ids[0]
		try:
			self.outport = mido.open_output(self.current_engine)
			self.error = False
		except:
			self.outport = mido.open_output()
			self.error = True
	def change(self, msg):
		if msg.is_cc(0):
			self.outport.close()
			self.current_engine = self.ids[msg.value]
			if msg.value < len(self.ids):
				try:
					self.outport = mido.open_output(self.current_engine)
					self.error = False
				except:
					self.outport = mido.open_output()
					self.error = True
			else:
				self.outport = mido.open_output()
				self.error = True
			return True
		else:
			return False
	def send(self, msg):
		self.outport.send(msg)
		if self.verbose:
			if self.error:
				print('Send to NOWHERE:', msg)
			else:
				print('Send (to '+self.current_engine+'):', msg)
				
def make_threads(functions):
	n = len(functions)
	threads = [None]*n
	for i in range(n):
		threads[i] = threading.Thread(target=functions[i], daemon=True)
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
				
				
			
			

			
			

		
