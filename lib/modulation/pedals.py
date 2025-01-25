import mido

from midi_implementation.midi1 import control_change as cc


class Assign:
    ignored = cc.not_knobs

    def __init__(self, outport, channel=0):
        self.outport = outport
        self.channel = channel
        self.assigned = None
        self.control = None
        self.knob = 64
        self.pedal = 0

    def out(self):
        a = (self.knob - 64) / 64
        y = (1 - a) * 64 + a * self.pedal - 1
        return round(y)

    def onoff(self, msg, control):
        if msg.is_cc(control):
            if msg.value < 64:
                self.assigned = None
                self.control = None
            else:
                self.assigned = False

    def target(self, msg):
        if msg.type == "control_change":
            if msg.control not in self.ignored:
                if self.assigned is False:
                    self.assigned = True
                    self.control = msg.control
                    self.knob = msg.value
                    self.outport.send(
                        mido.Message(
                            "control_change",
                            control=self.control, value=self.out(), channel=self.channel
                        )
                    )
                    return True
                elif self.assigned is True:
                    if msg.is_cc(self.control):
                        self.knob = msg.value
                        self.outport.send(
                            mido.Message(
                                "control_change",
                                control=self.control,
                                value=self.out(),
                                channel=self.channel,
                            )
                        )
                        return True
        return None

    def source(self, msg, control):
        if msg.is_cc(control) and self.control is not None:
            self.pedal = msg.value
            self.outport.send(
                mido.Message(
                    "control_change",
                    control=self.control,
                    value=self.out(),
                    channel=self.channel,
                )
            )
