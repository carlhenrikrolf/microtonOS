# available devices
from .osc import Display as OscDisplay
from .industria_oled import Display as OledDisplay

# libraries
from utils import make_threads


class Display:
    def __init__(self):
        self.osc_display = OscDisplay()
        self.oled_display = OledDisplay()

    def show(self, name=None, value=None, flipside=None, **kwargs):
        self.osc_display.show(name, value, flipside)
        self.oled_display.show(name, value, flipside, **kwargs)

    def run(self):
        make_threads(
            [
                self.osc_display.run,
                self.oled_display.run,
            ]
        )
