# external libraries
import jack
import mido
import mtsespy as esp
import numpy as np
import threading
import time

# internal libraries
from display import Display
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq
from midi_implementation.midi1 import (
    control_change as cc,
    realtime,
    active_sensing as sensing,
)
from midi_implementation import mts
from tuning import Tuning
from layouts import Drums
from sequencer import StepSequencer
from utils import (
    Inport,
    Outport,
    make_threads,
    load_config,
    set_gain4all,
    set_volume4all,
)

config = {
    "general_settings": load_config(__file__, "../config/general_settings.toml"),
    "programs": load_config(__file__, "../config/programs.toml"),
    "control_change": load_config(__file__, "../config/control_change.toml"),
    "tuning": load_config(__file__, "../config/tuning.toml"),
}

black = np.array(config["general_settings"]["palette"]["black"])
white = np.array(config["general_settings"]["palette"]["white"])
blue = np.array(config["general_settings"]["palette"]["blue"])
magenta = np.array(config["general_settings"]["palette"]["magenta"])
red = np.array(config["general_settings"]["palette"]["red"])
yellow = np.array(config["general_settings"]["palette"]["yellow"])
green = np.array(config["general_settings"]["palette"]["green"])
cyan = np.array(config["general_settings"]["palette"]["cyan"])


client_name = "microtonOS"
display = Display()
tuning = Tuning(
    bank_name=config["tuning"]["bank"][0]["name"],
    config=config["tuning"]["bank"][0]["program"][0],
)
ghostnote = 127
drums = Drums(device="Exquis", ghostnote=ghostnote)
step_sequencer = StepSequencer(display_length=6)


def mts_message(freqs, pgm_name=""):
    notes, cents = mts.to_notes_and_cents(freqs)
    tuning_program = 0
    sysex = mts.keybased_dump(
        pgm_name,
        notes,
        cents,
        tuning_program,
    )
    return sysex


def show_cc(msg, engine_name="Pianoteq"):
    if msg.type == "control_change":
        control = str(msg.control)
        transmitted = config["control_change"]["channel"][msg.channel]["transmitted"]
        if control in transmitted and engine_name in transmitted[control]:
            name = transmitted[control][engine_name]
            if type(name) is str:
                display.show(
                    name=name,
                    value=msg.value,
                )
            else:
                n = name[0]
                label = name[1]
                i = int(msg.value / 128 * len(label))
                display.show(name=n, value=label[i])
        else:
            display.show(name="", value=msg.value)


