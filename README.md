# microtonOS
Making a xenharmonic synth out of a Raspberry Pi

## Hardware
- Yamaha Reface CP
- Yamaha Reface CP official power supply---12.0V, 0.7A, and 8.4W (included with Reface CP) 
- Intuitive Instruments Exquis
- Raspberry Pi 5 8GB RAM
- Raspberry Pi 5 official powersupply---5.1V, 5.0A/9.0V, 3.0A/12.0V, 2.25A, 15.0V 1.8A, and 27W
- Inno-Maker Pi 5 Aluminum Case (with integrated fan/heatsink)
- Geeekpi GPIO pin header extension
- HifiBerry ADC plus DAC
- USB-B to USB-A cable
- USB-c to USB-A cable (included with Exquis)
- Stereo RCA to 3.5mm TRS female cable
- 2 3.5 mm TRS male to 3.5 mm TRS male cables
- Headphones
- CME WiDi DIN-5

## Software
- Python 3
	- mido
	- mstsespy
	- rtmidi
	- signal
	- subprocess
	- sys
	- time
- Pianoteq 8 STAGE
- tuneBfree (remove msse flags when installing)
- Surge XT
- SonoBus
- Cadence
- Claudia
- jackd2
- Qjackctl
- MTS-ESP shared object (specific for Raspberry Pi, see mtsespy)
- Blueman
- librespot
- cargo
- Raspberry Pi OS (Bookworm) 64bit

## Installation
- Note that this installation has not been tested on multiple devices and is unlikely to work out of the box.
- Download the software above and install the software above.
- The username should be 'pi'.
- Install config files and systemd files with 'update_*.sh' scripts.

## Presets

### Tuning

**12edo.** Used in contemporary music. Limited use in classical Chinese music.

**24edo.** Used in contemporary arabic music.

**17edo.** Approximates classical Iranian music.

**29edo.** Approximates classical Arabic music.

**9ed3/2.** Wendy Carlos's Alpha Scale. Can also be used to approximate maqam Saba in Arabic music.

**19edo.** Approximates 1/3 meantone tuning used in classical European music from the 1600s.

**31edo.** Approximates 1/4 meantone tuning used in classical European music from the 1600s.

**13ed3.** Bohlen--Pierce Scale used in experimental music.

**7edo.** Used in Bantu music (e.g. in Zimbabwean music).

**5edo.** Used in Bantu music (e.g. in Ugandan music) and Indonesian classical music

**9edo.** Approximates Indonesian classical music.

**53edo.** Approximates Indian classical music. Also approximates Turkish music and music from the Western Sahel (e.g. Mali).

### Layouts

**Exquis.** Similar to Gerhard and harmonic table.

**Accordion B.**

**Accordion C.**

**Wicki-Hayden.** Used on some bandoneóns.

**Jazz.** Not in use elsewhere what I know of. Good for playing jazzy chords and shell voicings. Semi-isomorphic (i.e. you have to learn two shapes for each chord rather than 1).

## Mistakes
- Reface CP does allow microtuning but only monophonically, maybe I should have gotten a Korg Minilogue XD instead?
- Blokas Midihub was meant to retune the Reface CP and it can do this, but I should just have gone directly to buying a Raspberry Pi 5 instead.
- Raspberry Pi 4, I had a good deal for, but you really want the CPU of the 5.
