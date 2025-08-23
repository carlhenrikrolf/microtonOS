# external libraries
from colour import Color
import time

# internal libraries
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq
from utils import Inport, Outport, make_threads, load_config

config = {
    "microtonOS": load_config(__file__, "../config/microtonOS.toml"),
    "control_change": load_config(__file__, "../config/control_change.toml"),
}


def microtonOS(Display):
    client_name = "microtonOS"
    display = Display()

    class Exquis:
        ack_rate = 0.3  # seconds

        def __init__(self):
            self.ack = 0.0
            self.page = self.start_page

        def active_sensing(self):
            while True:
                now = time.time()
                diff = now - self.ack
                ack = xq.get_tempo()
                to_exquis.send(ack)
                if diff > 2 * self.ack_rate:
                    self.page()
                time.sleep(self.ack_rate)

        def start_page(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                all_black = [Color("black")] * 128
                for led in xq.encoder_knob:
                    all_black[led] = Color("red")
                led_colors = xq.set_led_colors(all_black)
                to_exquis.send(led_colors)
                display.show("")
            elif xq.is_pressed(msg, xq.sound):
                self.page = self.instrument_page
                self.page()

        def instrument_page(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                all_black = [Color("black")] * 128
                for led, bank in enumerate(config["microtonOS"]["engine"][0]["bank"]):
                    all_black[led] = Color("red")
                led_colors = xq.set_led_colors(all_black)
                to_exquis.send(led_colors)
                display.show("instrument")
            elif xq.is_pressed(msg, xq.sound):
                self.page = self.start_page
                self.page()

    class Script:
        def exquis(self, msg):
            exquis.ack = time.time()
            exquis.page(msg)
            tempo = xq.get_tempo(msg)
            if tempo is None:
                print(msg)

        def upper(self, msg):
            self.show_cc(msg)
            to_lower.send(msg)
            to_pianoteq.send(msg)

        def lower(self, msg):
            self.show_cc(msg)
            to_upper.send(msg)
            to_pianoteq.send(msg)

        def show_cc(self, msg):
            if msg.type == "control_change":
                control = str(msg.control)
                print(control)
                if (
                    control
                    in config["control_change"]["channel"][msg.channel]["transmitted"]
                ):
                    config["control_change"]["channel"][msg.channel]["transmitted"][
                        control
                    ]["Pianoteq"]
                    display.show(
                        config["control_change"]["channel"][msg.channel]["transmitted"][
                            control
                        ]["Pianoteq"],
                        msg.value,
                    )

    exquis = Exquis()

    to_exquis = Outport(client_name, name="Exquis")
    to_upper = Outport(client_name, name="Upper")
    to_lower = Outport(client_name, name="Lower")
    to_pianoteq = Outport(client_name, name="Pianoteq")

    script = Script()

    from_exquis = Inport(script.exquis, client_name, name="Exquis")
    from_upper = Inport(script.upper, client_name, name="Upper")
    from_lower = Inport(script.lower, client_name, name="Lower")

    make_threads(
        [
            from_exquis.open,
            from_upper.open,
            from_lower.open,
            exquis.active_sensing,
            display.run,
        ]
    )
