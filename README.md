![Rig](resources/rig.jpeg)

# microtonOS

Making a xenharmonic synth out of a Raspberry Pi.
Most microtonal/xenharmonic products are geared towards music production---microtonOS is not.
microtonOS is a synthesiser meant for jamming.
You can jam by yourself and discover different music cultures as well as experimental approaches to harmony.
Or, you can use one of the many connectivity options on the Raspberry Pi to add additional instruments played by friends.
At first glance, microtonOS is ticking all the boxes.
It is a knob-per-function synthesiser with carefully selected presets.
Furthermore, it is screen-free, and, at its height, visual feedback is a somewhat culture-agnostic geometric representation of the tuning system.
The microtonOS code can be readily adapted to work with a minimum hardware requirement of 1 midi controller + 1 Linux computer.

## Components
**Intuitive Instruments Exquis.**
This is the main controller in my setup.

**Piano and organ style midi keyboards.**
I use a Yamaha Reface CP.

**Raspberry Pi.**
I use a Raspberry Pi 5 8GB RAM together with:
- Official powersupply (5.1V, 5.0A/9.0V, 3.0A/12.0V, 2.25A, 15.0V 1.8A, and 27W)
- Inno-Maker Raspberry Pi 5 Aluminum Case (with combined fan and heatsink)
- Geeekpi GPIO pin header extension
- HifiBerry ADC plus DAC soundcard
- 64GB Sandisk Pro Extreme SD card

**Cables and adapters.**
USB, TRS, and RCA adapters and cables are all necessary.
DIN-5 for midi can be useful.

**Software.**
The OS I use is Raspberry Pi OS 64bit Bookworm.
Python3 packages are included in `requirements.txt`.
Virtual instruments include:
- tuneBfree
- Modartt Pianoteq 8 STAGE
- Surge XT

Necessary KX Studio software is:
- Cadence
- Claudia

For connectivity I use:
- Blueman
- Sonobus

The MTS-ESP shared object is necessary for tuning.

## Installation
Burn the SD card with the Raspberry Pi OS.
Make sure the username is 'pi'.
Assemble the Raspberry Pi together with the case and soundcard.
Insert the SD card and pick appropriate settings for the OS.

From the default directory (`/home/pi`), clone the repository with
```bash
git clone --recurse-submodules git@github.com:carlhenrikrolf/microtonOS.git
```
If you forget the option, you can later add
```bash
git submodule update --init --recursive
```
In case you have your own fork, do not forget to set `git config --global user.name=<user name>`
and `git config --global user.email=<user email>`.

The following steps will be performed from withing the repository, so
```bash
cd microtonOS/
```

