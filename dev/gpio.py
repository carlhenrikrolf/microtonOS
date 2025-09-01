# something seems wrong with the otermost trs.
# 23 is always active
# the innermost works as intended.
from gpiozero import Button
import time

gpio_is_active = [False] * 27
gpio_of_interest = [
    4,
    14,
    # 20,
    # 21,
    # 22,
    # 23,
]  # only 4 seems to be used by the oled as a button, maybe the uart is doing something??

button = [Button(pin) for pin in gpio_of_interest]


while True:
    for i, pin in enumerate(gpio_of_interest):
        if button[i].is_pressed and not gpio_is_active[pin]:
            gpio_is_active[pin] = True
            print(f"GPIO {pin} is active")
        elif not button[i].is_pressed and gpio_is_active[pin]:
            gpio_is_active[pin] = False
            print(f"GPIO {pin} is inactive")
    # small delay to avoid busy-waiting
    time.sleep(0.1)
