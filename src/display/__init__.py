# available devices
from .industria_oled import Display as OledDisplay


class Display:
    def __init__(self):
        self.oled_display = OledDisplay()

    def show(self, name=None, value=None, flipside=None, **kwargs):
        self.oled_display.show(name, value, flipside)

    def run(self):
        self.oled_display.run()