class StartPage:
    def __init__(self):
        self.mic = {"XentoTune": False, "gain": 1.0}
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
        fx = xq.pulse2red if self.mic["XentoTune"] else xq.no_fx
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

    def update(self, msg=None, enter_dev=False):
        if enter_dev:
            developer_mode = xq.enter_developer_mode()
            to_exquis.send(developer_mode)
        if msg is None:
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
            self.mic["XentoTune"] = not self.mic["XentoTune"]
            # set_gain4all(muted=self.mic["muted"])
            color, fx = self.mic_led()
            led_colors = xq.set_led_colors(
                [color], fx=[fx], start_index=xq.encoder_knob[0]
            )
            to_exquis.send(led_colors)
            display.show(
                "mic (+CC)", value="XentoTune" if self.mic["XentoTune"] else "Vocoder"
            )
        elif xq.is_turned(msg, xq.encoder_knob[0]):
            change = xq.is_turned(msg, xq.encoder_knob[0])
            self.mic["gain"] += change / 3.0
            self.mic["gain"] = 1.0 if self.mic["gain"] > 1.0 else self.mic["gain"]
            self.mic["gain"] = 0.0 if self.mic["gain"] < 0.0 else self.mic["gain"]
            set_gain4all(level=self.mic["gain"], muted=False)  # self.mic["muted"])
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
    base_color = magenta

    def __init__(self):
        self.bank = 0
        self.prev_bank = 0
        self.pgm = 0
        self.prev_pgm = 0
        n_banks = len(config["programs"]["engine"][0]["bank"])
        n_banks = 11 if n_banks > 11 else n_banks
        self.bank_leds = range(0, n_banks)
        n_pgms = len(config["programs"]["engine"][0]["bank"][self.bank]["program"])
        n_pgms = 11 if n_pgms > 11 else n_pgms
        n_pgms = 0 if n_pgms == 1 else n_pgms
        self.pgm_leds = range(22, 22 + n_pgms)

    def update(self, msg=None, enter_dev=False):
        if enter_dev:
            developer_mode = xq.enter_developer_mode()
            to_exquis.send(developer_mode)
        if msg is None:
            colors = [black] * 128
            for bank, led in enumerate(self.bank_leds):
                colors[led] = white if bank == self.bank else self.base_color
            for pgm, led in enumerate(self.pgm_leds):
                colors[led] = white if pgm == self.pgm else self.base_color
            pad_colors = [colors[i] for i in xq.pad]
            pad_leds = xq.set_led_colors(pad_colors, start_index=xq.pad[0])
            to_exquis.send(pad_leds)
            misc_colors = [colors[i] for i in xq.arrow_or_encoder]
            misc_leds = xq.set_led_colors(
                misc_colors, start_index=xq.arrow_or_encoder[0]
            )
            to_exquis.send(misc_leds)
            pgm_name = config["programs"]["engine"][0]["bank"][self.bank]["program"][
                self.pgm
            ]
            display.show(pgm_name)
        elif msg.type == "note_on" and msg.velocity > 0 and msg.channel == 15:
            if msg.note in self.bank_leds:
                self.bank = msg.note
                n_pgms = len(
                    config["programs"]["engine"][0]["bank"][self.bank]["program"]
                )
                n_pgms = 11 if n_pgms > 11 else n_pgms
                n_pgms = 0 if n_pgms == 1 else n_pgms
                self.pgm_leds = range(22, 22 + n_pgms)
                self.pgm = -1
                self.update()
                if n_pgms == 0:
                    self.pgm = 0
                    bank_name = config["programs"]["engine"][0]["bank"][self.bank][0][
                        "program"
                    ][0]
                else:
                    bank_name = config["programs"]["engine"][0]["bank"][self.bank][
                        "name"
                    ]
                display.show(bank_name)
            elif msg.note in self.pgm_leds:
                self.pgm = msg.note - 22
                self.prev_bank = self.bank
                self.prev_pgm = self.pgm
                self.update()
                pgm_name = config["programs"]["engine"][0]["bank"][self.bank][
                    "program"
                ][self.pgm]
                display.show(pgm_name)
                pc = [
                    mido.Message(
                        "control_change", control=cc.bank_select[0], value=self.bank
                    ),
                    mido.Message("control_change", control=cc.bank_select[1], value=0),
                    mido.Message("program_change", program=self.pgm),
                ]
                for out in pc:
                    to_internal.send(out)

        elif xq.is_pressed(msg, xq.sound):
            self.bank = self.prev_bank
            self.pgm = self.prev_pgm
            n_pgms = len(config["programs"]["engine"][0]["bank"][self.bank]["program"])
            self.pgm_leds = range(22, 22 + n_pgms)


