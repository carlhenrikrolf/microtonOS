from gpiozero import Button

import mido
import signal

from utils import Outport
from midi_implementation.midi1 import control_change as cc

client_name = "Footswitches"
bounce_time = 0.001

inner_ring = Button(20, bounce_time=bounce_time)
inner_tip = Button(21, bounce_time=bounce_time)
outer_ring = Button(22, bounce_time=bounce_time)
outer_tip = Button(23, bounce_time=bounce_time)

out = Outport(client_name)


def soft_pedal(is_pressed):
    value = 127 if is_pressed else 0
    msg = mido.Message("control_change", control=cc.soft_pedal, value=value)  # cc 67
    out.send(msg)


def sostenuto(is_pressed):
    value = 127 if is_pressed else 0
    msg = mido.Message("control_change", control=cc.sostenuto, value=value)  # cc 66
    out.send(msg)


outer_tip.when_pressed = lambda: soft_pedal(True)
outer_tip.when_released = lambda: soft_pedal(False)
inner_tip.when_pressed = lambda: sostenuto(True)
inner_tip.when_released = lambda: sostenuto(False)

signal.pause()
