import mido
import time
from midi_implementation.midi1 import control_change as cc


class Damper:
    def __init__(self, outport, memory=128):
        self.outport = outport
        self.memory = memory

        self.note_on = [[0] * 16] * 128
        self.note = [-1] * self.memory
        self.channel = [-1] * self.memory
        self.is_on = False

    def hold(self, msg):
        if msg.type in ["note_on", "note_off"]:
            if msg.type == "note_on" and msg.velocity > 0:
                self.note_on[msg.note][msg.channel] = time.perf_counter_ns()
            elif self.is_on:
                if -1 not in self.note:
                    i = self.memory - 1
                    top = max(self.note)
                    bottom = min(self.note)
                    for j in range(self.memory):
                        if self.note[j] in [top, bottom]:
                            continue
                        elif self.note_on[j][msg.channel] < self.note_on[i]:
                            i = j
                    self.outport.send(
                        mido.Message(
                            "note_off", note=self.note[i], channel=self.channel[i]
                        )
                    )
                    self.note[i] = msg.note
                    self.channel[i] = msg.note
                else:
                    i = self.note.index(-1)
                    self.note[i] = msg.note
                    self.channel[i] = msg.channel
                return True
            elif msg.note in self.note:
                i = self.note.index(msg.note)
                if self.channel[i] == msg.channel:
                    self.note[i] = -1
                    self.channel[i] = -1
            return None

    def onoff(self, msg, control=cc.damper_pedal):
        if msg.is_cc(control):
            if msg.value >= 64 and not self.is_on:
                self.is_on = True
            elif msg.value < 64 and self.is_on:
                for i in range(self.memory):
                    self.outport.send(
                        mido.Message(
                            "note_off", note=self.note[i], channel=self.channel[i]
                        )
                    )
                    self.note[i] = -1
                    self.channel[i] = -1
                self.is_on = False


class Sostenuto:
    def __init__(self, outport, channel, memory=128):
        self.outport = outport
        self.channel = channel
        self.memory = memory

    def hold(self, msg):
        ...
        return None

    def onoff(self, msg, control=cc.sostenuto):
        if msg.is_cc(control):
            if msg.value >= 64 and not self.is_on:
                self.is_on = True
                ...
            elif msg.value < 64 and self.is_on:
                ...
                self.is_on = False