class RhythmPage:
    base_color = red
    source = ["internal", "external", "upper", "lower"]
    target = ["internal", "external"]
    percussion = [
        "drumkit",
        "toms",
        "cymbals",
        "bongó",
        "congas",
        "timbales",
        "agôgo",
        "shakers",
        "güiro",
        "woodblock",
        "triangle",
    ]
    controller = [80, 81, 82, 83, 84, 85, 86, 87]

    def __init__(self):
        drums.reinitialize(
            high="congas", low="congas", color0=self.base_color, color1=magenta
        )
        self.input = 0
        self.output = 0
        self.low = 0
        self.high = 0
        self.bpm = 120  # need not be the same as script.bpm
        self.dividend = 4
        self.divisor = 4
        self.control_value = [64, 64, 64, 64, 0, 0, 0, 0]
        step_sequencer.time_signature(dividend=self.dividend, divisor=self.divisor)

    def encoder_colors(self):
        color = self.base_color if self.target[self.output] == "internal" else magenta
        colors = [black] * 4
        colors[self.input] = color
        return colors

    def update(self, msg=None, enter_dev=False):
        if enter_dev:
            developer_mode = xq.enter_developer_mode(pads=False)
            to_exquis.send(developer_mode)
        if msg is None:
            snapshot_data = xq.generate_snapshot(
                notes=drums.notes,
                colors=drums.colors,
                polytouch=True,
            )
            snapshot = xq.set_snapshot(snapshot_data)
            to_exquis.send(snapshot)
            colors = [black] * 128
            colors[xq.up] = self.base_color
            colors[xq.down] = self.base_color
            colors[xq.left] = self.base_color
            colors[xq.right] = self.base_color
            colors[xq.encoder_led[0] : xq.encoder_led[3] + 1] = self.encoder_colors()
            misc_colors = [colors[i] for i in xq.arrow_or_encoder]
            misc_leds = xq.set_led_colors(
                misc_colors, start_index=xq.arrow_or_encoder[0]
            )
            to_exquis.send(misc_leds)
            display.show("")
        elif hasattr(msg, "note") and msg.note != ghostnote:
            step_sequencer.record(msg)
            if msg.type in ["note_on", "polytouch"]:
                if self.target[self.output] == "internal":
                    to_internal_rhythm.send(msg)
                else:
                    to_external_rhythm.send(msg)
        elif xq.is_pressed(msg, xq.up):
            if self.source[self.input] == "internal":
                bpm = self.bpm + 2
                self.bpm = max(min(bpm, 240), 20)
                display.show("tempo", value=str(self.bpm) + " bpm")
            else:
                display.show("tempo", value=self.source[self.input])
            led = xq.set_led_colors([white], start_index=xq.up)
            to_exquis.send(led)
        elif xq.is_released(msg, xq.up):
            led = xq.set_led_colors([self.base_color], start_index=xq.up)
            to_exquis.send(led)
        elif xq.is_pressed(msg, xq.down):
            if self.source[self.input] == "internal":
                bpm = self.bpm - 2
                self.bpm = max(min(bpm, 240), 20)
                display.show("tempo", value=str(self.bpm) + " bpm")
            else:
                display.show("tempo", value=self.source[self.input])
            led = xq.set_led_colors([white], start_index=xq.down)
            to_exquis.send(led)
        elif xq.is_released(msg, xq.down):
            led = xq.set_led_colors([self.base_color], start_index=xq.down)
            to_exquis.send(led)
        elif xq.is_slid(msg):  # I think I will have to deal with slider separately
            self.divisor = 2 ** (xq.is_slid(msg) - 1)
            step_sequencer.time_signature(divisor=self.divisor)
            subtext = str(self.dividend) + "/" + str(self.divisor)
            display.show("time signature", value=subtext)
        elif xq.is_pressed(msg, xq.left):
            dividend = self.dividend - 1
            self.dividend = max(min(dividend, 64), 1)
            step_sequencer.time_signature(dividend=self.dividend)
            subtext = str(self.dividend) + "/" + str(self.divisor)
            display.show("time signature", value=subtext)
            led = xq.set_led_colors([white], start_index=xq.left)
            to_exquis.send(led)
        elif xq.is_released(msg, xq.left):
            led = xq.set_led_colors([self.base_color], start_index=xq.left)
            to_exquis.send(led)
        elif xq.is_pressed(msg, xq.right):
            dividend = self.dividend + 1
            self.dividend = max(min(dividend, 64), 1)
            step_sequencer.time_signature(dividend=self.dividend)
            subtext = str(self.dividend) + "/" + str(self.divisor)
            display.show("time signature", value=subtext)
            led = xq.set_led_colors([white], start_index=xq.right)
            to_exquis.send(led)
        elif xq.is_released(msg, xq.right):
            led = xq.set_led_colors([self.base_color], start_index=xq.right)
            to_exquis.send(led)
        elif xq.is_turned(msg, xq.encoder_knob[0]):
            if shift.is_on:
                control_value = self.control_value[0] + int(
                    15 * xq.is_turned(msg, xq.encoder_knob[0])
                )
                self.control_value[0] = max(min(control_value, 127), 0)
                display.show(
                    "CC " + str(self.controller[0]), value=str(self.control_value[0])
                )
            else:
                sensitivity = min(15, len(self.source))
                i = self.input + int(
                    sensitivity * xq.is_turned(msg, xq.encoder_knob[0])
                )
                self.input = max(min(i, 3), 0)
                display.show("source", value=self.source[self.input])
                colors = self.encoder_colors()
                leds = xq.set_led_colors(colors, start_index=xq.encoder_led[0])
                to_exquis.send(leds)
        elif xq.is_turned(msg, xq.encoder_knob[1]):
            if shift.is_on:
                control_value = self.control_value[1] + int(
                    15 * xq.is_turned(msg, xq.encoder_knob[1])
                )
                self.control_value[1] = max(min(control_value, 127), 0)
                display.show(
                    "CC " + str(self.controller[1]), value=str(self.control_value[1])
                )
            else:
                o = self.output + int(15 * xq.is_turned(msg, xq.encoder_knob[1]))
                self.output = 1 if o > 0 else 0
                display.show("target", value=self.target[self.output])
                colors = self.encoder_colors()
                leds = xq.set_led_colors(colors, start_index=xq.encoder_led[0])
                to_exquis.send(leds)
        elif xq.is_turned(msg, xq.encoder_knob[2]):
            if shift.is_on:
                control_value = self.control_value[2] + int(
                    15 * xq.is_turned(msg, xq.encoder_knob[2])
                )
                self.control_value[2] = max(min(control_value, 127), 0)
                display.show(
                    "CC " + str(self.controller[2]), value=str(self.control_value[2])
                )
            else:
                sensitivity = min(15, len(self.percussion))
                low = self.low + int(
                    sensitivity * xq.is_turned(msg, xq.encoder_knob[2])
                )
                self.low = max(min(low, len(self.percussion) - 1), 0)
                drums.reinitialize(
                    high=self.percussion[self.high], low=self.percussion[self.low]
                )
                snapshot_data = xq.generate_snapshot(
                    notes=drums.notes,
                    colors=drums.colors,
                    polytouch=True,
                )
                snapshot = xq.set_snapshot(snapshot_data)
                to_exquis.send(snapshot)
                display.show("low drum", value=self.percussion[self.low])
        elif xq.is_turned(msg, xq.encoder_knob[3]):
            if shift.is_on:
                control_value = self.control_value[3] + int(
                    15 * xq.is_turned(msg, xq.encoder_knob[3])
                )
                self.control_value[3] = max(min(control_value, 127), 0)
                display.show(
                    "CC " + str(self.controller[3]), value=str(self.control_value[3])
                )
            else:
                sensitivity = min(15, len(self.percussion))
                high = self.high + int(
                    sensitivity * xq.is_turned(msg, xq.encoder_knob[3])
                )
                self.high = max(min(high, len(self.percussion) - 1), 0)
                drums.reinitialize(
                    high=self.percussion[self.high], low=self.percussion[self.low]
                )
                snapshot_data = xq.generate_snapshot(
                    notes=drums.notes,
                    colors=drums.colors,
                    polytouch=True,
                )
                snapshot = xq.set_snapshot(snapshot_data)
                to_exquis.send(snapshot)
                display.show("high drum", value=self.percussion[self.high])
        elif xq.is_pressed(msg, xq.encoder_button[0]):
            if shift.is_on:
                self.control_value[4] = 127 - self.control_value[4]
                display.show(
                    "CC " + str(self.controller[4]), value=str(self.control_value[4])
                )
        elif xq.is_pressed(msg, xq.encoder_button[1]):
            if shift.is_on:
                self.control_value[5] = 127 - self.control_value[5]
                display.show(
                    "CC " + str(self.controller[5]), value=str(self.control_value[5])
                )
        elif xq.is_pressed(msg, xq.encoder_button[2]):
            if shift.is_on:
                self.control_value[6] = 127 - self.control_value[6]
                display.show(
                    "CC " + str(self.controller[6]), value=str(self.control_value[6])
                )
        elif xq.is_pressed(msg, xq.encoder_button[3]):
            if shift.is_on:
                self.control_value[7] = 127 - self.control_value[7]
                display.show(
                    "CC " + str(self.controller[7]), value=str(self.control_value[7])
                )
        elif xq.is_pressed(msg, xq.record):
            pass


