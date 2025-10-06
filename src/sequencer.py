import mido
import numpy as np

n_notes = 128
n_channels = 16
per32 = 3


class StepSequencer:
    """
    Note that this step sequencer is intended for drum sounds
    and therefore does not transmit note off messages.
    If the time signature is x/y, then set the dividend to x and the divisor to y.
    """

    def __init__(self, dividend=4, divisor=4, display_length=6):
        self.divisor = divisor
        self.display_length = display_length
        self.counter = 0
        self.step = 0
        self.is_pressed = np.full(shape=(n_notes, n_channels), fill_value=0, dtype=int)
        self.velocity = np.full(
            shape=(n_notes, n_channels, dividend), fill_value=0, dtype=int
        )
        self.is_playing = False

    def time_signature(self, dividend=None, divisor=None):
        if dividend is not None:  # changing the dividend resets the recording
            self.step = 0
            self.is_pressed = np.full(
                shape=(n_notes, n_channels), fill_value=0, dtype=int
            )
            self.velocity = np.full(
                shape=(n_notes, n_channels, dividend), fill_value=0, dtype=int
            )
            self.is_playing = False
        if divisor is not None:
            self.divisor = divisor

    def record(self, msg):
        if hasattr(msg, "note") and not self.is_playing:
            if msg.type == "note_on" and msg.velocity > 0:
                self.is_pressed[msg.note, msg.channel] = 1
                erase = (
                    self.is_pressed.min() >= 0
                    and np.count_nonzero(self.is_pressed) == 1
                )
                if erase:  # instead of overdubbing, erase the previous data
                    self.velocity[:, :, self.step] = 0
                self.velocity[msg.note, msg.channel, self.step] = msg.velocity
            elif msg.type in ["note_on", "note_off"]:
                self.is_pressed[msg.note, msg.channel] = -1
            proceed = self.is_pressed.min() == -1 and self.is_pressed.max() <= 0
            if proceed:  # advance the step sequencer when all notes have been released
                self.is_pressed[:, :] = 0
                dividend = self.velocity.shape[2]
                self.step = (self.step + 1) % dividend

    def play(self, msg):
        notes_on = []
        if msg.type == "start":
            self.is_playing = True
            self.step = 0
        elif msg.type == "stop":
            self.is_playing = False
            self.step = 0
        if msg.type == "clock":
            if self.is_playing:
                ticks_per_beat = (32 // self.divisor) * per32
                on_beat = self.counter % ticks_per_beat == 0
                if on_beat:
                    step = self.counter // ticks_per_beat
                    step %= self.velocity.shape[2]  # return to beat 0 after one measure
                    notes, channels = self.velocity[:, :, step].nonzero()
                    for note, channel in zip(notes, channels):
                        note_on = mido.Message(
                            "note_on",
                            note=note,
                            channel=channel,
                            velocity=self.velocity[note, channel, step],
                        )
                        notes_on.append(note_on)
            self.counter += 1
        return notes_on

    def display(self):
        binary = np.zeros(shape=self.display_length, dtype=int)
        k = 0
        for i in range(
            self.display_length
        ):  # create a binary representation of the current position
            if self.divisor >= 32 / (2**i):
                j = self.display_length - 1 - i
                if self.is_playing:
                    binary[j] = (self.counter // ((2**i) * per32)) % 2
                else:
                    binary[j] = (self.step // (2**k)) % 2
                    k += 1
        return binary.tolist()
