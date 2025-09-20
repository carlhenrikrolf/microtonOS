from gpiozero import Button
import mido
import signal

from utils import Outport, load_config
from midi_implementation.midi1 import control_change as cc

device_name = "Self"
client_name = "Footswitches"
bounce_time = 0.001

# configurations
config = {
    "control_change": load_config(__file__, "../../config/control_change.toml"),
}
for i in range(16):
    if device_name == config["control_change"]["channel"][i]["device"]:
        internal_channel = i

inner_ring = Button(20, bounce_time=bounce_time)
inner_tip = Button(21, bounce_time=bounce_time)
outer_ring = Button(22, bounce_time=bounce_time)
outer_tip = Button(23, bounce_time=bounce_time)

out = Outport(client_name)


def soft_pedal(is_pressed):
    value = 127 if is_pressed else 0
    msg = mido.Message(
        "control_change", control=cc.soft_pedal, value=value, channel=internal_channel
    )  # cc 67
    out.send(msg)


def sostenuto(is_pressed):
    value = 127 if is_pressed else 0
    msg = mido.Message(
        "control_change", control=cc.sostenuto, value=value, channel=internal_channel
    )  # cc 66
    out.send(msg)


outer_tip.when_pressed = lambda: soft_pedal(True)
outer_tip.when_released = lambda: soft_pedal(False)
inner_tip.when_pressed = lambda: sostenuto(True)
inner_tip.when_released = lambda: sostenuto(False)

signal.pause()