Install Python3 packages.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install . --use-pep517
```

To set up the HifiBerry soundcard, copy these configuration files.
```bash
sudo cp config/config.txt /boot/firmware/config.txt
sudo cp config/asound.conf /etc/
```
Note that `config.txt` will be overwritten.
Reboot for the changes to take effect.
When using an audio application a red LED should be lit on the HifiBerry soundcard.

Install MTS-ESP.
```bash
sudo apt install cmake
cmake -S third_party/mts-dylib-reference/ -B third_party/mts-dylib-reference
make --directory=third_party/mts-dylib-reference/
sudo cp third_party/mts-dylib-reference/libMTS.so /usr/local/lib/
```

Install system daemon scripts.
```bash
sudo cp config/systemd/<service file> /lib/systemd/system/
sudo systemctl enable <service file>
sudo systemctl start <service file>
```
`systemctl status`, `sudo systemctl stop`, `sudo systemctl restart`, and `sudo systemctl daemon-reload` are also useful commands.


Install tuneBfree.
tuneBfree is found under `third_party/`.
Follow the instruction in the README.
The exception is that you should should not add libjack-dev.
It should be libjack-jackd2-dev instead.

Download Pianoteq (from user area if you have a license).
Extract into `/home/pi/`; `/home/pi/Pianoteq <version>/` should be created.
To add `.ptq` files, go into `.local/share/Modartt/Addons` and add them there.

Install Surge, e.g. from [open build](https://software.opensuse.org//download.html?project=home%3Asurge-synth-team&package=surge-xt-release).
You may have to apply an apt fix install command.

Follow the [instructions](https://kx.studio/Repositories) to install KS Studio.
Then you should see more software in *Add / Remove Software*.
Add Cadence.
Make sure that Claudia and Cadence have been installed.
If Claudia is not installed, add it specifically.
In Cadence, in configure, set buffer size 128 and make sure there are 2 inputs and 2 outputs.
Make sure Hifiberry is input device and MIDI should be None.
Also, auto-start JACK or LADISH at login

Install Blueman (available in *Add / Remove Software* in the main menu)
and connect to any applicable Bluetooth midi devices or dongles.

Install Sonobus [for Debian](https://sonobus.net/linux.html).


## Isomorphic Layouts
I suggest to think of musically useful isomorphic layouts as belonging to one of four categories.
Each category depends on three parameters:
whether the layout is mirrored (flipped) in the left--right direction,
whether it is flipped in the up--down position,
and the value of the 'dilation'.
The dilation is notated $d$ and defined separately for each category below.
A suitable value is the size of the minor or neutral third.
For a more jazzy sound (or the Studio Ghibli sound), try the major third or perfect fourth.
Below, the layouts are named according to $d=3$.

**Exquis.**
$d=3$ is the Exquis default layout.
How the number of steps depend on d is shown by arrows.
Number of steps for $d=3$ is also given as an example in the centres of the hexagons.
$d=3$ plus left--right flip is the Gerhard layout used in Shiverware's Musix Pro.

![Exquis](resources/hexagonal_vs_rectangular.svg)

To the right, you can see a suggestion on how to map the hexagonal layout to a rectangular layout.
$d=5$.
This is the layout used on a bass guitar in standard tuning. 

**Harmonic table.**
$d=3$ is the harmonic table.
The harmonic table has been used in C-thru's AXiS controllers as well as in the Lumatone controller.
$d=2$ is the Park layout used in Shiverware's Musix Pro.

![Harmonic table](resources/harmonic_table.svg)

**Wicki--Hayden.**
$d=3$ is the Wicki--Hayden layout. For calculations, see below. The Wicki--Hayden layout is used in concertinas although it was originally designed for the bandoneón (popular in Argentine tango).
The bandoneón typically uses a non-isomorphic layout that is different between the left and right hands as well as whether the instrument is squeezed or dragged. Life is short so we will ignore such complex layouts.

![Wicki--Hayden](resources/wicki-hayden_tilted.svg)

Calculations. $f_3$ is defined by $f_3(d)=\mathrm{round}\frac{d}{3}$ if $d\mod 3 > 0$
else $f_3(d)= \max(i)$ such that $i\in\mathbf{N}$, $i\mod 2 > 0$, and $1 \leq i < \frac{d}{3})$.
$\mathrm{round}(x)$ rounds $x$ to the nearest integer and $x \mod y > 0$ if and only if $x$ is not divisible by $y$.
It is easiest to break this down into two cases.
If $d$ is not divisible by $3$, $f_3(d)$ is the integer nearest the fraction $d/3$.
Otherwise, it is the largest odd integer less than $d/3$.
For example, if you want to use $d=6$ for 24edo and you use $\mathrm{round}(d/3)$ instead (as in the first case), the layout will only use half of the tones and be equivalent to 12edo.

**Jankó.**
Bosanquet--Wilson layouts.
$d=3$ is the Jankó layout.
$d=4$ is the type C accordion layout.
Both $d=3$ and $d=4$ are given as examples below.
$d=4$ plus left--right flip corresponds to both the type B accordion layout and the dugmetara layout (popular in the Balkans).
$d=5, 6, 8,$ and $13$
correspond to the Lumatone presets for 19edo, both 22edo and 24edo, 31edo, and 53edo respectively. 

![Jankó](resources/janko_tilted.svg)

For large $d$, the 1D tuning invariant layouts, i.e., Exquis and the harmonic table,
benefit from a split keyboard as shown below (in respective order).
The filled hexagons represent a muted splitting line.
$+,0,-$ represent three consecutive steps
(note that $+,0,-$ does not indicate whether pitch is rising or falling).

![Splits](resources/splits.svg)

For the 2D tuning invariant layouts, i.e., Wicki--Hayden and Jankó,
even modest values for $d$ benefit from a split.
As these layouts are 'tilted' to fit the Exquis better,
so are their splitting lines.

![Slashes](resources/slashes.svg)


## Tunings
By default, the top note is concert A (440 Hz), but this can be changed according to step size.
Equally divided octave (also known as equal temperament) is abbreviated as edo.
Other intervals can alse be equally divided.
The tuning presets are assigned to four different classes:
(1) Default contains 12edo and white keys on the piano correspond to white lights on the Exquis.
(2) Microtonal contains equal-step tunings with a step size smaller than one semitone (100 cents).
White keys on the piano have red light, black keys have yellow light.
(3) Macrotonal contains equal-step tunings with a step size larger than one semitone.
White keys on the piano have green light, black keys have cyan light.
Only every other octave (or other period) is lit.
(4) Unequal contains tunings with non-equal step sizes.
White keys on the piano have magenta light, black keys have blue light.
If the step size is larger than one semitone, only every other period is lit.


<b>5edo (<font color="green">macro</font><font color="cyan">tonal</font>).</b>
Used in [Bantu traditional music](learn/bantu.md) (e.g. in Ugandan music) and [Indonesian classical music](learn/indonesian.md).

<b>7edo (<font color="green">macro</font><font color="cyan">tonal</font>).</b>
Used in [Bantu traditional music](learn/bantu.md) (e.g. in Zimbabwean music).

<b>13ed3 (<font color="green">macro</font><font color="cyan">tonal</font>).</b>
Bohlen--Pierce scale.
Used in experimental music.

<b>9edo (<font color="green">macro</font><font color="cyan">tonal</font>).</b>
Approximates [Indonesian classical music](learn/indonesian.md).

<b>Pythagorean (<font color="magenta">un</font><font color="blue">equal</font>).</b>
Ancient tuning that seems to have been discovered independently by different cultures.
Some intervals sound really consonant, but the problem is that others sound very dissonant.
That is the problem that equal step tunings solve.
See [just intonation](learn/just_intonation.md).

**12edo (default).** Used in contemporary music.
Was independently discovered in [Europe](learn/european.md) and [China](learn/east_asian.md).
Used in [American urban music](learn/american.md).
Used in [Romani traditional music](learn/romani.md).
Approximates [Ethiopian classical music](learn/ethiopian.md).


<b>9ed3/2 (<font color="red">micro</font><font color="yellow">tonal</font>).</b>
Wendy Carlos's Alpha Scale. Can also be used to approximate maqam saba in [Arabic music](learn/arabic.md).

<b>17edo (<font color="red">micro</font><font color="yellow">tonal</font>).</b>
Approximates [Iranian classical music](learn/iranian.md).

<b>9edo-ombak (<font color="magenta">un</font><font color="blue">equal</font>).</b>
An 18-note superset of 9edo.
When ascending every other note is 10 Hz lower than the next resulting in stretched octave.
Used in [Indonesian classical music](learn/indonesian.md) as an alternative to 9edo.

<b>19edo (<font color="red">micro</font><font color="yellow">tonal</font>).</b>
Approximates 1/3 meantone tuning used in [European classical music](learn/european.md) from the 1600s.
The minor and major third closely approximates their justly tuned counterparts, but the cost is that the fifth is not close to its justly tuned counterpart.

<b>Partial 48edo (<font color="magenta">un</font><font color="blue">equal</font>).</b>
A 19-note subset of 48edo.
Used in contemporary [Turkish music](learn/turkish.md).

<b>22edo (<font color="red">micro</font><font color="yellow">tonal</font>).</b>
Used in experimental music.

<b>Partial 53edo (<font color="magenta">un</font><font color="blue">equal</font>).</b>
A 22-note subset of 53edo.
Approximates [Indian classical music](learn/indian.md) well---in particular, its 22 shrutis.
Used in [Turkish classical music](learn/turkish.md).
After to 12edo, it is the tuning that can approximate the largest number of traditional musics including (apart from Indian and Turkish):
[West-Sahelian classical music](learn/west_sahelian.md) and
[East-Asian classical music](learn/east_asian.md).

<b>24edo (<font color="red">micro</font><font color="yellow">tonal</font>).</b>
Used in contemporary [Arabic music](learn/arabic.md).

<b>29edo (<font color="red">micro</font><font color="yellow">tonal</font>).</b>
Approximates [Arabic classical music](learn/arabic.md).

<b>31edo (<font color="red">micro</font><font color="yellow">tonal</font>).</b>
Approximates 1/4 meantone tuning used in [European classical music](learn/european.md) from the 1600s.
Closely approximates the harmonic seventh (the seventh harmonic in just intonation).
