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
I'm using a CME WIDI Master adapter for MIDI over bluetooth.
DIN-5 for midi can be useful.

**Software.**
The OS I use is Raspberry Pi OS 64bit Bookworm.
Python3 packages are included in [requirements.txt](requirements.txt).
Virtual instruments include:
- tuneBfree
- Modartt Pianoteq 8 STAGE
- Surge XT

Background programs include:
- Pipewire, Qjackctl, and a2jmidid (for routing MIDI and audio)
- Blueman (for MIDI bluetooth connectivity) and Sonobus (for network)
- MTS-ESP (for tuning)


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

To set up the HifiBerry DAC+ADC soundcard, copy these configuration files.
```bash
sudo cp config/firmware/config.txt /boot/firmware/config.txt
sudo cp config/etc/asound.conf /etc/
```
Note that `config.txt` will be overwritten.
`config.txt.` additionally overclocks the CPU to 3000.
For other soundcard, the configurations would have to be different.
Reboot for the changes to take effect.
When using an audio application a red LED should be lit on the HifiBerry soundcard.

Install tools for connecting audio.
```bash
sudo apt install pw-jack pw-alsa qjackctl a2jmidid blueman
```
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

To use MIDI over bluetooth, start blueman and search for devices.
To send audio over the network, install [Sonobus](https://sonobus.net/linux.html).
At the time of writing, the following commands were sufficient:
```bash
echo "deb http://pkg.sonobus.net/apt stable main" | sudo tee /etc/apt/sources.list.d/sonobus.list
sudo wget -O /etc/apt/trusted.gpg.d/sonobus.gpg https://pkg.sonobus.net/apt/keyring.gpg
sudo apt update && sudo apt install sonobus
```
A summary of sound tools is available [here](learn/linux_sound.md).

Install MTS-ESP.
```bash
sudo apt install cmake
cmake -S third_party/mts-dylib-reference/ -B third_party/mts-dylib-reference
make --directory=third_party/mts-dylib-reference/
sudo cp third_party/mts-dylib-reference/libMTS.so /usr/local/lib/
```
A summary of different tuning standards in electronic music is available [here](learn/tuning_standards.md).

Install systemd scripts.
```bash
sudo cp config/systemd/<service file> /lib/systemd/system/
sudo systemctl enable <service file>
sudo systemctl start <service file>
```
A shortcut is to use `sudo dev/daemon_reload.sh`.
You can get more background on systemd [here](learn/systemd.md).


Install tuneBfree.
tuneBfree is found under `third_party/`.
Follow the instruction in the [README](third_party/tuneBfree/).
The exception is that you should should not add libjack-dev.
It should be libjack-jackd2-dev instead, i.e.,
```bash
sudo apt install libjack-jackd2-dev libopengl-dev libglu1-mesa-dev libftgl-dev libwebp-dev xxd
make --directory=third_party/tuneBfree/
```

Install Surge, e.g. from [open build](https://software.opensuse.org//download.html?project=home%3Asurge-synth-team&package=surge-xt-release).
You may have to apply an apt fix install command.
At the time of writing, the you could install it with
```bash
echo 'deb http://download.opensuse.org/repositories/home:/surge-synth-team/Raspbian_12/ /' | sudo tee /etc/apt/sources.list.d/home:surge-synth-team.list
curl -fsSL https://download.opensuse.org/repositories/home:surge-synth-team/Raspbian_12/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_surge-synth-team.gpg > /dev/null
sudo apt update
sudo apt install surge-xt-release
```

Download Pianoteq (from user area if you have a license).
Extract into `/home/pi/`; `/home/pi/Pianoteq <version>/` should be created.
To add `.ptq` files, go into `.local/share/Modartt/Addons` and add them there.


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

DEFAULT ⚫⚫ **Exquis.**
$d=3$ is the Exquis default layout.
How the number of steps depend on d is shown by arrows.
Number of steps for $d=3$ is also given as an example in the centres of the hexagons.
$d=3$ plus left--right flip is the Gerhard layout used in Shiverware's Musix Pro.

![Exquis](resources/hexagonal_vs_rectangular.svg)

To the right, you can see a suggestion on how to map the hexagonal layout to a rectangular layout.
$d=5$.
This is the layout used on a bass guitar in standard tuning. 

⚫🔴 **Harmonic table.**
$d=3$ is the harmonic table.
The harmonic table has been used in C-thru's AXiS controllers as well as in the Lumatone controller.
$d=2$ is the Park layout used in Shiverware's Musix Pro.

![Harmonic table](resources/harmonic_table.svg)

⚫🟠 **Wicki--Hayden.**
$d=3$ is the Wicki--Hayden layout. For calculations, see below. The Wicki--Hayden layout is used in concertinas although it was originally designed for the bandoneón (popular in Argentine tango).
The bandoneón typically uses a non-isomorphic layout that is different between the left and right hands as well as whether the instrument is squeezed or dragged. Life is short so we will ignore such complex layouts.

![Wicki--Hayden](resources/wicki-hayden_tilted.svg)

<details>
<summary>
Calculations with $f_3$.
</summary>
$f_3$ is defined by $f_3(d)=\mathrm{round}\frac{d}{3}$ if $d\mod 3 > 0$
else $f_3(d)= \max(i)$ such that $i\in\mathbf{N}$, $i\mod 2 > 0$, and $1 \leq i < \frac{d}{3})$.
$\mathrm{round}(x)$ rounds $x$ to the nearest integer and $x \mod y > 0$ if and only if $x$ is not divisible by $y$.
It is easiest to break this down into two cases.
If $d$ is not divisible by $3$, $f_3(d)$ is the integer nearest the fraction $d/3$.
Otherwise, it is the largest odd integer less than $d/3$.
For example, if you want to use $d=6$ for 24edo and you use $\mathrm{round}(d/3)$ instead (as in the first case), the layout will only use half of the tones and be equivalent to 12edo.
</details>


⚫🟡 **Jankó.**
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

⚫⚫ **5edo (ombak).**
Approximates the sléndro scale in [Indonesian classical music](learn/indonesian.md).
Alternating pengumbang ang pengisep notes, with pengisep in 5edo and pengumbang 10Hz lower.
Mapped to black keys.
See also *15edo*.

⚫🔴 **13ed3 (octaveless).**
Also known as the equally tempered Bohlen–Pierce scale.
Used in experimental music.
Mapped to white keys.

⚫🟠 **43Hz steps (uneven).**
Uneven in terms of cents but even in terms of Hz.
Possibly used in [Ancient Andean music](learn/andean.md).
Mapped to black keys plus the D-key.

⚫🟡 **4ed3/2 (octaveless).**
Used in [Georgian classical music](learn/georgian.md).
Mapped to white keys.

⚫🟢 **9edo (ombak).**
Approximates the pélog scales in [Indonesian classical music](learn/indonesian.md).
Alternating pengumbang ang pengisep notes, with pengumbang in 9edo and pengisep 8Hz higher.
Common pélog scales are mapped to the black keys.
The B, C, E, and F-keys can be used as accidentals.

⚫🔵 **12edo (ombak).**
Approximates the pélog scales in [Balinese classical music](learn/indonesian.md).
Alternating pengumbang ang pengisep notes, with pengumbang 3Hz lower than 12edo and pengisep 3Hz higher.
Without ombak, it can also simulate an untuned piano.

___

DEFAULT ⚫🟣 **12edo.**
"Normal" tuning.
Approximates the perfect fifth well.
Was independently discovered in [China](learn/east_asian.md) and [Europe](learn/european.md).
From Europe, it influenced [Romani music](learn/romani.md) and [American music](learn/american.md).
It is good for approximating [Ethiopian secular music](learn/ethiopian.md), and is used to approximate most of the rest of the world's music despite not being optimal.
Indeed, most contemporary music is in 12edo.

⚫⚪ **Harmonics (uneven).**
On the white keys:
The harmonics produced by playing flageolets on a string—condensed into one octave.
You get a 7-note subset of the Carlos harmonic scale starting from the G-key.
On the black keys:
The pitches produced by pressing (stopping) the string at points where flageolets would be produced.
G is duplicated on Gb.

___

🔴⚫ **14edo.**
The 7-note subset approximates scales used by many cultures around the world such as in [Thai classical music](learn/thai.md), [Bantu traditional music](learn/bantu.md), for bala in [West-Sahelian classical music](learn/west_sahelian.md), and it was possibly used in [ancient Andean music](learn/andean.md).

🔴🔴 **15edo.**
The 5-note subset approximates scales used in [Bantu traditional music](learn/bantu.md) as well ezil scale in [Ethiopian Christian music](learn/ethiopian.md).
All the 15 notes are useful for salendro scales [Sundanese classical music](learn/indonesian.md).
See also *5edo (ombak)*.

🔴🟠 **16edo.**
Used to approximate pélog scales in [Sundanese classical music](learn/indonesian.md).

🔴🟡 **9ed3/2 (octaveless).**
Approximates the Carlos alpha scale (experimental music).
It completely misses the octave, but (or because of this) approximates maqam saba from [Arabic classical music](learn/arabic.md) very well.
The notes are mapped such that maqam saba can be played from D above middle C the same way as maqam saba would be played in other tunings.

🔴🟢 **17edo.**
Approximates [Burmese classical music](learn/burmese.md) and the salendro bedantara scale of [Sundanese classical music](learn/indonesian.md).
I approximate [Iranian classical music](learn/iranian.md) with 17edo.

<details>
<summary>
<i>Halberstadt mapping</i>.
</summary>
<table>
<tr>
<td bgcolor="red"></td><td bgcolor="darkorange"></td><td bgcolor="red"></td><td bgcolor="darkorange"></td><td bgcolor="red"></td><td bgcolor="red"></td><td bgcolor="darkorange"></td><td bgcolor="red"></td><td bgcolor="darkorange"></td><td bgcolor="red"></td><td bgcolor="darkorange"></td><td bgcolor="red"></td>
</tr><tr>
<td>0</td><td>1(2)</td><td>3</td><td>4</td><td>5(6)</td><td>7</td><td>8(9)</td><td>10</td><td>11(12)</td><td>13</td><td>14</td><td>15(16)</td>
</tr><tr>
<td>-1</td><td>0(1)</td><td>2</td><td>3</td><td>4(5)</td><td>6</td><td>7(8)</td><td>9</td><td>10(11)</td><td>12</td><td>13</td><td>14(15)</td>
</tr>
</table>
</details>

🔴🔵 **17-note Pythagorean (uneven).**
[Pythagorean tuning](learn/pythagorean.md) seems to have been developed independently in East Asia and the Middle East.
The 17 notes have historically been a foundation for [Iranian](learn/iranian.md), [Arabic](learn/arabic.md), and [Turkish](learn/turkish.md) music.
[Ancient greek music](learn/greek.md) used a 12-note subset, and so have [East-Asian classical music](learn/east_asian.md).

🔴🟣 **41edo (18-note subset).**
Approximates the perfect fifth *very* well.
Approximates [West-Sahelian classical music](learn/west_sahelian.md).
The black keys plus C and F (i.e. like a Db major scale) approximates 7edo used to play the bala.
The remaining keys can be used for various kora tunings.

🔴⚪ **19edo.**
Approximates 1/3 meantone tuning used in [European classical music](learn/european.md) from the 1600s.
In particular, it approximates the European major and, especially, minor thirds well.

🟠⚫ **48edo (19-note subset).**
A 19-note subset of 48edo.
Used in contemporary [Turkish music](learn/turkish.md).

🟠🔴 **8ed4/3 (octaveless).**
Approximates the Carlos beta scale (experimental music).
Can be useful for approximating jins hijaz in [Arabic](learn/arabic.md) and [Iranian classical music](learn/iranian.md).

🟠🟠 **22edo.**
Used in experimental music.
I, however, use an 11-note subset to approximate the ararai scale of [Ethiopian Christian music](learn/ethiopian.md).

🟠🟡 **53edo (22-note subset).**
Approximates the perfect fifth *very* well.
A 22-note subset of 53edo.
Approximates [Indian classical music](learn/indian.md) well—in particular, its [22 shrutis](learn/shruti.md).
Used in [Turkish classical music](learn/turkish.md).

🟠🟢 **24edo.**
Approximates the perfect fifth well.
Used in contemporary [Arabic](learn/arabic.md) and [Iranian](learn/iranian.md) music.
Approximates [Burmese classical music](learn/burmese.md).
Can be used for niche cases in [Greek](learn/greek.md), [Japanese](learn/east_asian.md) and [American](learn/american.md) music.

🟠🔵 **29edo.**
Approximates the perfect fifth well.
Approximates [Arabic classical music](learn/arabic.md).
I have approximated [Iranian classical music](learn/iranian.md) with 17edo, but 29edo would also have been a good choice.

🟠🟣 **31edo.**
Approximates 1/4 meantone tuning used in [European classical music](learn/european.md) from the 1600s.
Closely approximates the harmonic seventh (the seventh harmonic) used in some European music but completely lacking from 12edo.

🟠⚪ **20ed3/2 (octaveless).**
Approximates the Carlos gamma scale (experimental music).
Additionally, it can approximate the "minor" scale in [Georgian classical music](learn/georgian.md).