class IsomorphicPage:
    base_color = yellow

    def update(self, msg=None, enter_dev=False):
        if enter_dev:
            developer_mode = xq.enter_developer_mode()
            to_exquis.send(developer_mode)
        if msg is None:
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
    base_color = green

    def __init__(self):
        self.bank = 0
        self.prev_bank = 0
        self.pgm = 0
        self.prev_pgm = 0
        n_banks = len(config["tuning"]["bank"])
        n_banks = 11 if n_banks > 11 else n_banks
        self.bank_leds = range(0, n_banks)
        n_pgms = len(config["tuning"]["bank"][self.bank]["program"])
        n_pgms = 0 if n_pgms == 1 else n_pgms
        self.pgm_leds = range(22, 22 + n_pgms)
        esp.set_multi_channel_note_tunings(tuning.linear, linear_tun_ch)
        esp.set_multi_channel_note_tunings(tuning.lower, lower_tun_ch)
        esp.set_multi_channel_note_tunings(tuning.upper, upper_tun_ch)
        self.dynamic_freqs = tuning.linear
        esp.set_note_tunings(self.dynamic_freqs)
        pgm_name = config["tuning"]["bank"][self.bank]["program"][self.pgm]["name"]
        esp.set_scale_name(pgm_name)
        self.last_freq = None

    def retune(self, msg=None, channel=None):
        if msg is None:
            bank_config = config["tuning"]["bank"][self.bank]
            bank_name = bank_config["name"]
            pgm_config = bank_config["program"][self.pgm]
            tuning.reinitialize(bank_name, pgm_config)
            esp.set_multi_channel_note_tunings(tuning.linear, linear_tun_ch)
            esp.set_multi_channel_note_tunings(tuning.lower, lower_tun_ch)
            esp.set_multi_channel_note_tunings(tuning.upper, upper_tun_ch)
            self.dynamic_freqs = tuning.linear
            esp.set_note_tunings(self.dynamic_freqs)
            pgm_name = pgm_config["name"]
            esp.set_scale_name(pgm_name)
            self.last_freq = None
        elif msg.type == "note_on" and msg.velocity > 0:
            channel = linear_tun_ch if channel is None else channel
            if channel == linear_tun_ch:
                freq = tuning.linear[msg.note]
            elif channel == lower_tun_ch:
                freq = tuning.lower[msg.note]
            elif channel == upper_tun_ch:
                freq = tuning.upper[msg.note]
            esp.set_note_tuning(freq, msg.note)
            self.dynamic_freqs[msg.note] = freq
            if self.last_freq is not None:
                cents = np.log2(freq / self.last_freq) * 1200
                cents = round(cents, ndigits=1)
                display.show(flipside=str(cents) + "c")
            self.last_freq = freq

    def sysex(self, channel=None):
        pgm_name = config["tuning"]["bank"][self.bank]["program"][self.pgm]["name"]
        if channel == linear_tun_ch:
            return mts_message(tuning.linear, pgm_name)
        elif channel == lower_tun_ch:
            return mts_message(tuning.lower, pgm_name)
        elif channel == upper_tun_ch:
            return mts_message(tuning.upper, pgm_name)
        else:
            return mts_message(self.dynamic_freqs, pgm_name)

    def update(self, msg=None, enter_dev=False):
        if enter_dev:
            developer_mode = xq.enter_developer_mode()
            to_exquis.send(developer_mode)
        if msg is None:
            colors = [black] * 128
            for bank, led in enumerate(self.bank_leds):
                colors[led] = white if bank == self.bank else self.base_color
            for pgm, led in enumerate(self.pgm_leds):
                colors[led] = white if pgm == self.pgm else self.base_color
            pad_colors = [colors[i] for i in xq.pad]
            pad_leds = xq.set_led_colors(pad_colors, start_index=xq.pad[0])
            to_exquis.send(pad_leds)
            misc_colors = [colors[i] for i in xq.arrow_or_encoder]
            misc_leds = xq.set_led_colors(
                misc_colors, start_index=xq.arrow_or_encoder[0]
            )
            to_exquis.send(misc_leds)
            display.show("")
            pgm_name = config["tuning"]["bank"][self.bank]["program"][self.pgm]["name"]
            display.show(pgm_name)
        elif msg.type == "note_on" and msg.velocity > 0 and msg.channel == 15:
            if msg.note in self.bank_leds:
                self.bank = msg.note
                n_pgms = len(config["tuning"]["bank"][self.bank]["program"])  # 1=0
                n_pgms = 0 if n_pgms == 1 else n_pgms
                self.pgm_leds = range(22, 22 + n_pgms)
                self.pgm = -1
                self.update()
                if n_pgms == 0:
                    self.pgm = 0
                    bank_name = config["tuning"]["bank"][self.bank]["program"][0][
                        "name"
                    ]
                    self.retune()
                else:
                    bank_name = config["tuning"]["bank"][self.bank]["name"]
                display.show(bank_name)
            elif msg.note in self.pgm_leds:
                self.pgm = msg.note - 22
                self.prev_bank = self.bank
                self.prev_pgm = self.pgm
                self.update()
                pgm_name = config["tuning"]["bank"][self.bank]["program"][self.pgm][
                    "name"
                ]
                self.retune()
                display.show(pgm_name)

        elif xq.is_pressed(msg, xq.clips):
            self.bank = self.prev_bank
            self.pgm = self.prev_pgm
            n_pgms = len(config["config"]["bank"][self.bank]["program"])
            self.pgm_leds = range(22, 22 + n_pgms)


