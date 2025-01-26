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

synths = [5, 4, 3, 2, 1, 0, 10, 9, 8, 7, 6, 16, 15, 14, 13, 12, 11]

knobs = [xq.knob1, xq.knob2, xq.knob3, xq.knob4]


class Sounds:
    def __init__(
        self,
        outport,
        engine_banks_pgms,
        drivers=[],
        indicators=[lambda turn=0, click=0: 0] * 4,
        base_color="red",
        click_color="white",
    ):
        self.outport = outport
        self.engine_banks_pgms = engine_banks_pgms
        self.drivers = drivers
        self.indicators = indicators
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

        self.knob_turns = [1] * 4
        self.knob_clicks = [False] * 4

    def start(self):
        for key in xq.keys:
            xq.send(self.outport, xq.sysex(xq.map_key_to_note, key, key))
        for i, key in enumerate(engines):
            if i < self.n_engines:
                xq.send(
                    self.outport, xq.sysex(xq.color_key, key, xq.led(self.base_color))
                )
            else:
                break
        for key in range(i, 61 - len(synths)):
            xq.send(
                self.outport,
                xq.sysex(xq.color_key, mapping[key], xq.led("black")),
            )
        for i, key in enumerate(synths):
            if i < self.n_drivers:
                is_connected = self.drivers[i][1]()
                if is_connected:
                    xq.send(
                        self.outport,
                        xq.sysex(xq.color_key, key, xq.led(self.base_color)),
                    )
            else:
                xq.send(self.outport, xq.sysex(xq.color_key, key, xq.led("black")))

    def onoff(self, msg):
        if xq.is_sysex(msg, [xq.click, xq.sounds, xq.pressed]):
            self.start()
            for button in [xq.octave_up, xq.octave_down, xq.page_left, xq.page_right]:
                xq.send(
                    self.outport,
                    xq.sysex(xq.color_button, button, xq.led("black")),
                )

            for indicator, knob in zip(self.indicators, knobs):
                color = indicator()
                sysex = xq.sysex(xq.color_knob, knob, xq.led(color))
                xq.send(self.outport, sysex)

            self.n_banks = 0
            self.n_pgms = 0

            self.is_on = True
            self.submenu = 0

        elif xq.is_sysex(
            msg, [xq.click, xq.sounds, xq.released]
        ):  # implement longpress?
            self.is_on = None
            return False

        return self.is_on

    def knob(self, i, msg):
        assert i in range(1, 5)
        if xq.is_sysex(msg, [xq.clockwise, knobs[i - 1], None]):
            self.knob_turns[i - 1] = min(
                1, self.knob_turns[i - 1] + xq.rotation(msg) / 100
            )
        elif xq.is_sysex(msg, [xq.counter_clockwise, knobs[i - 1], None]):
            self.knob_turns[i - 1] = max(
                0, self.knob_turns[i - 1] + xq.rotation(msg) / 100
            )
        elif xq.is_sysex(msg, [xq.click, xq.to_button(knobs[i - 1]), xq.pressed]):
            self.knob_clicks[i - 1] = not self.knob_clicks[i-1]
        else:
            return self.knob_turns[i - 1], self.knob_clicks[i - 1]
        color = self.indicators[i - 1](
            turn=self.knob_turns[i - 1], click=self.knob_clicks[i - 1]
        )
        sysex = xq.sysex(xq.color_knob, knobs[i - 1], xq.led(color))
        xq.send(self.outport, sysex)
        return self.knob_turns[i - 1], self.knob_clicks[i - 1]

    def select(self, msg):
        if msg.type == "note_on":
            if msg.note in engines:
                i = engines.index(msg.note)
                if i < self.n_engines:
                    self.start()
                    xq.send(
                        self.outport,
                        xq.sysex(xq.color_key, msg.note, xq.led(self.click_color)),
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
                                    xq.sysex(
                                        xq.color_key, key, xq.led(self.base_color)
                                    ),
                                )
                            else:
                                break

            elif msg.note in synths and self.submenu <= 1:
                i = synths.index(msg.note)
                if i < self.n_drivers:
                    is_connected = self.drivers[i][1]()
                    if is_connected:
                        self.start()
                        xq.send(
                            self.outport,
                            xq.sysex(xq.color_key, msg.note, xq.led(self.click_color)),
                        )
                        self.engine = -i - 1
                        self.submenu = 0

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
                        self.outport,
                        xq.sysex(xq.color_key, msg.note, xq.led(self.click_color)),
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
                                    xq.sysex(
                                        xq.color_key, key, xq.led(self.base_color)
                                    ),
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
                        self.outport,
                        xq.sysex(xq.color_key, msg.note, xq.led(self.click_color)),
                    )
                    self.pgm = i

        return self.engine, self.bank, self.pgm
