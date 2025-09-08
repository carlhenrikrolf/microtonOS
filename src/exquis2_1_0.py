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
red = np.array(config["microtonOS"]["palette"]["red"])
yellow = np.array(config["microtonOS"]["palette"]["yellow"])
green = np.array(config["microtonOS"]["palette"]["green"])
cyan = np.array(config["microtonOS"]["palette"]["cyan"])
magenta = np.array(config["microtonOS"]["palette"]["magenta"])


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
            self.lower = {"local": True, "filter": "pc"}
            self.upper = {"local": True, "filter": "pc"}
            set_gain4all(level=1.0, muted=False)
            set_volume4all(level=1.0, muted=False)

        def mic_led(self):
            color = (
                white * 2 * (self.mic["gain"] - 0.5)
                + green * (1.5 - 2 * (self.mic["gain"]))
                if self.mic["gain"] >= 0.5
                else green * 2 * self.mic["gain"]
            )
            fx = xq.pulse2red if self.mic["muted"] else xq.no_fx
            return color, fx

        def midi_led(self):
            color = (
                white * 2 * (self.midi["volume"] - 0.5)
                + green * (1.5 - 2 * self.midi["volume"])
                if self.midi["volume"] >= 0.5
                else green * 2 * self.midi["volume"]
            )
            fx = xq.pulse2red if self.midi["thru"] else xq.no_fx
            return color, fx

        def lower_led(self):
            color = (
                white
                if self.lower["filter"] == "pc"
                else green
                if self.lower["filter"] == "cc+pc"
                else black
            )
            fx = xq.pulse2red if not self.lower["local"] else xq.no_fx
            return color, fx

        def upper_led(self):
            color = (
                white
                if self.upper["filter"] == "pc"
                else green
                if self.upper["filter"] == "cc+pc"
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
                (colors[xq.encoder_knob[0]], fx[xq.encoder_knob[0]]) = self.mic_led()
                (colors[xq.encoder_knob[1]], fx[xq.encoder_knob[1]]) = self.midi_led()
                (colors[xq.encoder_knob[2]], fx[xq.encoder_knob[2]]) = self.lower_led()
                (colors[xq.encoder_knob[3]], fx[xq.encoder_knob[3]]) = self.upper_led()
                led_colors = xq.set_led_colors(colors, fx=fx)
                to_exquis.send(led_colors)
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
                    if self.lower["filter"] == "pc":
                        self.lower["filter"] = "cc+pc"
                    elif self.lower["filter"] == "cc+pc":
                        self.lower["filter"] = "MIDI"
                    else:
                        self.lower["filter"] = "pc"
                elif change < 0:
                    if self.lower["filter"] == "pc":
                        self.lower["filter"] = "MIDI"
                    elif self.lower["filter"] == "cc+pc":
                        self.lower["filter"] = "pc"
                    else:
                        self.lower["filter"] = "cc+pc"
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
                    if self.upper["filter"] == "pc":
                        self.upper["filter"] = "cc+pc"
                    elif self.upper["filter"] == "cc+pc":
                        self.upper["filter"] = "MIDI"
                    else:
                        self.upper["filter"] = "pc"
                elif change < 0:
                    if self.upper["filter"] == "pc":
                        self.upper["filter"] = "MIDI"
                    elif self.upper["filter"] == "cc+pc":
                        self.upper["filter"] = "pc"
                    else:
                        self.upper["filter"] = "cc+pc"
                color, fx = self.upper_led()
                led_colors = xq.set_led_colors(
                    [color], fx=[fx], start_index=xq.encoder_knob[3]
                )
                to_exquis.send(led_colors)
                display.show("upper filter", value=self.upper["filter"])
            elif xq.is_pressed(msg, xq.sound):
                script.page = instrument_page
                script.page.update()
                all_sound_off()

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
                colors[xq.sound] = red
                for bank, led in enumerate(self.bank_leds):
                    colors[led] = white if bank == self.bank else red
                for pgm, led in enumerate(self.pgm_leds):
                    colors[led] = white if pgm == self.pgm else red
                led_colors = xq.set_led_colors(colors)
                to_exquis.send(led_colors)
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
                script.page = start_page
                script.page.update()

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

        def exquis(self, msg):
            active_sensing.ack = time.time()
            script.page.update(msg)
            # tempo = xq.get_tempo(msg)
            # if tempo is None:
            #     print(msg)

        def master(self, msg):
            to_internal.send(msg)
            show_cc(msg)
            if msg.type != "program_change":
                if start_page.lower["filter"] == "pc":
                    to_lower.send(msg)
                elif start_page.lower["filter"] == "cc+pc":
                    if msg.type != "control_change":
                        to_lower.send(msg)
                if start_page.upper["filter"] == "pc":
                    to_upper.send(msg)
                elif start_page.upper["filter"] == "cc+pc":
                    if msg.type != "control_change":
                        to_upper.send(msg)

        def lower(self, msg):
            if not start_page.lower["local"]:
                to_lower.send(msg)
            if start_page.lower["filter"] == "pc":
                if msg.type != "program_change":
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.upper["filter"] == "pc":
                        to_upper.send(msg)
                    elif start_page.upper["filter"] == "cc+pc":
                        if msg.type != "control_change":
                            to_upper.send(msg)
            elif start_page.lower["filter"] == "cc+pc":
                if msg.type not in ["program_change", "control_change"]:
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.upper["filter"] in ["pc", "cc+pc"]:
                        to_upper.send(msg)

        def upper(self, msg):
            if not start_page.upper["local"]:
                to_upper.send(msg)
            if start_page.upper["filter"] == "pc":
                if msg.type != "program_change":
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.lower["filter"] == "pc":
                        to_lower.send(msg)
                    elif start_page.lower["filter"] == "cc+pc":
                        if msg.type != "control_change":
                            to_lower.send(msg)
            elif start_page.upper["filter"] == "cc+pc":
                if msg.type not in ["program_change", "control_change"]:
                    if not start_page.midi["thru"]:
                        to_internal.send(msg)
                        show_cc(msg)
                    if start_page.lower["filter"] in ["pc", "cc+pc"]:
                        to_lower.send(msg)

        def clock(self, msg):
            # to_exquis.send(msg) # clock will freeze developer mode in exquis
            to_clock.send(msg)
            bpm = rt.bpm(msg)
            if bpm is not None:
                out = xq.set_tempo(bpm)
                to_exquis.send(out)

    to_exquis = Outport(client_name, name="Exquis")
    to_internal = Outport(client_name, name="Internal")
    # to_external = Outport(client_name, name="External")
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
