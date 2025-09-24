# Pianoteq

**This is a placeholder for Pianoteq, which is not opensource.
Download from [www.modartt.com/try](www.modartt.com/try) or [www.modartt.com/buy](www.modartt.com/buy).
Original README is attached below.**

# Pianoteq for Linux : notes and advices.

## Supported architectures:

Pianoteq for Linux as available as a standalone application, vst plugin and lv2, for two
architectures:

 * x86-64bit : for 64-bit Intel or AMD x86 processors.
 * arm-32bit : for ARM processors, 32-bit mode (see the notes below).
 * arm-64bit : for ARM processors, 64-bit mode (see the notes below).

(If you do not see these subfolders "x86-64bit", "arm-64bit" and "arm-32bit", make sure you extract
the archive with "7z x" instead of "7z e")

## Audio configuration

Most well-known Linux distributions are installed with a default configuration that is not well
suited for low-latency audio. You will find tons of tutorials about this on the web. Here are a few
tips:

 * make sure your user account is allowed to request real-time scheduling. This is mandatory if you
   want a decent latency without tons of cracklings.

   In order to elevate your account priviledges w.r.t. real time scheduling, you will need to edit
   the /etc/security/limits.conf (as root or with sudo) file and add:

     @audio - rtprio 90
     @audio - nice -10
     @audio - memlock 500000

 You may want to tune the numerical values, but the most important is to grant realtime priviledges
 to your account. If your user account is not member of the "audio" group, either join it, or
 replace the "@audio" above by "@youruseraccount". After editing /etc/security/limits.conf, you must
 log out and log in again in order to have the changes applied.

 * you will probably want to turn off CPU frequency throttling when Pianoteq is running, especially
   if you CPU is not very powerful. You can use the "cpufreq-info" command-line program to checks
   its current settings. CPU throttling can be disabled by the command:

     sudo cpufreq-set -c 0 -g performance (disable on the first cpu core)
     sudo cpufreq-set -c 1 -g performance (disable on the second core)
     ... (repeat for each CPU core)

 * you can use Pianoteq as a Jack client ( http://jackaudio.org/ ). Jack is a low latency audio
   server that will allow you to route the audio output of Pianoteq into any other Jack-enabled
   application. Learn how to use the patchbay of qjackctl ( http://qjackctl.sourceforge.net ) in
   order to have your connections between Jack clients recalled automatically.

 * with Jack or Alsa, use buffer sizes that are multiple of 64, as Pianoteq prefers those
   sizes. With the Alsa driver, the latency is 3 times the buffer size (a buffer of 64 samples at
   44100Hz gives a latency of 4.3 ms).

 * On modern Linux distributions, the default ALSA output will probably be pulseaudio. You may use
   it to listen to MIDI files, but this is not suitable for realtime playing. In order to achieve
   the lowest latency possible, you will want to select the ALSA outputs whose name end with 'Direct
   hardware device without any conversion'.

 * if pulseaudio is grabbing your soundcard and prevents Pianoteq from using it, you can temporarily
   disable it while Pianoteq is running with this command: pasuspender -- ./Pianoteq


## Non-audio configuration

Pianoteq tries to follow freedesktop XDG guidelines. Its settings are saved in the file:

  ~/.config/Modartt/Pianoteq71.prefs

Its various data files (add-ons, presets, ..) are stored by default in

  ~/.local/share/Modartt/Pianoteq/

Pianoteq also accepts a few command line options for loading midi files and exporting to wav. You
can list them with ./Pianoteq --help


## Pianoteq as a VST2 plugin

Pianoteq also comes as a native linux VST -- this is the "Pianoteq 8.so" file. You can then load it
in linux hosts that handle native VSTs, such as Ardour, Reaper, Bitwig Studio, Renoise, Tracktion,
Carla,...


## Pianoteq as an LV2 plugin

The folder "Pianoteq 8.lv2" may be copied into your ~/.lv2/ folder if you want to use Pianoteq as an
lv2 instrument.

## Pianoteq on ARM boards such as the Raspberry Pi

Pianoteq is able to run (with some performance limitations) on ARM boards, such as for example the
Raspberry Pi 4. Due to the limited cpu power available, a lot of care has to be taken in order to
achieve low latency without pops and cracks:

  * the user account used to run Pianoteq *must* have real-time rights (see the tip above about
    /etc/security/limits.conf ).

  * the cpu frequency should be locked at its maximum frequency. On a Raspberry Pi 3, which max out
    at 1.2GHz, it is:

      sudo cpufreq-set -f 1200MHz

  * prefer using a 64-bit Linux distribution as the performance of Pianoteq will be better
    if it can take advantage of the higher number of registers available in 64-bit mode.

  * some drivers may interfere and cause cpu usage pikes which provoke pops and cracks: wifi
    drivers, ethernet drivers...

  * the boards which draw their power from a micro-usb cable require a good micro-usb cable in order
    to run reliably. See for example:

      https://www.cnx-software.com/2017/04/27/selecting-a-micro-usb-cable-to-power-development-boards-or-charge-phones/

  * as these boards are typically much less powerful than a modern PC or Mac, you may have to reduce
    the internal sample rate (in Pianoteq options / perf panel) to 29400 or 22050 Hz. Since most of
    these board have four core (or more), you may want to use the following option when starting
    Pianoteq:

      ./Pianoteq --multicore max

    This will cause Pianoteq to switch to a different multithreading strategy that allows it to use
    more aggressively the high number of cores of the CPU. However it requires that you do not run
    any other cpu-intensive application on your board.

  * more informations, such as user contributed guides for various ARM board, can be found on our
    forum:

      https://forum.modartt.com/ (search 'raspberry')

