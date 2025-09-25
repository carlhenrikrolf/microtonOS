# external libraries
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
import time
from gpiozero import Button

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)

button = Button(4)

class Display:
    def __init__(
        self,
        refresh_rate=0.03,
        typeface="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 
        wait_time=1,
        scroll_speed=2,
    ):
        self.refresh_rate = refresh_rate
        self.typeface = typeface
        self.scroll_speed = scroll_speed
        self.wait_time = wait_time
        self.name_font = ImageFont.truetype(typeface, 22)
        self.value_font = ImageFont.truetype(typeface, 18)
        self.flipside_font = ImageFont.truetype(typeface, 20)
        self.display_width = device.width
        self.x = 0
        self.is_on = False
        self.value = None
        self.start_time = None
        self.flipside = ""
        self.is_flipped = False
        self.flipped_is_on = False
        self.was_pressed = False
        self.flip_time = None

    def show(self, name=None, value=None, flipside=None):
        if name is not None:
            self.start_time = time.time()
            self.x = 0
            self.name = name
            self.value = "" if value is None else str(value)
            bbox = self.name_font.getbbox(name)
            self.name_width = bbox[2] - bbox[0]
            self.name_height = bbox[3] - bbox[1]
            self.is_on = True
        if flipside is not None:
            self.flip_time = time.time()
            self.flipside = str(flipside)
            self.flipped_is_on = True

    def run(self):
        while True:
            if self.is_flipped:
                if self.flipped_is_on:
                    current_time = time.time()
                    with canvas(device) as draw:
                        if current_time - self.flip_time >= self.wait_time:
                            self.flipped_is_on = False
                        draw.text(
                            (64, 32),
                            self.flipside,
                            fill="white",
                            font=self.flipside_font,
                            anchor="mm",
                        )
                else:
                    with canvas(device) as draw:
                        pass

            else:
                if self.is_on:
                    with canvas(device) as draw:
                        # draw name
                        draw.text(
                            (self.x, 0), self.name, fill="white", font=self.name_font
                        )

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
            current_time = time.time()
            if current_time - self.start_time >= self.wait_time:
                self.x -= self.scroll_speed
                if (
                    self.x < -self.name_width
                ):  # Reset when text is completely off screen
                    self.is_on = False
            time.sleep(self.refresh_rate)
            if button.is_pressed:
                if not self.was_pressed:
                    self.is_flipped = not self.is_flipped
                    self.was_pressed = True
            else:
                self.was_pressed = False
