# external libraries
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import time

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)


class Display:
    def __init__(
        self,
        typeface="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        wait_time=1,
        scroll_speed=2,
    ):
        self.typeface = typeface
        self.scroll_speed = scroll_speed
        self.wait_time = wait_time
        self.name_font = ImageFont.truetype(typeface, 24)
        self.value_font = ImageFont.truetype(typeface, 18)
        self.display_width = device.width
        self.x = 0
        self.is_on = False
        self.value = None
        self.start_time = None

    def show(self, name, value=None):
        self.x = 0
        self.start_time = time.time()
        self.name = name
        self.value = "" if value is None else str(value)
        bbox = self.name_font.getbbox(name)
        self.name_width = bbox[2] - bbox[0]
        self.name_height = bbox[3] - bbox[1]
        self.is_on = True

    def run(self):
        while True:
            if self.is_on:
                with canvas(device) as draw:
                    # draw name
                    draw.text((self.x, 0), self.name, fill="white", font=self.name_font)
                    current_time = time.time()
                    if current_time - self.start_time >= self.wait_time:
                        self.x -= self.scroll_speed
                        if (
                            self.x < -self.name_width
                        ):  # Reset when text is completely off screen
                            self.is_on = False

                    # draw value
                    draw.text(
                        (64, 40),
                        self.value,
                        fill="white",
                        font=self.value_font,
                        anchor="mm",
                    )
            else:
                # Clear the display when text has scrolled off
                with canvas(device) as draw:
                    pass
            time.sleep(0.03)


# display = Display()
# display.show("sustain", "45")
# display.run()
