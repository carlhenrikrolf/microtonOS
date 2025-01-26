import mido
from colour import Color
from menu import Sounds
from utils import (
    Inport,
    Outport,
    make_threads,
    set_volume,
    get_volume,
    set_luminance,
)
from midi_implementation.midi1 import control_change as cc
from midi_implementation.dualo import exquis as xq
from midi_implementation.yamaha import reface_cp as cp
from midi_implementation.cme import widi_master as widi
from modulation.pedals import Assign

menu_colors = [  # 🔴🟠🟡🟢🔵🟣
    Color("red"),
    Color("darkorange"),
    Color("yellow"),
    Color("green"),
    Color("blue"),
    Color("magenta"),
]

buttons = [
    xq.settings,
    xq.sounds,
    xq.record,
    xq.tracks,
    xq.scenes,
    xq.play_stop,
]

engine_banks_pgms = [
    ["Pianoteq", (9, 4, 4, 2)],
    ["tuneBfree", (12, 12, 12)],
    ["Surge XT", (8, 14, 7, 4, 4)],
]

drivers = [
    ["Synth 1", cp.is_connected],
    ["Synth 2", widi.is_connected],
]


def is_transport(msg):
    return msg.type in ["clock", "start", "stop", "continue"]


def loopbackable(msg):
    result = not is_transport(msg)
    result = result and msg.type not in ["control_change", "sysex", "program_change"]
    return result


class Indicators:
    def __init__(self):
        self.gain = 1
        self.xentotune = False
        self.engine = 0
        self.widi = False
        self.cp = False
        self.sounds_color = "DarkOrange"

    def sounds1(self, turn=None, click=None):
        volume, muted = get_volume() if click is turn is None else (turn, click)
        luminance = 0 if muted else volume
        color = set_luminance(self.sounds_color, luminance)
        return color

    def sounds2(self, turn=None, click=None):
        if not (turn is click is None):
            self.gain, self.xentotune = turn, click
        luminance = self.gain * (-1 if self.xentotune else 1)
        color = set_luminance(self.sounds_color, luminance)
        return color

    def sounds3(self, turn=None, click=None):
        if widi.is_connected():
            self.widi = self.widi if click is None else click
            reference = None if self.widi else Color("white")
            luminance = -1 if self.engine == -2 else 1
            color = set_luminance(self.sounds_color, luminance, reference=reference)
        else:
            color = Color("black")
        return color

    def sounds4(self, turn=None, click=None):
        if cp.is_connected():
            self.cp = self.cp if click is None else click
            reference = None if self.cp else Color("white")
            luminance = -1 if self.engine == -1 else 1
            color = set_luminance(self.sounds_color, luminance, reference=reference)
        else:
            color = Color("black")
        return color


