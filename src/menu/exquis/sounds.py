from colour import Color
from utils import get_volume, get_gain
from midi_implementation.dualo import exquis as xq
				
				
mapping = [
	55, 56, 57, 58, 59, 60,
	50, 51, 52, 53, 54,
	44, 45, 46, 47, 48, 49,
	39, 40, 41, 42, 43,
	33, 34, 35, 36, 37, 38,
	28, 29, 30, 31, 32,
	22, 23, 24, 25, 26, 27,
	17, 18, 19, 20, 21,
	11, 12, 13, 14, 15, 16,
   	6, 7, 8, 9, 10,
    0, 1, 2, 3, 4, 5,
]

engines = [55, 56, 57, 58, 59, 60, 50, 51, 52, 53, 54, 44, 45, 46, 47, 48, 49]
banks = [33, 34, 35, 36, 37, 38, 28, 29, 30, 31, 32, 22, 23, 24, 25, 26, 27]
pgms = [11, 12, 13, 14, 15, 16, 6, 7, 8, 9, 10, 0, 1, 2, 3, 4, 5]

class Sounds:
    def __init__(
        self,
        outport,
        engine_banks_pgms,
        drivers,
        base_color="red",
        click_color="white",
    ):
        self.outport = outport
        self.engine_banks_pgms = engine_banks_pgms
        self.drivers = drivers
        self.base_color = base_color
        self.click_color = click_color
        self.engine = 0
        self.bank = 0
        self.pgm = 0

        self.n_engines = len(self.engine_banks_pgms)
        self.n_banks = 0
        self.n_pgms = 0
        self.n_drivers = len(self.drivers)

        self.is_on = None
        self.submenu = 0

        self.volume = 1
        self.volume_is_muted = False
        self.gain = 1
        self.gain_is_muted = False

    def onoff(self, msg):
        if xq.is_sysex(msg, [xq.click, xq.sounds, xq.pressed]):
            for key in xq.keys:
                xq.send(self.outport, xq.sysex(xq.map_key_to_note, key, key))
            for i, key in enumerate(engines):
                if i < self.n_engines:
                    xq.send(self.outport, xq.sysex(xq.color_key, key, xq.led(self.base_color)))
                else:
                    break
            for key in range(i, 61):
                xq.send(
                    self.outport,
                    xq.sysex(xq.color_key, mapping[key], xq.led("black")),
                )
            for button in [xq.octave_up, xq.octave_down, xq.page_left, xq.page_right]:
                xq.send(
                    self.outport,
                    xq.sysex(xq.color_button, button, xq.led("black")),
                )

            self.volume, self.volume_is_muted = get_volume()
            volume_indicator = Color(self.base_color)
            volume_indicator.luminance = 0 if self.volume_is_muted else self.volume
            xq.send(
                self.outport, xq.sysex(xq.color_knob, xq.knob1, xq.led(volume_indicator))
            )
            self.gain, self.gain_is_muted = get_gain()
            gain_indicator = Color(self.base_color)
            gain_indicator.luminance = 0 if self.gain_is_muted else self.gain
            xq.send(
                self.outport, xq.sysex(xq.color_knob, xq.knob2, xq.led(gain_indicator))
            )
            xq.send(
                self.outport, xq.sysex(xq.color_knob, xq.knob3, xq.led("black"))
            )
            xq.send(
                self.outport, xq.sysex(xq.color_knob, xq.knob4, xq.led("black"))
            )

            self.n_banks = 0
            self.n_pgms = 0

            self.is_on = True
            self.submenu = 0

        elif xq.is_sysex(msg, [xq.click, xq.sounds, xq.released]):
            self.is_on = None
            return False

        return self.is_on

    def set_volume(self, msg):
        if xq.is_sysex(msg, [xq.clockwise, xq.knob1, None]):
            self.volume = min(1, self.volume + xq.rotation(msg) / 100)
        elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob1, None]):
            self.volume = max(0, self.volume + xq.rotation(msg) / 100)
        elif xq.is_sysex(msg, [xq.click, xq.button1, xq.pressed]):
            self.volume_is_muted = not self.volume_is_muted
        else:
            return False
        volume_indicator = Color(self.base_color)
        volume_indicator.luminance = 0 if self.volume_is_muted else self.volume
        xq.send(
            self.outport, xq.sysex(xq.color_knob, xq.knob1, xq.led(volume_indicator))
        )
        return True

    def set_gain(self, msg):
        if xq.is_sysex(msg, [xq.clockwise, xq.knob2, None]):
            self.gain = min(1, self.gain + xq.rotation(msg) / 100)
        elif xq.is_sysex(msg, [xq.counter_clockwise, xq.knob2, None]):
            self.gain = max(0, self.gain + xq.rotation(msg) / 100)
        elif xq.is_sysex(msg, [xq.click, xq.button2, xq.pressed]):
            self.gain_is_muted = not self.gain_is_muted
        else:
            return False
        gain_indicator = Color(self.base_color)
        gain_indicator.luminance = 0 if self.gain_is_muted else self.gain
        xq.send(self.outport, xq.sysex(xq.color_knob, xq.knob2, xq.led(gain_indicator)))
        return True

    def select(self, msg):
        if msg.type == "note_on":
            if msg.note in engines:
                i = engines.index(msg.note)
                if i < self.n_engines:
                    for j, key in enumerate(engines):
                        if j < self.n_engines:
                            xq.send(
                                self.outport,
                                xq.sysex(xq.color_key, key, xq.led(self.base_color)),
                            )
                        else:
                            break
                    for key in range(j, 61):
                        xq.send(
                            self.outport,
                            xq.sysex(xq.color_key, mapping[key], xq.led("black")),
                        )
                    xq.send(
                        self.outport, xq.sysex(xq.color_key, msg.note, xq.led(self.click_color))
                    )
                    self.engine = i
                    self.n_banks = len(self.engine_banks_pgms[self.engine][1])
                    self.n_pgms = 0
                    self.submenu = 1
                    if self.n_banks > 1:
                        for j, key in enumerate(banks):
                            if j < self.n_banks:
                                xq.send(
                                    self.outport,
                                    xq.sysex(xq.color_key, key, xq.led(self.base_color)),
                                )
                            else:
                                break

            elif msg.note in banks and self.n_banks > 1 and self.submenu > 0:
                i = banks.index(msg.note)
                if i < self.n_banks:
                    for j, key in enumerate(banks):
                        if j < self.n_banks:
                            xq.send(
                                self.outport,
                                xq.sysex(xq.color_key, key, xq.led(self.base_color)),
                            )
                        else:
                            xq.send(
                                self.outport,
                                xq.sysex(xq.color_key, key, xq.led("black")),
                            )
                    for key in pgms:
                        xq.send(
                            self.outport,
                            xq.sysex(xq.color_key, key, xq.led("black")),
                        )
                    xq.send(
                        self.outport, xq.sysex(xq.color_key, msg.note, xq.led(self.click_color))
                    )
                    self.bank = i
                    self.n_pgms = round(
                        self.engine_banks_pgms[self.engine][1][self.bank]
                    )
                    self.submenu = 2
                    if self.n_pgms > 1:
                        for j, key in enumerate(pgms):
                            if j < self.n_pgms:
                                xq.send(
                                    self.outport,
                                    xq.sysex(xq.color_key, key, xq.led(self.base_color)),
                                )
                            else:
                                break

            elif msg.note in pgms and self.n_pgms > 1 and self.submenu > 1:
                i = pgms.index(msg.note)
                if i <= self.engine_banks_pgms[self.engine][1][self.bank]:
                    for j, key in enumerate(pgms):
                        if j < self.n_pgms:
                            xq.send(
                                self.outport,
                                xq.sysex(xq.color_key, key, xq.led(self.base_color)),
                            )
                        else:
                            xq.send(
                                self.outport,
                                xq.sysex(xq.color_key, key, xq.led("black")),
                            )
                    xq.send(
                        self.outport, xq.sysex(xq.color_key, msg.note, xq.led(self.click_color))
                    )
                    self.pgm = i

        return self.engine, self.bank, self.pgm