class Shift:
    base_color = blue

    def __init__(self):
        self.is_on = False
        self.is_locked = False
        self.is_tmp = False

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
                led_color = xq.set_led_colors(
                    [self.base_color], start_index=xq.settings
                )
                to_exquis.send(led_color)
                display.show("shift")
        elif xq.is_released(msg, xq.settings):
            if self.is_on:
                if self.is_tmp:  # added
                    self.is_on = False
                    self.is_tmp = False
                    led_color = xq.set_led_colors([black], start_index=xq.settings)
                    to_exquis.send(led_color)
                else:
                    self.is_locked = True
                    led_color = xq.set_led_colors(
                        [self.base_color], start_index=xq.settings
                    )
                    to_exquis.send(led_color)
                    display.show("shift lock")
        elif msg.type == "control_change":
            if self.is_on and not self.is_locked:
                # self.is_on = False
                self.is_tmp = True
                led_color = xq.set_led_colors([black], start_index=xq.settings)
                to_exquis.send(led_color)


class Play:
    def __init__(self):
        self.base_color = cyan
        self.is_on = False
        self.to_all = False

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
                step_sequencer.play(stop)
                to_internal_rhythm.send(stop)
                to_external_rhythm.send(stop)
                led_color = xq.set_led_colors([black], start_index=xq.play)
                to_exquis.send(led_color)
                display.show("all stop")
            elif self.is_on:
                self.is_on = False
                stop = mido.Message("stop")
                step_sequencer.play(stop)
                if rhythm_page.target[rhythm_page.output] == "internal":
                    to_internal_rhythm.send(stop)
                else:
                    to_external_rhythm.send(stop)
                led_color = xq.set_led_colors([black], start_index=xq.play)
                to_exquis.send(led_color)
                display.show("stop")
            elif not shift.is_on:
                self.base_color = cyan
                self.is_on = True
                self.counter = 0
                start = mido.Message("start")
                step_sequencer.play(start)
                if rhythm_page.target[rhythm_page.output] == "internal":
                    to_internal_rhythm.send(start)
                else:
                    to_external_rhythm.send(start)
                led_color = xq.set_led_colors([self.base_color], start_index=xq.play)
                to_exquis.send(led_color)
                subtext = str(round(script.bpm)) + " bpm"
                display.show("play", subtext)
            elif shift.is_on:
                self.base_color = white
                self.to_all = True
                self.is_on = True
                self.counter = 0
                start = mido.Message("start")
                step_sequencer.play(start)
                to_internal_rhythm.send(start)
                to_external_rhythm.send(start)
                to_lower.send(start)
                to_upper.send(start)
                led_color = xq.set_led_colors([self.base_color], start_index=xq.play)
                to_exquis.send(led_color)
                subtext = str(round(script.bpm)) + " bpm"
                display.show("all play", subtext)


