import mido
import numpy as np
import time


class Sine:
    def __init__(self, outport, control, off=64, channel=0, sample_rate=32):
        self.outport = outport
        self.control = control
        self.off = off
        self.channel = channel
        self.sample_rate = sample_rate

    def open(self):
        while True:
            if self.is_on:
                t = time.perf_counter_ns() / 1e9
                y = round(self.a / 2 * np.sin(self.b * t) + 64)
            else:
                y = self.off
            self.outport.send(
                mido.Message(
                    "control_change",
                    control=self.control,
                    value=y,
                    channel=self.channel,
                )
            )
            time.sleep(1.0 / self.sample_rate)

    def onoff(self, msg, control):
        if msg.is_cc(control):
            self.is_on = True if msg.value >= 64 else False

    def depth(self, msg, control):
        if msg.is_cc(control):
            self.a = msg.value

    def rate(self, msg, control):
        if msg.is_cc(control):
            self.b = msg.value
