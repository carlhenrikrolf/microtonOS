# external libraries
import mido
import numpy as np
import time

# internal libraries
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq
from midi_implementation.midi1 import control_change as cc, realtime as rt
from utils import (
    Inport,
    Outport,
    make_threads,
    load_config,
    set_gain4all,
    set_volume4all,
)

config = {
    "microtonOS": load_config(__file__, "../config/microtonOS.toml"),
    "control_change": load_config(__file__, "../config/control_change.toml"),
}

black = np.array(config["microtonOS"]["palette"]["black"])
white = np.array(config["microtonOS"]["palette"]["white"])
blue = np.array(config["microtonOS"]["palette"]["blue"])
magenta = np.array(config["microtonOS"]["palette"]["magenta"])
red = np.array(config["microtonOS"]["palette"]["red"])
yellow = np.array(config["microtonOS"]["palette"]["yellow"])
green = np.array(config["microtonOS"]["palette"]["green"])
cyan = np.array(config["microtonOS"]["palette"]["cyan"])


def microtonOS(Display):
    client_name = "microtonOS"
    display = Display()

    def show_cc(msg):
        if msg.type == "control_change":
            control = str(msg.control)
            transmitted = config["control_change"]["channel"][msg.channel][
                "transmitted"
            ]
            if control in transmitted:
                Pianoteq = config["control_change"]["channel"][msg.channel][
                    "transmitted"
                ][control]["Pianoteq"]
                display.show(
                    Pianoteq,
                    msg.value,
                )

    class StartPage:
        def __init__(self):
            self.mic = {"muted": False, "gain": 1.0}
            self.midi = {"thru": False, "volume": 1.0}
            self.lower = {"local": True, "filter": "PC"}
            self.upper = {"local": True, "filter": "PC"}
            set_gain4all(level=1.0, muted=False)
            set_volume4all(level=1.0, muted=False)

        def mic_led(self):
            if self.mic["gain"] > 0.5:
                color = white * self.mic["gain"] + green * (1 - self.mic["gain"])
                color -= 0.5
                color *= 2
            else:
                color = green * self.mic["gain"]
                color *= 2
            fx = xq.pulse2red if self.mic["muted"] else xq.no_fx
            return color, fx

        def midi_led(self):
            if self.midi["volume"] > 0.5:
                color = white * self.midi["volume"] + green * (1 - self.midi["volume"])
                color -= 0.5
                color *= 2
            else:
                color = green * self.midi["volume"]
                color *= 2
            fx = xq.pulse2red if self.midi["thru"] else xq.no_fx
            return color, fx

        def lower_led(self):
            color = (
                white
                if self.lower["filter"] == "PC"
                else green
                if self.lower["filter"] == "CC+PC"
                else black
            )
            fx = xq.pulse2red if not self.lower["local"] else xq.no_fx
            return color, fx

        def upper_led(self):
            color = (
                white
                if self.upper["filter"] == "PC"
                else green
                if self.upper["filter"] == "CC+PC"
                else black
            )
            fx = xq.pulse2red if not self.upper["local"] else xq.no_fx
            return color, fx

        def update(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                colors = [black] * 128
                fx = [xq.no_fx] * 128
                pad_colors = [colors[i] for i in xq.pad]
                pad_leds = xq.set_led_colors(pad_colors, start_index=xq.pad[0])
                to_exquis.send(pad_leds)
                (colors[xq.encoder_led[0]], fx[xq.encoder_led[0]]) = self.mic_led()
                (colors[xq.encoder_led[1]], fx[xq.encoder_led[1]]) = self.midi_led()
                (colors[xq.encoder_led[2]], fx[xq.encoder_led[2]]) = self.lower_led()
                (colors[xq.encoder_led[3]], fx[xq.encoder_led[3]]) = self.upper_led()
                misc_colors = [colors[i] for i in xq.arrow_or_encoder]
                misc_fx = [fx[i] for i in xq.arrow_or_encoder]
                misc_leds = xq.set_led_colors(
                    misc_colors, fx=misc_fx, start_index=xq.arrow_or_encoder[0]
                )
                to_exquis.send(misc_leds)
                display.show("")
            elif xq.is_pressed(msg, xq.encoder_button[0]):
                self.mic["muted"] = not self.mic["muted"]
                set_gain4all(muted=self.mic["muted"])
                color, fx = self.mic_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[0]
                )
                to_exquis.send(led_colors)
                display.show("mic", value="on" if not self.mic["muted"] else "off")
            elif xq.is_turned(msg, xq.encoder_knob[0]):
                change = xq.is_turned(msg, xq.encoder_knob[0])
                self.mic["gain"] += change / 3.0
                self.mic["gain"] = 1.0 if self.mic["gain"] > 1.0 else self.mic["gain"]
                self.mic["gain"] = 0.0 if self.mic["gain"] < 0.0 else self.mic["gain"]
                set_gain4all(level=self.mic["gain"], muted=self.mic["muted"])
                color, fx = self.mic_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[0]
                )
                to_exquis.send(led_colors)
                text = str(round(self.mic["gain"] * 100)) + "%"
                display.show("gain", value=text)
            elif xq.is_pressed(msg, xq.encoder_button[1]):
                self.midi["thru"] = not self.midi["thru"]
                color, fx = self.midi_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[1]
                )
                to_exquis.send(led_colors)
                display.show("MIDI", value="thru" if self.midi["thru"] else "in")
            elif xq.is_turned(msg, xq.encoder_knob[1]):
                change = xq.is_turned(msg, xq.encoder_knob[1])
                self.midi["volume"] += change / 3.0
                self.midi["volume"] = (
                    1.0 if self.midi["volume"] > 1.0 else self.midi["volume"]
                )
                self.midi["volume"] = (
                    0.0 if self.midi["volume"] < 0.0 else self.midi["volume"]
                )
                set_volume4all(level=self.midi["volume"], muted=False)
                color, fx = self.midi_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[1]
                )
                to_exquis.send(led_colors)
                text = str(round(self.midi["volume"] * 100)) + "%"
                display.show("volume", value=text)
            elif xq.is_pressed(msg, xq.encoder_button[2]):
                self.lower["local"] = not self.lower["local"]
                value = 127 if self.lower["local"] else 0
                local_control = mido.Message(
                    "control_change", control=cc.local_onoff_switch, value=value
                )
                to_lower.send(local_control)
                color, fx = self.lower_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[2]
                )
                to_exquis.send(led_colors)
                display.show(
                    "lower control", value="local" if self.lower["local"] else "remote"
                )
            elif xq.is_turned(msg, xq.encoder_knob[2]):
                change = xq.is_turned(msg, xq.encoder_knob[2])
                if change > 0:
                    if self.lower["filter"] == "PC":
                        self.lower["filter"] = "CC+PC"
                    elif self.lower["filter"] == "CC+PC":
                        self.lower["filter"] = "MIDI"
                    else:
                        self.lower["filter"] = "PC"
                elif change < 0:
                    if self.lower["filter"] == "PC":
                        self.lower["filter"] = "MIDI"
                    elif self.lower["filter"] == "CC+PC":
                        self.lower["filter"] = "PC"
                    else:
                        self.lower["filter"] = "CC+PC"
                color, fx = self.lower_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[2]
                )
                to_exquis.send(led_colors)
                display.show("lower filter", value=self.lower["filter"])
            elif xq.is_pressed(msg, xq.encoder_button[3]):
                self.upper["local"] = not self.upper["local"]
                value = 127 if self.upper["local"] else 0
                local_control = mido.Message(
                    "control_change", control=cc.local_onoff_switch, value=value
                )
                to_upper.send(local_control)
                color, fx = self.upper_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[3]
                )
                to_exquis.send(led_colors)
                display.show(
                    "upper control", value="local" if self.upper["local"] else "remote"
                )
            elif xq.is_turned(msg, xq.encoder_knob[3]):
                change = xq.is_turned(msg, xq.encoder_knob[3])
                if change > 0:
                    if self.upper["filter"] == "PC":
                        self.upper["filter"] = "CC+PC"
                    elif self.upper["filter"] == "CC+PC":
                        self.upper["filter"] = "MIDI"
                    else:
                        self.upper["filter"] = "PC"
                elif change < 0:
                    if self.upper["filter"] == "PC":
                        self.upper["filter"] = "MIDI"
                    elif self.upper["filter"] == "CC+PC":
                        self.upper["filter"] = "PC"
                    else:
                        self.upper["filter"] = "CC+PC"
                color, fx = self.upper_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[3]
                )
                to_exquis.send(led_colors)
                display.show("upper filter", value=self.upper["filter"])

    class InstrumentPage:
        def __init__(self):
            self.bank = 0
            self.prev_bank = 0
            self.pgm = 0
            self.prev_pgm = 0
            n_banks = len(config["microtonOS"]["engine"][0]["bank"])
            n_banks = 11 if n_banks > 11 else n_banks
            self.bank_leds = range(0, n_banks)
            n_pgms = len(
                config["microtonOS"]["engine"][0]["bank"][self.bank]["program"]
            )
            n_pgms = 11 if n_pgms > 11 else n_pgms
            self.pgm_leds = range(22, 22 + n_pgms)

        def update(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                colors = [black] * 128
                for bank, led in enumerate(self.bank_leds):
                    colors[led] = white if bank == self.bank else magenta
                for pgm, led in enumerate(self.pgm_leds):
                    colors[led] = white if pgm == self.pgm else magenta
                pad_colors = [colors[i] for i in xq.pad]
                pad_leds = xq.set_led_colors(pad_colors, start_index=xq.pad[0])
                to_exquis.send(pad_leds)
                misc_colors = [colors[i] for i in xq.arrow_or_encoder]
                misc_leds = xq.set_led_colors(
                    misc_colors, start_index=xq.arrow_or_encoder[0]
                )
                to_exquis.send(misc_leds)
                pgm_name = config["microtonOS"]["engine"][0]["bank"][self.bank][
                    "program"
                ][self.pgm]
                display.show(pgm_name)
            elif msg.type == "note_on" and msg.velocity > 0 and msg.channel == 15:
                if msg.note in self.bank_leds:
                    self.bank = msg.note
                    n_pgms = len(
                        config["microtonOS"]["engine"][0]["bank"][self.bank]["program"]
                    )
                    self.pgm_leds = range(22, 22 + n_pgms)
                    self.pgm = -1
                    script.page.update()
                    bank_name = config["microtonOS"]["engine"][0]["bank"][self.bank][
                        "name"
                    ]
                    display.show(bank_name)
                elif msg.note in self.pgm_leds:
                    self.pgm = msg.note - 22
                    self.prev_bank = self.bank
                    self.prev_pgm = self.pgm
                    script.page.update()
                    pgm_name = config["microtonOS"]["engine"][0]["bank"][self.bank][
                        "program"
                    ][self.pgm]
                    display.show(pgm_name)
                    pc = [
                        mido.Message(
                            "control_change", control=cc.bank_select[0], value=self.bank
                        ),
                        mido.Message(
                            "control_change", control=cc.bank_select[1], value=0
                        ),
                        mido.Message("program_change", program=self.pgm),
                    ]
                    for out in pc:
                        to_internal.send(out)

            elif xq.is_pressed(msg, xq.sound):
                self.bank = self.prev_bank
                self.pgm = self.prev_pgm
                n_pgms = len(
                    config["microtonOS"]["engine"][0]["bank"][self.bank]["program"]
                )
                self.pgm_leds = range(22, 22 + n_pgms)

    class RhythmPage:
        def update(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                colors = [black] * 128
                pad_colors = [colors[i] for i in xq.pad]
                pad_leds = xq.set_led_colors(pad_colors, start_index=xq.pad[0])
                to_exquis.send(pad_leds)
                misc_colors = [colors[i] for i in xq.arrow_or_encoder]
                misc_leds = xq.set_led_colors(
                    misc_colors, start_index=xq.arrow_or_encoder[0]
                )
                to_exquis.send(misc_leds)
                display.show("")
            elif xq.is_pressed(msg, xq.record):
                pass

    class IsomorphicPage:
        def update(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                colors = [black] * 128
                pad_colors = [colors[i] for i in xq.pad]
                pad_leds = xq.set_led_colors(pad_colors, start_index=xq.pad[0])
                to_exquis.send(pad_leds)
                misc_colors = [colors[i] for i in xq.arrow_or_encoder]
                misc_leds = xq.set_led_colors(
                    misc_colors, start_index=xq.arrow_or_encoder[0]
                )
                to_exquis.send(misc_leds)
                display.show("")
            elif xq.is_pressed(msg, xq.loop):
                pass

    class TuningPage:
        def update(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                colors = [black] * 128
                pad_colors = [colors[i] for i in xq.pad]
                pad_leds = xq.set_led_colors(pad_colors, start_index=xq.pad[0])
                to_exquis.send(pad_leds)
                misc_colors = [colors[i] for i in xq.arrow_or_encoder]
                misc_leds = xq.set_led_colors(
                    misc_colors, start_index=xq.arrow_or_encoder[0]
                )
                to_exquis.send(misc_leds)
                display.show("")
            elif xq.is_pressed(msg, xq.clips):
                pass

    class Shift:
        def __init__(self):
            self.is_on = False
            self.is_locked = False

        def update(self, msg=None):
            if msg is None:
                color = [white] if self.is_on else [black]
                led_color = xq.set_led_colors(color, start_index=xq.settings)
                to_exquis.send(led_color)
            elif xq.is_pressed(msg, xq.settings):
                if self.is_locked:
                    self.is_locked = False
                    self.is_on = False
                    led_color = xq.set_led_colors([black], start_index=xq.settings)
                    to_exquis.send(led_color)
                else:
                    self.is_on = True
                    led_color = xq.set_led_colors([blue], start_index=xq.settings)
                    to_exquis.send(led_color)
                    display.show("shift")
            elif xq.is_released(msg, xq.settings):
                if self.is_on:
                    self.is_locked = True
                    led_color = xq.set_led_colors([blue], start_index=xq.settings)
                    to_exquis.send(led_color)
            else:
                if self.is_on and not self.is_locked:
                    self.is_on = False
                    led_color = xq.set_led_colors([black], start_index=xq.settings)
                    to_exquis.send(led_color)

    class Play:
        def __init__(self):
            self.is_on = False
            self.to_all = False
            self.counter = 0

        def update(self, msg=None):
            if msg is None:
                color = [cyan] if self.is_on or self.to_all else [black]
                led_color = xq.set_led_colors(color, start_index=xq.play)
                to_exquis.send(led_color)
            if xq.is_pressed(msg, xq.play):
                if self.to_all:
                    self.to_all = False
                    self.is_on = False
                    stop = mido.Message("stop")
                    to_lower.send(stop)
                    to_upper.send(stop)
                    to_clock.send(stop)
                    led_color = xq.set_led_colors([black], start_index=xq.play)
                    to_exquis.send(led_color)
                    display.show("all stop")
                elif self.is_on:
                    self.is_on = False
                    stop = mido.Message("stop")
                    to_clock.send(stop)
                    led_color = xq.set_led_colors([black], start_index=xq.play)
                    to_exquis.send(led_color)
                    display.show("stop")
                elif not shift.is_on:
                    self.is_on = True
                    self.counter = 0
                    start = mido.Message("start")
                    to_clock.send(start)
                    led_color = xq.set_led_colors([cyan], start_index=xq.play)
                    to_exquis.send(led_color)
                    subtext = (
                        "" if script.bpm is None else "BPM " + str(round(script.bpm))
                    )
                    display.show("play", subtext)
                elif shift.is_on:
                    self.to_all = True
                    self.counter = 0
                    start = mido.Message("start")
                    to_lower.send(start)
                    to_upper.send(start)
                    to_clock.send(start)
                    led_color = xq.set_led_colors([1 - cyan], start_index=xq.play)
                    to_exquis.send(led_color)
                    subtext = (
                        "" if script.bpm is None else "BPM " + str(round(script.bpm))
                    )
                    display.show("all play", subtext)

        def tick(self, msg=None):
            per32 = 3
            if msg is None or msg.type == "clock":
                if self.is_on or self.to_all:
                    indicator = [
                        (self.counter // (32 * per32)) % 2,
                        (self.counter // (16 * per32)) % 2,
                        (self.counter // (8 * per32)) % 2,
                        (self.counter // (4 * per32)) % 2,
                        (self.counter // (2 * per32)) % 2,
                        (self.counter // per32) % 2,
                    ]
                    slider_colors = [white if indicator[i] else black for i in range(6)]
                    self.counter += 1
                else:
                    slider_colors = [black] * len(xq.slider)
                slider_leds = xq.set_led_colors(slider_colors, start_index=xq.slider[0])
                to_exquis.send(slider_leds)

    class ActiveSensing:
        ack_rate = 0.3  # seconds

        def __init__(self):
            self.ack = 0.0

        def run(self):
            while True:
                now = time.time()
                diff = now - self.ack
                ack = xq.get_tempo()
                to_exquis.send(ack)
                if diff > 2 * self.ack_rate:
                    script.page.update()
                time.sleep(self.ack_rate)

    class Script:
        def __init__(self):
            self.page = start_page
            self.bpm = None
            self.is_menu = [False] * 4

        def exquis(self, msg):
            active_sensing.ack = time.time()
            shift.update(msg)
            play.update(msg)
            if xq.is_pressed(msg, xq.sound):
                self.is_menu = [not self.is_menu[0], False, False, False]
                self.page = instrument_page if self.is_menu[0] else start_page
                self.page.update()
            elif xq.is_pressed(msg, xq.record):
                self.is_menu = [False, not self.is_menu[1], False, False]
                self.page = rhythm_page if self.is_menu[1] else start_page
                self.page.update()
            elif xq.is_pressed(msg, xq.loop):
                self.is_menu = [False, False, not self.is_menu[2], False]
                self.page = isomorphic_page if self.is_menu[2] else start_page
                self.page.update()
            elif xq.is_pressed(msg, xq.clips):
                self.is_menu = [False, False, False, not self.is_menu[3]]
                self.page = tuning_page if self.is_menu[3] else start_page
                self.page.update()
            else:
                self.page.update(msg)
            if any([xq.is_pressed(msg, button) for button in xq.menu]):
                all_sound_off()
            menu_colors = [
                magenta if self.is_menu[0] else black,
                red if self.is_menu[1] else black,
                yellow if self.is_menu[2] else black,
                green if self.is_menu[3] else black,
            ]
            menu_leds = xq.set_led_colors(menu_colors, start_index=xq.sound)
            to_exquis.send(menu_leds)
            # tempo = xq.get_tempo(msg)
            # if tempo is None:
            #     print(msg)

        def master(self, msg):
            to_internal.send(msg)
            show_cc(msg)
            if msg.type != "program_change":
                if start_page.lower["filter"] == "PC":
                    to_lower.send(msg)
                elif start_page.lower["filter"] == "CC+PC":
                    if msg.type != "control_change":
                        to_lower.send(msg)
                if start_page.upper["filter"] == "PC":
                    to_upper.send(msg)
                elif start_page.upper["filter"] == "CC+PC":
                    if msg.type != "control_change":
                        to_upper.send(msg)

        def lower(self, msg):
            if not start_page.lower["local"]:
                to_lower.send(msg)
            if start_page.lower["filter"] == "PC":
                if msg.type != "program_change":
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.upper["filter"] == "PC":
                        to_upper.send(msg)
                    elif start_page.upper["filter"] == "CC+PC":
                        if msg.type != "control_change":
                            to_upper.send(msg)
            elif start_page.lower["filter"] == "CC+PC":
                if msg.type not in ["program_change", "control_change"]:
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.upper["filter"] in ["PC", "CC+PC"]:
                        to_upper.send(msg)

        def upper(self, msg):
            if not start_page.upper["local"]:
                to_upper.send(msg)
            if start_page.upper["filter"] == "PC":
                if msg.type != "program_change":
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.lower["filter"] == "PC":
                        to_lower.send(msg)
                    elif start_page.lower["filter"] == "CC+PC":
                        if msg.type != "control_change":
                            to_lower.send(msg)
            elif start_page.upper["filter"] == "CC+PC":
                if msg.type not in ["program_change", "control_change"]:
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.lower["filter"] in ["PC", "CC+PC"]:
                        to_lower.send(msg)

        def clock(self, msg):
            to_clock.send(msg)
            play.tick(msg)
            bpm = rt.bpm(msg)
            if bpm is not None:
                self.bpm = bpm
                out = xq.set_tempo(self.bpm)
                to_exquis.send(out)

    to_exquis = Outport(client_name, name="Exquis")
    to_internal = Outport(client_name, name="Internal")
    to_lower = Outport(client_name, name="Lower")
    to_upper = Outport(client_name, name="Upper")
    to_clock = Outport(client_name, name="Clock")

    def all_sound_off():
        msg = mido.Message("control_change", control=cc.all_sound_off)
        to_internal.send(msg)
        to_lower.send(msg)
        to_upper.send(msg)

    start_page = StartPage()
    instrument_page = InstrumentPage()
    rhythm_page = RhythmPage()
    isomorphic_page = IsomorphicPage()
    tuning_page = TuningPage()
    shift = Shift()
    play = Play()
    active_sensing = ActiveSensing()
    script = Script()

    from_exquis = Inport(script.exquis, client_name, name="Exquis")
    from_master = Inport(script.master, client_name, name="Master")
    from_upper = Inport(script.upper, client_name, name="Upper")
    from_lower = Inport(script.lower, client_name, name="Lower")
    from_clock = Inport(script.clock, client_name, name="Clock")

    make_threads(
        [
            from_exquis.open,
            from_master.open,
            from_upper.open,
            from_lower.open,
            from_clock.open,
            active_sensing.run,
            display.run,
        ]
    )
