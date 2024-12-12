import mido

from midi_implementation.midi1 import control_change as cc


class Assign:
    ignored = [
        cc.damper_pedal,
        cc.soft_pedal,
        cc.sostenuto,
        cc.legato_footswitch,
        cc.hold2,
        *cc.expression_controller,
        *cc.foot_controller,
        *cc.bank_select,
        cc.timbre,
        cc.data_increment,
        cc.data_decrement,
        *cc.rpn,
        *cc.nrpn,
        *cc.channel_mode_message,
    ]

    def __init__(self, outport, channel=0):
        self.outport = outport
        self.channel = channel
        self.assigned = None
        self.control = None
        self.d = 64

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
                    self.control = msg.control
                    self.d = msg.value
                    self.assigned = True
                    return True
                elif self.assigned is True:
                    if msg.is_cc(self.control):
                        self.d = msg.value
                        return True
        return None

    def source(self, msg, control):
        if msg.is_cc(control) and self.control_change is not None:
            coeff = (self.d - 64) / 64
            value = round((1 - coeff) * 64 + coeff * msg.value)
            self.outport.send(
                mido.Message(
                    "control_change",
                    control=self.control,
                    value=value,
                    channel=self.channel,
                )
            )
