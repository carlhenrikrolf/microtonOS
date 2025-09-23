# Developing microtonOS Further

> [!warning]
> No need to do any of this.
> These are notes on future work that can also be helpful personal customisation.

**Git setup.**
- `git config --global user.name=<user name>`
- `git config --global user.email=<user email>`
- `ssh-keygen`, follow instructions, and copy-paste `.pub` contents to Github.

**Linux utils.**
Package managers:
```bash
sudo apt install pacman-package-manager

wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash

sudo apt install flatpak
sudo flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```
Then reboot. More info at [Pi-Apps](https://pi-apps.io/install/) and [Flatpak](https://flathub.org/setup/Raspberry%20Pi%20OS).

Miscellaneous:
```bash
sudo apt install code
```

## Music software
```bash
sudo apt install qpwgraph hydrogen
```

**Exquis**
Needs to be v1.2.0, the newer v2.1.0 cannot both do microtonal music and mpe at the same time.
[for mac](https://web.archive.org/web/20250505203214/https://dualo.com/download/15603)
[for windows](https://web.archive.org/web/20250505203358/https://dualo.com/download/15609)

**Aeolus**

```bash
git clone --recurse-submodules https://github.com/Archie3d/aeolus_plugin.git
cd aeolus_plugin/
git checkout develop
cmake .
make
```

Start with
```bash
pw-jack Aeolus_artefacts/Standalone/Aeolus
```
Tuning works.
Settings are saved on shutdown.
Not clear how to choose presets (Tried creating `~/Documents/Aeolus`)

**Decent Sampler**
Download the ARM64 build from [Decent Sameples](https://www.decentsamples.com/product/decent-sampler-plugin/).
Extract the content and move into the extracted directory.
```bash
sudo cp DecentSampler /usr/bin/
sudo cp -r DecentSampler.vst3 /usr/lib/vst3
```
Cannot load tunings dynamically but accepts mpe.

Samples can be loaded into
```bash
cp -r <sample library> /home/pi/.config/Sample\ Libraries/
```

**Open Stage Control**
To run **Open Stage Control**, you need [nodejs](https://nodejs.org/en/download)

```bash
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash

# in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
nvm install 22

# Verify the Node.js version:
node -v # Should print "v22.14.0".
nvm current # Should print "v22.14.0".

# Verify npm version:
npm -v # Should print "10.9.2".
```
run with
```bash
node /path/to/open_stage_control
```

**Rippler X**

Download from git, enter the directory and run

```bash
# linux
sudo apt update
sudo apt-get install libx11-dev libfreetype-dev libfontconfig1-dev libasound2-dev libxrandr-dev libxinerama-dev libxcursor-dev
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -S . -B ./build
cmake --build ./build --config Release
```

Move the LV2 and VST3 plugins:

```bash
sudo cp -r build/RipplerX_artefacts/Release/LV2/RipplerX.lv2 /usr/lib/lv2/
sudo cp -r build/RipplerX_artefacts/Release/VST3/RipplerX.vst3 /usr/lib/vst3/
```

**Dexed**

Available in software downloader, but that one does not support microtuning.

[install instructions](https://github.com/asb2m10/dexed?tab=readme-ov-file)

[dependencies](https://github.com/asb2m10/dexed/wiki/Linux-build-dependencies)

```bash
sudo apt install libx11-dev libcurl4-gnutls-dev libfreetype6-dev libasound2-dev libxinerama-dev libjack-jackd2-dev libxcursor-dev libxrandr-dev
git clone https://github.com/asb2m10/dexed.git --recurse-submodules
cd dexed/
mkdir build
cd build
cmake .. -DJUCE_COPY_PLUGIN_AFTER_BUILD=TRUE
cmake --build .
```

**Surge XT**
```bash
git clone https://github.com/surge-synthesizer/surge.git
cd surge
```

```bash
git submodule update --init --recursive
cmake -Bbuild
cmake --build build --config Release --target surge-staged-assets
```

**Carla**

```bash
cd Carla
make
```

The following command will build the apps in `/usr/bin/`, `/usr/lib` etc.
```bash
sudo make install PREFIX=/usr
```
(It uses sudo and leaves out DESTDIR.)

**SonoBus**

```bash
git clone https://github.com/sonosaurus/sonobus.git --recurse-submodules
cd sonobus
```

```bash
cd linux
./deb_get_prereqs.sh
./build.sh
```