class Script:
    def __init__(self):
        self.ack = 0.0
        self.page = start_page
        self.bpm = 120.0
        self.is_menu = [False] * 4
        self.is_slid = False

    def exquis(self, msg):
        self.ack = time.time()
        if xq.is_slid(msg):
            self.is_slid = True
        elif xq.is_unslid(msg):
            self.is_slid = False
        shift.update(msg)
        play.update(msg)
        if xq.is_pressed(msg, xq.sound):
            self.is_menu = [not self.is_menu[0], False, False, False]
            self.page = instrument_page if self.is_menu[0] else start_page
            self.page.update(enter_dev=True)
        elif xq.is_pressed(msg, xq.record):
            self.is_menu = [False, not self.is_menu[1], False, False]
            self.page = rhythm_page if self.is_menu[1] else start_page
            self.page.update(enter_dev=True)
        elif xq.is_pressed(msg, xq.loop):
            self.is_menu = [False, False, not self.is_menu[2], False]
            self.page = isomorphic_page if self.is_menu[2] else start_page
            self.page.update(enter_dev=True)
        elif xq.is_pressed(msg, xq.clips):
            self.is_menu = [False, False, False, not self.is_menu[3]]
            self.page = tuning_page if self.is_menu[3] else start_page
            self.page.update(enter_dev=True)
        else:
            self.page.update(msg)
        if any([xq.is_pressed(msg, button) for button in xq.menu]):
            all_sound_off()
        menu_colors = [
            shift.base_color if shift.is_on else black,
            instrument_page.base_color if self.is_menu[0] else black,
            rhythm_page.base_color if self.is_menu[1] else black,
            isomorphic_page.base_color if self.is_menu[2] else black,
            tuning_page.base_color if self.is_menu[3] else black,
            play.base_color if play.is_on else black,
        ]
        menu_leds = xq.set_led_colors(menu_colors, start_index=xq.settings)
        to_exquis.send(menu_leds)
        # tempo = xq.get_tempo(msg)
        # if tempo is None:
        #     print(msg)

    def master(self, msg):
        if msg.type == "control_change":
            to_external.send(msg)
            if start_page.mic["XentoTune"]:
                to_xentotune.send(msg)
                show_cc(msg, "XentoTune")
            else:
                to_internal.send(msg)
                show_cc(msg)
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
        untune = False
        if msg.is_realtime and rhythm_page.source[rhythm_page.input] == "lower":
            self.bpm = realtime.bpm(msg)
            self.tick(msg, loop="lower")
        elif msg.type != "active_sensing":
            if msg.type == "note_on" and msg.velocity > 0:
                sysex = tuning_page.sysex(lower_tun_ch)
                to_lower.send(sysex)
                if start_page.lower["filter"] != "MIDI":
                    tuning_page.retune(msg, channel=lower_tun_ch)
                    to_upper.send(sysex)
                    untune = True
            if start_page.lower["filter"] == "PC":
                if msg.type != "program_change":
                    if hasattr(msg, "note"):
                        sysex = tuning_page.sysex(lower_tun_ch)
                        to_external.send(sysex)
                    to_external.send(msg)
                    if not start_page.midi["thru"]:
                        if hasattr(msg, "note"):
                            note = msg.copy(channel=lower_tun_ch)
                            to_internal.send(note)
                        elif msg.type == "control_change":
                            if start_page.mic["XentoTune"]:
                                to_xentotune.send(msg)
                                show_cc(msg, "XentoTune")
                            else:
                                to_internal.send(msg)
                                show_cc(msg)
                        else:
                            to_internal.send(msg)
                        show_cc(msg)
                    if start_page.upper["filter"] == "PC":
                        to_upper.send(msg)
                    elif start_page.upper["filter"] == "CC+PC":
                        if msg.type != "control_change":
                            to_upper.send(msg)
            elif start_page.lower["filter"] == "CC+PC":
                if msg.type not in ["program_change", "control_change"]:
                    if hasattr(msg, "note"):
                        sysex = tuning_page.sysex(lower_tun_ch)
                        to_external.send(sysex)
                    to_external.send(msg)
                    if not start_page.midi["thru"]:
                        if hasattr(msg, "note"):
                            note = msg.copy(channel=lower_tun_ch)
                            to_internal.send(note)
                        else:
                            to_internal.send(msg)
                    if start_page.upper["filter"] in ["PC", "CC+PC"]:
                        to_upper.send(msg)
            if not start_page.lower["local"]:
                to_lower.send(msg)
            if untune:
                sysex = tuning_page.sysex(upper_tun_ch)
                to_upper.send(sysex)

    def upper(self, msg):
        untune = False
        if msg.is_realtime and rhythm_page.source[rhythm_page.input] == "upper":
            self.bpm = realtime.bpm(msg)
            self.tick(msg, loop="upper")
        elif msg.type != "active_sensing":
            if msg.type == "note_on" and msg.velocity > 0:
                sysex = tuning_page.sysex(upper_tun_ch)
                to_upper.send(sysex)
                if start_page.upper["filter"] != "MIDI":
                    tuning_page.retune(msg, upper_tun_ch)
                    to_lower.send(msg)
                    untune = True
            if start_page.upper["filter"] == "PC":
                if msg.type != "program_change":
                    if hasattr(msg, "note"):
                        sysex = tuning_page.sysex(upper_tun_ch)
                        to_external.send(sysex)
                    to_external.send(msg)
                    if not start_page.midi["thru"]:
                        if hasattr(msg, "note"):
                            note = msg.copy(channel=upper_tun_ch)
                            to_internal.send(note)
                        elif msg.type == "control_change":
                            if start_page.mic["XentoTune"]:
                                to_xentotune.send(msg)
                                show_cc(msg, "XentoTune")
                            else:
                                to_internal.send(msg)
                                show_cc(msg)
                        else:
                            to_internal.send(msg)
                        show_cc(msg)
                    if start_page.lower["filter"] == "PC":
                        to_lower.send(msg)
                    elif start_page.lower["filter"] == "CC+PC":
                        if msg.type != "control_change":
                            to_lower.send(msg)
            elif start_page.upper["filter"] == "CC+PC":
                if msg.type not in ["program_change", "control_change"]:
                    if hasattr(msg, "note"):
                        sysex = tuning_page.sysex(upper_tun_ch)
                        to_external.send(sysex)
                    to_external.send(msg)
                    if not start_page.midi["thru"]:
                        if hasattr(msg, "note"):
                            note = msg.copy(channel=upper_tun_ch)
                            to_internal.send(note)
                        else:
                            to_internal.send(msg)
                    if start_page.lower["filter"] in ["PC", "CC+PC"]:
                        to_lower.send(msg)
            if not start_page.upper["local"]:
                to_upper.send(msg)
            if untune:
                sysex = tuning_page.sysex(lower_tun_ch)
                to_lower.send(sysex)

    def rhythm(self, msg):
        if msg.is_realtime and rhythm_page.source[rhythm_page.input] == "external":
            self.bpm = realtime.bpm(msg)
            self.tick(msg, loop="external")

    def tick(self, msg, loop=None):
        if msg.is_realtime:
            sysex = xq.set_tempo(self.bpm)
            to_exquis.send(sysex)
            to_internal_rhythm.send(msg)
            if loop != "external":
                to_external_rhythm.send(msg)
            if loop != "lower":
                to_lower.send(msg)
            if loop != "upper":
                to_upper.send(msg)
            if not self.is_slid:
                colors = [white if step_sequencer.display() else black]
                leds = xq.set_led_colors(colors, start_index=xq.slider[0])
                to_exquis.send(leds)
        notes_on = step_sequencer.play(msg)
        if rhythm_page.target[rhythm_page.output] == "internal":
            to_internal_rhythm.send(notes_on)
        else:
            to_external_rhythm.send(notes_on)

    def clock(self):
        while True:
            if rhythm_page.source[rhythm_page.input] == "internal":
                msg = mido.Message("clock")
                self.tick(msg)
            realtime.sleep(rhythm_page.bpm)

    def active_sensing(self):
        while True:
            # Exquis
            now = time.time()
            diff = now - self.ack
            ack = xq.get_tempo()
            to_exquis.send(ack)
            if diff > 2 * sensing.transmit_sec:
                self.page.update(enter_dev=True)
            # The rest
            to_internal.send(mido.Message("active_sensing"))
            to_lower.send(mido.Message("active_sensing"))
            to_upper.send(mido.Message("active_sensing"))
            time.sleep(sensing.transmit_sec)


