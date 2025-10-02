# Software
The OS I use is Raspberry Pi OS 64bit Bookworm.
Python3 packages are included in [requirements.txt](requirements.txt).
Virtual instruments include:
- Modartt Pianoteq 8 STAGE
- tuneBfree
- Surge XT
- XentoTune

Background programs include:
- Carla (a host for audio plugins)
- Pipewire, Qjackctl, and a2jmidid (for routing MIDI and audio)
- Blueman (for MIDI bluetooth connectivity) and Sonobus (for network)
- MTS-ESP (for tuning)


## Installation
Burn the SD card with the Raspberry Pi OS.
Make sure the username is *pi*.
Assemble the Raspberry Pi together with the case and soundcard.
Insert the SD card and pick appropriate settings for the OS.
In particular, make sure to use *pipewire* in the audio settings (and not *pulseaudio*).
Install a number of dependencies through a pre-installed package manager.
Do this by opening a terminal and running:
```bash
sudo apt update
sudo apt install cmake python3-pyqt5.qtsvg python3-rdflib pyqt5-dev-tools libmagic-dev liblo-dev libasound2-dev libpulse-dev libx11-dev libxcursor-dev libxext-dev qtbase5-dev libfluidsynth-dev libjack-jackd2-dev libopengl-dev libglu1-mesa-dev libftgl-dev libwebp-dev xxd pipewire-jack pipewire-alsa qjackctl a2jmidid blueman
sudo apt purge pipewire-pulse pulseaudio
```


From the default directory (`/home/pi`), clone the repository with
```bash
git clone --recurse-submodules git@github.com:carlhenrikrolf/microtonOS.git
```
If you forget the option, you can later add
```bash
git submodule update --init --recursive
```

The following steps will be performed from withing the repository, so
```bash
cd microtonOS/
```

