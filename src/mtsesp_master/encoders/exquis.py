"""
Encoders on Exquis.
"""

from midi_implementation.dualo import exquis as xq

default_color = xq.led("red")
alternative_color = xq.led("green")
click_color = xq.led("white")
unavailable_color = xq.led("black")


def color_coding(number):
    digits = [
        xq.led("black"),
        xq.led("magenta"),
        xq.led("blue"),
        xq.led("cyan"),
        xq.led("lime"),
        xq.led("yellow"),
        xq.led("red"),
        xq.led("white"),
    ]
    return [digits[number // 8], digits[number % 8]]


class Encoders:
    def __init__(
        self,
        outport,
        equave=0,
        equave_range=range(-2, 3),
        n_tunings=24,
        tuning_pgm=0,
        n_layouts=4,
        layout_pgm=0,
    ):
        self.outport = outport
        self.equave_range = equave_range
        self.init_equave = equave
        self.equave = equave
        self.n_tunings = n_tunings
        self.init_tuning_pgm = tuning_pgm
        self.tuning_pgm = tuning_pgm
        self.n_layouts = n_layouts
        self.init_layout_pgm = layout_pgm
        self.layout_pgm = layout_pgm

        self.is_left_right = False
        self.is_up_down = False
        self.default_color = default_color

    def reset(self):
        self.is_left_right = False
        self.is_up_down = False
        self.equave = self.init_equave

        self.recolor()

    def equave_color(self):
        if self.equave == self.init_equave:
            xq.send(
                self.outport,
                xq.sysex(xq.color_button, xq.octave_up, self.default_color),
            )
            xq.send(
                self.outport,
                xq.sysex(xq.color_button, xq.octave_down, self.default_color),
            )
        elif self.equave == max(self.equave_range):
            xq.send(
                self.outport, xq.sysex(xq.color_button, xq.octave_up, unavailable_color)
            )
            xq.send(
                self.outport,
                xq.sysex(xq.color_button, xq.octave_down, self.default_color),
            )
        elif self.equave == min(self.equave_range):
            xq.send(
                self.outport,
                xq.sysex(xq.color_button, xq.octave_up, self.default_color),
            )
            xq.send(
                self.outport,
                xq.sysex(xq.color_button, xq.octave_down, unavailable_color),
            )
        elif self.equave > self.init_equave:
            xq.send(self.outport, xq.sysex(xq.color_button, xq.octave_up, click_color))
            xq.send(
                self.outport,
                xq.sysex(xq.color_button, xq.octave_down, self.default_color),
            )
        else:
            xq.send(
                self.outport,
                xq.sysex(xq.color_button, xq.octave_up, self.default_color),
            )
            xq.send(
                self.outport, xq.sysex(xq.color_button, xq.octave_down, click_color)
            )

    def recolor(self):
        xq.send(
            self.outport,
            xq.sysex(
                xq.color_button,
                xq.page_right,
                click_color if self.is_left_right else self.default_color,
            ),
        )
        xq.send(
            self.outport,
            xq.sysex(
                xq.color_button,
                xq.page_left,
                click_color if self.is_up_down else self.default_color,
            ),
        )
        self.equave_color()
        code = color_coding(self.tuning_pgm)
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob1, code[0]))
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, code[1]))
        code = color_coding(self.layout_pgm)
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob3, code[0]))
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob4, code[1]))

    def refresh(self, msg):
        for menu_button in [
            xq.settings,
            xq.sounds,
            xq.record,
            xq.tracks,
            xq.scenes,
            xq.play_stop,
        ]:
            if xq.is_sysex(msg, [xq.click, menu_button, xq.released]):
                self.recolor()
                return True
        return None

    def change_equave(self, msg, equave):
        if xq.is_sysex(msg, [xq.click, xq.octave_up, xq.pressed]):
            self.equave = equave + 1 if equave + 1 in self.equave_range else equave
            self.equave_color()
            return self.equave
        elif xq.is_sysex(msg, [xq.click, xq.octave_down, xq.pressed]):
            self.equave = equave - 1 if equave - 1 in self.equave_range else equave
            self.equave_color()
            return self.equave
        return None

    def flip_left_right(self, msg):
        if xq.is_sysex(msg, [xq.click, xq.page_right, xq.pressed]):
            self.is_left_right = not self.is_left_right
            if self.is_left_right:
                xq.send(
                    self.outport, xq.sysex(xq.color_button, xq.page_right, click_color)
                )
            else:
                xq.send(
                    self.outport,
                    xq.sysex(xq.color_button, xq.page_right, self.default_color),
                )
            return self.is_left_right
        return None

    def flip_up_down(self, msg):
        if xq.is_sysex(msg, [xq.click, xq.page_left, xq.pressed]):
            self.is_up_down = not self.is_up_down
            if self.is_up_down:
                xq.send(
                    self.outport, xq.sysex(xq.color_button, xq.page_left, click_color)
                )
            else:
                xq.send(
                    self.outport,
                    xq.sysex(xq.color_button, xq.page_left, self.default_color),
                )
            return self.is_up_down
        return None

    def transpose(self, msg, transposition, transposition_range=range(0, 128)):
        if xq.is_sysex(msg, [xq.clockwise, xq.knob1, None]):
            transposition = (
                transposition + 1
                if transposition + 1 in transposition_range
                else transposition
            )
        elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, None]):
            transposition = (
                transposition - 1
                if transposition - 1 in transposition_range
                else transposition
            )
        else:
            return None
        return transposition

    def reset_keyswitches(self, msg):
        if xq.is_sysex(msg, [xq.click, xq.button1, xq.pressed]):
            return True
        return None

    def tuning_preset(self, msg, tuning_pgm):
        if xq.is_sysex(msg, [xq.clockwise, xq.knob2, None]):
            self.tuning_pgm = (
                tuning_pgm + 1 if tuning_pgm + 1 < self.n_tunings else tuning_pgm
            )
        elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob2, None]):
            self.tuning_pgm = tuning_pgm - 1 if tuning_pgm - 1 >= 0 else tuning_pgm
        else:
            return None
        code = color_coding(self.tuning_pgm)
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob1, code[0]))
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, code[1]))
        return self.tuning_pgm

    def differentiate_manuals(self, msg, different_manuals):
        if xq.is_sysex(msg, [xq.click, xq.button2, xq.pressed]):
            different_manuals = not different_manuals
            self.default_color = (
                alternative_color if different_manuals else default_color
            )
            self.recolor()
            return different_manuals
        return None

    def dilate(self, msg, dilation, dilation_range=range(1, 13)):
        if xq.is_sysex(msg, [xq.clockwise, xq.knob3, None]):
            dilation = dilation + 1 if dilation + 1 in dilation_range else dilation
        elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob3, None]):
            dilation = dilation - 1 if dilation - 1 in dilation_range else dilation
        else:
            return None
        return dilation

    def reset_dilation(self, msg, min3rd):
        if xq.is_sysex(msg, [xq.click, xq.button3, xq.pressed]):
            return min3rd
        return None

    def layout_preset(self, msg, layout_pgm):
        if xq.is_sysex(msg, [xq.clockwise, xq.knob4, None]):
            self.layout_pgm = (
                layout_pgm + 1 if layout_pgm + 1 < self.n_layouts else layout_pgm
            )
        elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob4, None]):
            self.layout_pgm = layout_pgm - 1 if layout_pgm - 1 >= 0 else layout_pgm
        else:
            return None
        code = color_coding(self.layout_pgm)
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob3, code[0]))
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob4, code[1]))
        return self.layout_pgm

    def split(self, msg, is_split):
        if xq.is_sysex(msg, [xq.click, xq.button4, xq.pressed]):
            is_split = not is_split
            return is_split
        return None
