# external libraries
import mido
import time

# internal libraries
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq
from midi_implementation.midi1 import control_change as cc
from utils import Inport, Outport, make_threads, load_config, set_gain

config = {
    "microtonOS": load_config(__file__, "../config/microtonOS.toml"),
    "control_change": load_config(__file__, "../config/control_change.toml"),
}

black = config["microtonOS"]["palette"]["black"]
white = config["microtonOS"]["palette"]["white"]
red = config["microtonOS"]["palette"]["red"]
orange = config["microtonOS"]["palette"]["orange"]
yellow = config["microtonOS"]["palette"]["yellow"]
green = config["microtonOS"]["palette"]["green"]
cyan = config["microtonOS"]["palette"]["cyan"]
blue = config["microtonOS"]["palette"]["blue"]
magenta = config["microtonOS"]["palette"]["magenta"]


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
            self.routing = [True] * 4
            set_gain(level=1.0, muted=not self.routing[0])

        def update(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                colors = [black] * 128
                for led, on in zip(xq.encoder_knob, self.routing):
                    colors[led] = white if on else red
                led_colors = xq.set_led_colors(colors)
                to_exquis.send(led_colors)
                display.show("")
            elif xq.is_pressed(msg, xq.encoder_button[0]):
                self.routing[0] = not self.routing[0]
                set_gain(level=1.0, muted=not self.routing[0])
                script.page.update()
                display.show("mic", value="on" if self.routing[0] else "off")
            elif xq.is_pressed(msg, xq.encoder_button[1]):
                self.routing[1] = not self.routing[1]
                script.page.update()
                display.show("MIDI", value="receive" if self.routing[1] else "bypass")
            elif xq.is_pressed(msg, xq.encoder_button[2]):
                self.routing[2] = not self.routing[2]
                script.page.update()
                display.show(
                    "lower manual", value="global" if self.routing[2] else "local"
                )
            elif xq.is_pressed(msg, xq.encoder_button[3]):
                self.routing[3] = not self.routing[3]
                script.page.update()
                display.show(
                    "upper manual", value="global" if self.routing[3] else "local"
                )
            elif xq.is_pressed(msg, xq.sound):
                script.page = instrument_page
                script.page.update()
                all_notes_off = mido.Message("control_change", control=cc.all_notes_off)
                to_internal.send(all_notes_off)

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
            to_lower.send(msg)
            to_upper.send(msg)
            show_cc(msg)

        def lower(self, msg):
            if start_page.routing[2]:
                if start_page.routing[3]:
                    to_upper.send(msg)
                if start_page.routing[1]:
                    to_internal.send(msg)
                    show_cc(msg)

        def upper(self, msg):
            if start_page.routing[3]:
                if start_page.routing[2]:
                    to_lower.send(msg)
                if start_page.routing[1]:
                    to_internal.send(msg)
                    show_cc(msg)

        def clock(self, msg):
            # to_exquis.send(msg) # clock will freeze developer mode in exquis
            to_clock.send(msg)

    to_exquis = Outport(client_name, name="Exquis")
    to_internal = Outport(client_name, name="Internal")
    # to_external = Outport(client_name, name="External")
    to_lower = Outport(client_name, name="Lower")
    to_upper = Outport(client_name, name="Upper")
    to_clock = Outport(client_name, name="Clock")

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