Install Python3 packages in a virtual environment.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install . --use-pep517
```
PyQt5 should already be installed as part of the OS. However, a copy within the virtual environment is necessary.
Note that PyQt5 may take a long time to make a copy within the virtual environment.[^pyqt5]
Use the following to finalise the copying:
```bash
cp -r /usr/lib/python3/dist-packages/PyQt5/* /home/pi/microtonOS/.venv/lib/python3*/site-packages/PyQt5 --no-clobber
```

[^pyqt5]: If it does not work, try installing it manually with `.venv/bin/pip3 install pyqt5 --config-settings --confirm-license= --verbose`.

Install MTS-ESP.
```bash
cmake -S third_party/mts-dylib-reference/ -B third_party/mts-dylib-reference
make --directory=third_party/mts-dylib-reference/
sudo cp third_party/mts-dylib-reference/libMTS.so /usr/local/lib/
```
A summary of different tuning standards in electronic music is available [here](learn/tuning_standards.md).

To set up the HifiBerry DAC+ADC soundcard, copy these configuration files.
```bash
sudo cp config/firmware/config.txt /boot/firmware/config.txt
sudo cp config/etc/asound.conf /etc/
```
Note that `config.txt` will be overwritten.
`config.txt.` additionally overclocks the CPU to 3000.
For other soundcard, the configurations would have to be different.
Reboot for the changes to take effect.
When using an audio application (e.g. Qjackctl below) a red LED should be lit on the HifiBerry soundcard.

Set up Pipewire/Wireplumber.
```bash
chmod 0700 /run/user/1000
wpctl status
```
Check that both default source (mic) and sink (audio out) are prepended by `*`s.
If not, note the id and use:
`wpctl set-default <id>`

Qjackctl is a tool for routing
Run `pw-jack qjackctl` to set it up for the soundcard.
For the HifiBerry DAC+ADC soundcard, the parameters should be
- Driver: ALSA
- ✅ Realtime
- Interface: sndrphihifiberry,0
- Sample Rate: 48000
- Frames/Period: 128
- Periods/Buffer: 2

The advanced settings should be
- Channels I/O: 2, 2

A summary of sound tools is available [here](learn/linux_sound.md).

To use MIDI over bluetooth, start blueman and search for devices.
(To pair a mac with the pi through bluetooth midi: 1. On Mac, advertise bluetooth midi with Audio Midi Setup or Surge XT. 2. On Raspberry Pi, search devices on blueman and trust the Mac. 3. On Raspberry Pi, connect to the Mac. 4. On both, approve the pairing.)
Bluetooth works great with MIDI but not always great with audio as it struggles with delays for example.
To send audio over the network, install [Sonobus](https://sonobus.net/linux.html).
At the time of writing, the following commands were sufficient:
```bash
echo "deb http://pkg.sonobus.net/apt stable main" | sudo tee /etc/apt/sources.list.d/sonobus.list
sudo wget -O /etc/apt/trusted.gpg.d/sonobus.gpg https://pkg.sonobus.net/apt/keyring.gpg
sudo apt update && sudo apt install sonobus
```
Sonobus can be installed on other devices running on Windows, MacOS, iOS, Linux, or Android.
Then audio can be transferred between those devices.
(As a bonus, you can [install Librespot](learn/librespot.md) to stream Spotify audio.)


Install [Carla](https://github.com/falkTX/Carla).
```bash
make --directory=third_party/Carla
make install --directory=third_party/Carla
```
Install [XentoTune](https://github.com/narenratan/xentotune).
```bash
cmake -S third_part/xentotune -B third_party/xentotune/build -DCMAKE_BUILD_TYPE=Release
cmake -S third_party/xentotune --build third_party/xentotune/build --config Release
sudo cp -rf third_party/xentotune/build/Xentotune.clap /lib/clap
```
[Set up XentoTune and Carla.](learn/xentotune.md)

Install [Surge XT](https://surge-synthesizer.github.io/), e.g. from [open build](https://software.opensuse.org//download.html?project=home%3Asurge-synth-team&package=surge-xt-release).
(You may have to apply an apt fix install command.)
At the time of writing, the you could install it with
```bash
echo 'deb http://download.opensuse.org/repositories/home:/surge-synth-team/Raspbian_12/ /' | sudo tee /etc/apt/sources.list.d/home:surge-synth-team.list
curl -fsSL https://download.opensuse.org/repositories/home:surge-synth-team/Raspbian_12/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_surge-synth-team.gpg > /dev/null
sudo apt update
sudo apt install surge-xt-release
```
[Set up Surge XT.](learn/surge_xt.md)


Install [tuneBfree](https://github.com/narenratan/tuneBfree).
```bash
make --directory=third_party/tuneBfree/
sudo cp -r third_party/tuneBfree/build/tuneBfree.lv2 /usr/lib/lv2
```
Note that the tuneBfree README suggests to install the dependency `libjack-dev`.
Do **not** do this.
It will remove `libjack-jackd2-dev` from before.
(It is possible to revert by `sudo apt install libjack-jackd2-dev qjackctl`.)
[Set up tuneBfree](learn/tuneBfree.md)


Download [Pianoteq](https://www.modartt.com/) (from the user area if you have a license).
Extract into `/home/pi/`; `/home/pi/Pianoteq <version>/` should be created.
(Extraction does not have to be there, it's a suggestion.)
Enter that directory and run
```bash
sudo cp arm-64bit/Pianoteq <version> /usr/bin
sudo cp -r arm-64bit/Pianoteq <version>.lv2 /usr/lib/lv2
```
To add `.ptq` files, go into `.local/share/Modartt/Addons` and add them there.
[Set up Pianoteq](learn/pianoteq.md)

Go back to `microtonOS/` and install the systemd scripts.
Each `.service` file makes sure a program is started automatically at boot.
```bash
sudo cp config/systemd/<service file> /lib/systemd/system/
sudo systemctl enable <service file>
sudo systemctl start <service file>
```
A shortcut is to use `sudo dev/daemon_reload.sh`.
[More background on systemd.](learn/systemd.md)

[Develop microtonOS further.](learn/developing.md)
If you want to.