def microtonOS(client_name):
    class Script:
        def __init__(self):
            self.is_init = True
            self.exquis_is_init = True
            self.reopen = False
            self.engine = 0
            indicators.engine = self.engine
            self.bank = 0
            self.pgm = 0
            self.outport = to_engine[self.engine]
            self.volume = 1.0
            self.muted = False
            self.gain = 1.0
            self.xentotune = False
            self.local1 = False
            self.local2 = False

        def init_touch(self):
            for i, button in enumerate(buttons):
                xq.send(
                    to_exquis, xq.sysex(xq.color_button, button, xq.led(menu_colors[i]))
                )

        def exquis(self, msg):
            if self.exquis_is_init:
                self.init_touch()
                self.is_init = False
                self.exquis_is_init = False

            if any(
                [xq.is_sysex(msg, [xq.click, button, xq.pressed]) for button in buttons]
            ):
                for outport in *to_engine, *to_driver:
                    outport.send(
                        mido.Message("control_change", control=cc.all_notes_off)
                    )

            if sounds.onoff(msg) is True:
                self.engine, self.bank, self.pgm = sounds.select(msg)
                self.indicators = self.engine
                self.volume, self.muted = sounds.knob(1,
                    msg
                )
                self.gain, self.xentotune = sounds.knob(2,
                    msg
                )
                _, self.local1 = sounds.knob(3, msg
                )
                _, self.local2 = sounds.knob(4,msg)  # sim.

            elif sounds.onoff(msg) is False:
                to_isomorphic.send(msg)

                if self.engine >= 0:
                    self.outport = to_engine[self.engine]
                    bank_select = mido.Message(
                        "control_change", control=cc.bank_select[0], value=self.bank
                    )
                    self.outport.send(bank_select)
                    program_change = mido.Message("program_change", program=self.pgm)
                    self.outport.send(program_change)
                else:
                    driver = -self.engine - 1
                    self.outport = to_driver[driver]

                set_volume(self.volume, self.muted)
                onoff = mido.Message("control_change", control=cc.local_onoff_switch)
                onoff.value = 127 if self.xentotune else 0
                to_xentotune.send(onoff)
                gain = mido.Message("control_change", control=cc.volume[1])
                gain.value = round(127 * self.gain)
                to_xentotune.send(gain)

            else:
                to_isomorphic.send(msg)

        def synth1(self, msg):
            if self.is_init:
                self.init_touch()
                self.is_init = False
            no_menu = not sounds.is_on
            if no_menu:
                local = self.local1 or self.engine == -1
                if is_transport(msg):
                    clock.send(msg)
                elif local and loopbackable(msg):
                    to_halberstadt.send(msg)
                elif not local:  # Can assign not be moved to loopback from mtsesp?
                    assign.onoff(msg, cc.foot_controller[0])
                    assign.source(msg, cc.foot_controller[1])
                    assigned_to_pedal = assign.target(msg)
                    if (
                        assigned_to_pedal is None
                        and not msg.is_cc(cc.foot_controller[0])
                        and not msg.is_cc(cc.foot_controller[1])
                    ):
                        to_halberstadt.send(msg)

        def synth2(self, msg):
            if self.is_init:
                self.init_touch()
                self.is_init = False
            no_menu = not sounds.is_on
            if no_menu:
                local = self.local2 and self.engine == -2
                assigned_to_pedal = assign.target(msg)
                if assigned_to_pedal is None:
                    if is_transport(msg):
                        clock.send(msg)
                    elif (local and loopbackable(msg)) or not local:
                        to_manual2.send(msg)

        def mtsesp_master(self, msg):
            if xq.is_active_sensing(msg):
                to_exquis.send(msg)
            elif xq.is_sysex(msg) and not sounds.is_on:
                to_exquis.send(msg)
            elif self.xentotune and cc.is_in(msg, cc.knobs):
                to_xentotune.send(msg)
            elif hasattr(msg, "channel"):
                if self.engine == -1:
                    if self.local1 and msg.channel in range(1, 13):
                        to_driver[2 - 1].send(msg)
                    elif self.local2 and msg.channel in [14, 15]:
                        to_driver[2 - 1].send(msg)
                    else:
                        self.outport.send(msg)
                elif self.engine == -2:
                    if self.local2 and msg.channel in range(1, 13):
                        to_driver[1 - 1].send(msg)
                    elif self.local1 and msg.channel in [0, 13]:
                        to_driver[1 - 1].send(msg)
                    else:
                        self.outport.send(msg)
                else:
                    if self.local1 and msg.channel in [0, 13]:
                        to_driver[1 - 1].send(msg)
                    elif self.local2 and msg.channel in [14, 15]:
                        to_driver[2 - 1].send(msg)
                    else:
                        self.outport.send(msg)
            else:
                self.outport.send(msg)

    to_exquis = Outport(client_name, name="Exquis")
    to_isomorphic = Outport(client_name, name="Isomorphic")
    to_halberstadt = Outport(client_name, name="Halberstadt")
    to_manual2 = Outport(client_name, name="Manual 2")
    to_engine = [
        Outport(client_name, name=engine_banks_pgms[i][0])
        for i in range(len(engine_banks_pgms))
    ]
    to_driver = [Outport(client_name, name=driver[0]) for driver in drivers]
    to_xentotune = Outport(client_name, name="XentoTune")
    clock = Outport(client_name, name="Clock")
    assign = Assign(to_halberstadt)
    indicators = Indicators()
    sounds = Sounds(
        to_exquis,
        engine_banks_pgms,
        drivers=drivers,
        indicators=[indicators.sounds1, indicators.sounds2, indicators.sounds3, indicators.sounds4],
        base_color=menu_colors[1],
    )
    script = Script()
    from_exquis = Inport(script.exquis, client_name, name="Exquis")
    from_synth1 = Inport(script.synth1, client_name, name="Synth 1")
    from_synth2 = Inport(script.synth2, client_name, name="Synth 2")
    from_mtsesp_master = Inport(script.mtsesp_master, client_name, "MTS-ESP Master")
    make_threads(
        [from_exquis.open, from_synth1.open, from_synth2.open, from_mtsesp_master.open]
    )
