import mido
import time

pause = 0.001


def set_mpe_mode(outport, polyphony=15, zone="lower"):
    manager = 15 if zone == "upper" else 0
    assert polyphony in range(0, 16)
    outport.send(mido.Message("control_change", control=101, value=0, channel=manager))
    time.sleep(pause)
    outport.send(mido.Message("control_change", control=100, value=6, channel=manager))
    time.sleep(pause)
    outport.send(
        mido.Message("control_change", control=6, value=polyphony, channel=manager)
    )


def set_pitchbend_sensitivity(
    outport, manager_sensitivity, member_sensitivity, polyphony=15, zone="lower"
):
    manager = 15 if zone == "upper" else 0
    members = range(14 - polyphony, 14) if zone == "upper" else range(1, polyphony + 1)
    msgs = []
    msgs.append(mido.Message("control_change", control=101, value=0, channel=manager))
    msgs.append(mido.Message("control_change", control=100, value=0, channel=manager))
    msgs.append(
        mido.Message(
            "control_change", control=0, value=manager_sensitivity, channel=manager
        )
    )
    msgs.append(
        mido.Message(
            "control_change", control=0, value=0, channel=manager
        )
    )
    for member in members:
        msgs.append(
            mido.Message("control_change", control=101, value=0, channel=member)
        )
        msgs.append(
            mido.Message("control_change", control=100, value=0, channel=member)
        )
        msgs.append(
            mido.Message(
                "control_change", control=0, value=member_sensitivity, channel=member
            )
        )
        msgs.append(
            mido.Message(
                "control_change", control=0, value=0, channel=member
            )
        )
    for msg in msgs:
        outport.send(msg)
        time.sleep(pause)


def is_polyexpression(msg):
    if not hasattr(msg, "channel"):
        return False
    if msg.type in ["note_on", "note_off", "aftertouch", "pitchwheel"]:
        return True
    if msg.is_cc(74):
        return True
    return False


class MPE:
    def __init__(
        self,
        outport,
        masters=[0],
        members=range(1, 16),
        zone="lower",
        polyphony=14,
    ):
        self.outport = outport
        assert all([i not in members for i in masters])
        self.masters = masters
        self.members = members
        self.polyphony = polyphony
        if zone == "lower":
            self.manager_channel = 0
            self.member_channels = range(1, polyphony + 1)
        else:
            raise Warning("upper zones not yet implemented")
        self.active = [False] * polyphony
        self.note_on = [0] * polyphony
        self.note_off = [False] * polyphony
        self.note = [-1] * polyphony
        self.mapping = [-1] * polyphony

    def dispatch(self, msg):
        if not hasattr(msg, "channel"):
            self.outport.send(msg)
        elif msg.channel in self.members:
            if msg.type == "note_on" and msg.velocity > 0:
                if all(self.active):
                    i = self.polyphony - 1
                    top = max(self.note)
                    bottom = min(self.note)
                    for j in range(self.polyphony):
                        if self.note[j] in [top, bottom]:
                            continue
                        elif self.note_on[j] < self.note_on[i]:
                            i = j
                    self.outport.send(
                        mido.Message("note_off", note=self.note[i], channel=i + 1)
                    )
                    self.mapping[i] = msg.channel
                    self.note[i] = msg.note
                    self.note_on[i] = time.perf_counter_ns()
                    self.outport.send(msg.copy(channel=i + 1))
                else:
                    i = self.active.index(False)
                    self.mapping[i] = msg.channel
                    self.note[i] = msg.note
                    self.note_on[i] = time.perf_counter_ns()
                    self.active[i] = True
                    self.outport.send(msg.copy(channel=i + 1))
            elif msg.type in ["note_on", "note_off"]:
                if (
                    msg.channel in self.mapping
                    and msg.note == self.note[self.mapping.index(msg.channel)]
                ):
                    i = self.mapping.index(msg.channel)
                    self.note_off[i] = True
                    self.active[i] = False
                    self.outport.send(msg.copy(channel=i + 1))
            elif msg.type == "polytouch":
                self.outport.send(msg.copy(channel=self.manager_channel))
            else:
                if msg.channel in self.mapping:
                    i = self.mapping.index(msg.channel)
                    self.outport.send(msg.copy(channel=i + 1))
        elif msg.channel in self.masters:
            self.outport.send(msg.copy(channel=self.manager_channel))
            if msg.is_cc(120):
                self.active = [False] * self.polyphony
