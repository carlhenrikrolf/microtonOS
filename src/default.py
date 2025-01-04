import mido
from colour import Color
from menu import Sounds
from utils import Inport, Outport, make_threads, set_volume, set_gain
from midi_implementation.midi1 import control_change as cc
from midi_implementation.dualo import exquis as xq
from modulation.pedals import Assign


engine_banks_pgms = [
    ["Pianoteq", (9, 4, 4, 2)],
    ["tuneBfree", (12, 12, 12)],
    ["Surge XT", (8, 14, 7, 4, 4)],
]

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


def microtonOS(client_name):
    class Script:
        def __init__(self):
            self.is_init = True
            self.exquis_is_init = True
            self.reopen = False
            self.engine = 0
            self.bank = 0
            self.pgm = 0
            self.change_volume = False
            self.change_gain = False

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
                for outport in to_engine:
                    outport.send(
                        mido.Message("control_change", control=cc.all_notes_off)
                    )

            if sounds.onoff(msg) is True:
                self.engine, self.bank, self.pgm = sounds.select(msg)
                self.change_volume += sounds.set_volume(msg)
                self.change_gain += sounds.set_gain(msg)

            elif sounds.onoff(msg) is False:
                print("eng =", self.engine, "bnk =", self.bank, "pgm =", self.pgm)
                to_isomorphic.send(msg)
                to_engine[self.engine].send(
                    mido.Message(
                        "control_change", control=cc.bank_select[0], value=self.bank
                    )
                )
                to_engine[self.engine].send(
                    mido.Message("program_change", program=self.pgm)
                )
                if self.change_volume:
                    set_volume(sounds.volume, sounds.volume_is_muted)
                    self.change_volume = False
                if self.change_gain:
                    set_gain(sounds.gain, sounds.gain_is_muted)
                    self.change_gain = False
            else:
                to_isomorphic.send(msg)

        def widi(self, msg):
            if self.is_init:
                self.init_touch()
                self.is_init = False
            assigned_to_pedal = assign.target(msg)
            if assigned_to_pedal is None:
                to_manual2.send(msg)

        def reface_cp(self, msg):
            if self.is_init:
                self.init_touch()
                self.is_init = False
            assign.onoff(msg, cc.foot_controller[0])
            assign.source(msg, cc.foot_controller[1])
            assigned_to_pedal = assign.target(msg)
            if (
                assigned_to_pedal is None
                and not msg.is_cc(cc.foot_controller[0])
                and not msg.is_cc(cc.foot_controller[1])
            ):
                to_halberstadt.send(msg)

        def mtsesp_master(self, msg):
            if xq.is_sysex(msg):
                to_exquis.send(msg)
            else:
                to_engine[self.engine].send(msg)

    to_exquis = Outport(client_name, name="Exquis")
    to_reface_cp = Outport(client_name, name="Reface CP")
    to_widi = Outport(client_name, "widi")
    to_isomorphic = Outport(client_name, name="Isomorphic")
    to_halberstadt = Outport(client_name, name="Halberstadt")
    to_manual2 = Outport(client_name, name="Manual 2")
    to_engine = [
        Outport(client_name, name=engine_banks_pgms[i][0])
        for i in range(len(engine_banks_pgms))
    ]
    assign = Assign(to_halberstadt)
    sounds = Sounds(to_exquis, engine_banks_pgms, base_color=menu_colors[1])
    script = Script()
    from_exquis = Inport(script.exquis, client_name, name="Exquis")
    from_widi = Inport(script.widi, client_name, name="widi")
    from_reface_cp = Inport(script.reface_cp, client_name, name="Reface CP")
    from_mtsesp_master = Inport(script.mtsesp_master, client_name, "MTS-ESP master")
    make_threads(
        [from_exquis.open, from_widi.open, from_reface_cp.open, from_mtsesp_master.open]
    )