if esp.has_ipc() and not esp.can_register_master():
    esp.reinitialize()

with esp.Master():
    linear_tun_ch = 0
    lower_tun_ch = 1
    upper_tun_ch = 2
    for channel in range(16):
        is_on = channel in [linear_tun_ch, lower_tun_ch, upper_tun_ch]
        esp.set_multi_channel(is_on, channel)

    to_exquis = Outport(client_name, name="Exquis")
    to_lower = Outport(client_name, name="Lower")
    to_upper = Outport(client_name, name="Upper")
    to_internal = Outport(client_name, name="Internal")
    to_external = Outport(client_name, name="External")
    to_internal_rhythm = Outport(client_name, name="Internal Rhythm")
    to_external_rhythm = Outport(client_name, name="External Rhythm")
    to_xentotune = Outport(client_name, name="XentoTune")

    def all_sound_off():
        msg = mido.Message("control_change", control=cc.all_sound_off)
        to_lower.send(msg)
        to_upper.send(msg)
        to_internal.send(msg)
        to_external.send(msg)
        to_internal_rhythm.send(msg)
        to_external_rhythm.send(msg)
        to_xentotune.send(msg)

    start_page = StartPage()
    instrument_page = InstrumentPage()
    rhythm_page = RhythmPage()
    isomorphic_page = IsomorphicPage()
    tuning_page = TuningPage()
    shift = Shift()
    play = Play()
    script = Script()

    from_exquis = Inport(script.exquis, client_name, name="Exquis")
    from_upper = Inport(script.upper, client_name, name="Upper")
    from_lower = Inport(script.lower, client_name, name="Lower")
    from_master = Inport(script.master, client_name, name="Master")
    from_rhythm = Inport(script.rhythm, client_name, name="Rhythm")

    selector_client = jack.Client("microtonOS Selector")

    @selector_client.set_process_callback
    def process(frames):
        assert frames == selector_client.blocksize
        in_mono = selector_client.inports[0]
        out_left = selector_client.outports[2 if start_page.mic["XentoTune"] else 0]
        out_right = selector_client.outports[3 if start_page.mic["XentoTune"] else 1]
        out_left.get_buffer()[:] = in_mono.get_buffer()
        out_right.get_buffer()[:] = in_mono.get_buffer()

    selector_client.inports.register("input_MONO")
    selector_client.outports.register("to_Vocoder_FL")
    selector_client.outports.register("to_Vocoder_FR")
    selector_client.outports.register("to_XentoTune_FL")
    selector_client.outports.register("to_XentoTune_FR")

    def selector():
        event = threading.Event()
        with selector_client:
            try:
                event.wait()
            except KeyboardInterrupt:
                pass

    make_threads(
        [
            from_exquis.open,
            from_upper.open,
            from_lower.open,
            from_master.open,
            from_rhythm.open,
            script.clock,
            script.active_sensing,
            display.run,
            selector,
        ]
    )
