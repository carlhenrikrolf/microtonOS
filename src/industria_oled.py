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

# run
text = "This is a long text that will scroll if it doesn't fit on the display."
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
bbox = font.getbbox(text)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
display_width = device.width

x = display_width  # Start from the right edge

while True:
    with canvas(device) as draw:
        if text_width > display_width:
            draw.text((x, 0), text, fill="white", font=font)
            x -= 2  # Speed of scrolling
            if x < -text_width:
                x = display_width
        else:
            draw.text((0, 0), text, fill="white", font=font)
    time.sleep(0.03)
