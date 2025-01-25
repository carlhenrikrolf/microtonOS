import mido
from colour import Color
from menu import Sounds
from utils import (
    Inport,
    Outport,
    make_threads,
    set_volume,
    get_volume,
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

drivers = ["Synth 1", "Synth 2"]


def is_transport(msg):
    return msg.type in ["clock", "start", "stop", "continue"]


def loopbackable(msg):
    result = not is_transport(msg)
    result = result and msg.type not in ["control_change", "sysex", "program_change"]
    return result


class Indicators:
    def __init__(self):
        self.volume, self.muted = get_volume()
        self.gain = 1
        self.xentotune = False
        self.engine = 0
        self.widi = widi.is_connected()
        self.reface_cp = cp.is_connected()

    def knob1(self, turn=None, click=None):
        assert True if turn is None else 0 <= turn <= 1
        if click is turn is None:
            self.volume, self.muted = get_volume()
        else:
            if click is not None:
                self.muted = not self.muted
            if turn is not None:
                update = self.volume + turn
                self.volume = max([0, min([1, update])])
        result = 0 if self.muted else self.volume
        return result

    def knob2(self, turn=None, click=None):
        assert True if turn is None else 0 <= turn <= 1
        if click is not None:
            self.xentotune = not self.xentotune
        if turn is not None:
            update = self.gain + turn
            self.gain = max([0, min([1, update])])
        result = self.gain * (-1 if self.xentotune else 1)
        return result

    def knob3(self, turn=None, click=None):
        assert True if turn is None else 0 <= turn <= 1
        self.widi = widi.is_connected() if click is None else not self.widi
        if self.widi:
            result = -1 if self.engine == -2 else 1
        else:
            result = 0
        return result

    def knob4(self, turn=None, click=None):
        assert True if turn is None else 0 <= turn <= 1
        self.reface_cp = cp.is_connected() if click is None else not self.reface_cp
        if self.reface_cp:
            result = -1 if self.engine == -1 else 1
        else:
            result = 0
        return result


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
                self.volume, self.muted = sounds.knob1(
                    msg
                )  # self.change_volume += sounds.set_volume(msg)
                self.gain, self.xentotune = sounds.knob2(
                    msg
                )  # self.change_gain += sounds.set_gain(msg)
                _, self.local1 = sounds.knob3(
                    msg
                )  # self.local1, self.local2 = sounds.local_control(msg)
                _, self.local2 = sounds.knob4(msg)  # sim.

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
                elif not local:
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
            elif cc.is_in(msg, cc.knobs) and self.xentotune:
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
    to_driver = [Outport(client_name, name=driver) for driver in drivers]
    to_xentotune = Outport(client_name, name="XentoTune")
    clock = Outport(client_name, name="Clock")
    assign = Assign(to_halberstadt)
    indicators = Indicators()
    sounds = Sounds(
        to_exquis,
        engine_banks_pgms,
        indicators,
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
