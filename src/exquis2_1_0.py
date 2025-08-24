# external libraries
import time

# internal libraries
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq
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

    class Exquis:
        ack_rate = 0.3  # seconds

        def __init__(self):
            self.ack = 0.0
            self.page = self.start_page

            # start page
            self.routing = [True, True, True, True]

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
                colors = [black] * 128
                for led, on in zip(xq.encoder_knob, self.routing):
                    colors[led] = white if on else red
                led_colors = xq.set_led_colors(colors)
                to_exquis.send(led_colors)
                display.show("")
            elif xq.is_pressed(msg, xq.encoder_button[0]):
                self.routing[0] = not self.routing[0]
                set_gain(level=1.0, muted=not self.routing[0])
                self.page()
                display.show("mic", value="on" if self.routing[0] else "off")
            elif xq.is_pressed(msg, xq.encoder_button[1]):
                self.routing[1] = not self.routing[1]
                self.page()
                display.show("MIDI", value="receive" if self.routing[1] else "bypass")
            elif xq.is_pressed(msg, xq.encoder_button[2]):
                self.routing[2] = not self.routing[2]
                self.page()
                display.show(
                    "lower manual", value="global" if self.routing[2] else "local"
                )
            elif xq.is_pressed(msg, xq.encoder_button[3]):
                self.routing[3] = not self.routing[3]
                self.page()
                display.show(
                    "upper manual", value="global" if self.routing[3] else "local"
                )
            elif xq.is_pressed(msg, xq.sound):
                self.page = self.instrument_page
                self.page()

        def instrument_page(self, msg=None):
            if msg is None:
                developer_mode = xq.developer_mode("enter")
                to_exquis.send(developer_mode)
                colors = [black] * 128
                colors[xq.sound] = red
                for led, bank in enumerate(config["microtonOS"]["engine"][0]["bank"]):
                    colors[led] = red
                led_colors = xq.set_led_colors(colors)
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
            if exquis.routing[3]:
                to_lower.send(msg)
                if exquis.routing[1]:
                    to_pianoteq.send(msg)
                    self.show_cc(msg)

        def lower(self, msg):
            if exquis.routing[2]:
                to_upper.send(msg)
                if exquis.routing[1]:
                    to_pianoteq.send(msg)
                    self.show_cc(msg)

        def show_cc(self, msg):
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
