import mido

class ContinuousControllers:
    
    def bank(self, outport, msb, lsb=None, channel=0):
        common = mido.Message('control_change', control=0, value=msb, channel=channel)
        if lsb is None:
            outport.send(common)
        else:
            outport.send(common)
            outport.send(mido.Message('control_change', control=32, value=lsb, channel=channel))
	
	def expression:
	
	def sustain:
		
	def phaser:
	
	def detune:


continuous_controllers = ContinuousControllers()
