# Linux Sound
Raspberry Pi runs on operating systems derived from Linux.
As Linux has been developed by many independent developers, several sound systems have been developed, e.g.
- Pipewire,
- JACK and a2jmidid (musical instruments)
- PulseAudio (music playback)
- ALSA (inputs and outputs)

Pipewire is a more recent sound system that is intended to unify and replace earlier systems.
However, many pieces of software and hardware were developed to interface with earlier systems, so it is still useful to know a thing or two about those.

ALSA is a system for reading MIDI and audio inputs from the soundcard, USB, analog inputs, bluetooth, etc.
Therefore all other systems build on top of ALSA.

PulseAudio is mainly developed for playback of recorded music.
As such, it has not been optimised for low-latency audio.
This becomes a problem when connecting instruments as they will make sound with noticeable delay since pressing a key.
Therefore, PulseAudio should not be used for making a Linux-based synth.
Indeed, it can be good to check whether any PulseAudio processes are running and, if so, uninstall them.
This applies also for bridges such as pipewire-pulse.
Before uninstalling anything, it can be good to check `sudo raspi-config` and advanced options > audio.
(If you see audio volume and mic volume at the top panel, this is not necessarily a good thing.
It means that some kind of PulseAudio is running.)

JACK has been optimised for low-latency with the purpose of using it with musical instruments.
An inportant feature of JACK is the *patchbay*.
A patchbay routes audio and midi between different pieces of software.
a2jmidid is a software for translating between ALSA and JACK.
ALSA assigns different numbers to different ports at each boot, so to ignore these numbers, it should be run as `a2jmidi -u`

JACK, however, lacks some of the music playback features of PulseAudio, such as using the Raspberry Pi as a bluetooth speaker.
Therefore, I bridge JACK and Pipewire.
This can be done by installing `pw-jack` and prefix JACK-based software with it, e.g. `pw-jack a2jmidi -u` or `pw-jack qjackctl`.
Qjackctl is a GUI for JACK.
(Many other GUIs are available, e.g. KX Studio, Raysession, Helvum, and qpwgraph, but Qjackctl is lightweight, versatile, and reliable.)
Apart from the bridge, Pipewire comes pre-installed on recent Raspberry Pi OSes.

___

Python modules for dealing with sound include
- mido and rtmidi
- mtsespy

mido and rtmidi can be used to process MIDI data.
mtsespy is for interfacing with the MTS-ESP shared object used for tuning.