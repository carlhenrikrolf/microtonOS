from gpiozero import Button
from gpiozero.pins.rpigpio import RPiGPIOFactory  # Changed from lgpio
import mido
import signal

from utils import Outport

client_name = "Footswitches"
tip_gpio = 23
ring_gpio = 22
bounce_time = 0.01

plug_cc = mido.Message("control_change", control=4)
latch_cc = mido.Message("control_change", control=36)


pin_factory = RPiGPIOFactory()  # Changed from LGPIOFactory
tip = Button(tip_gpio, bounce_time=bounce_time, pin_factory=pin_factory)
ring = Button(ring_gpio, bounce_time=bounce_time, pin_factory=pin_factory)


class Switch:
    def __init__(self):
        self.is_plugged = ring.is_pressed
        self.is_latched = False
        self.update()
        out.send(plug_cc)
        out.send(latch_cc)

    def update(self):
        plug_cc.value = 127 if self.is_plugged else 0
        latch_cc.value = 127 if self.is_latched else 64

    def latch(self):
        self.is_latched = not self.is_latched
        self.update()
        if self.is_plugged:
            out.send(latch_cc)

    def plug(self):
        self.is_plugged = True
        self.update()
        out.send(plug_cc)

    def unplug(self):
        self.is_plugged = False
        self.update()
        out.send(plug_cc)


out = Outport(client_name)

switch = Switch()

tip.when_pressed = switch.latch
ring.when_pressed = switch.plug
ring.when_released = switch.unplug

signal.pause()
