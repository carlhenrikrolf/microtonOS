# Soundcraft
Driver for the Soundcraft Notepad series for Linux.
Available from [PyPI](https://pypi.org/project/soundcraft-utils/).
Install system-wide:
```bash
deactivate
sudo apt install python3-gi
sudo pip install soundcraft-utils --break-system-packages
sudo apt-get install gir1.2-gudev-1.0
sudo soundcraft_dbus_service --setup
```

List:
```bash
soundcraft_ctl -l
```
Set routing
```bash
soundcraft_ctl -s <number>
```
The option `--no-dbus` is also available and requires `sudo`.
The `--no-dbus` option is recommended for a bugfree performance.
Both commands print the routing and if no device is connected they print a message saying so

When making a change and rebooting the Raspberry Pi or the Soundcraft Notebook,
the change is persistent in the listing option.
But that does not mean that it is persistent on the Notepad device.