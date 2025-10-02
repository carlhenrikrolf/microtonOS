# OLED

Industria OLED for Argon One V5 uses the i2c interface.

Check if the i2c interface is in use by either
```bash
dmesg | grep i2c
```
or
```bash
lsmod | grep i2c
```
If nothing is listed, then i2c has to be enabled.
See the [Luma.OLED documentation](https://luma-oled.readthedocs.io/en/latest/hardware.html).

`microtonOS/config/firmware/context.txt` contains some optimisations.

Add permission and install ic2 tools.
```bash
sudo usermod -a -G i2c pi
sudo apt-get install i2c-tools
```
For the permissions to take hold log out and log in again.

Check the ic2 address
```bash
i2cdetect -y 1
```
It should be 3c for Industria OLED.

Python dependencies should be in `microtonOS/requirements.txt`
Other dependencies should be installed with
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
```

Add permissions
```bash
sudo usermod -a -G spi,gpio,i2c pi
```
where `pi` is the username.