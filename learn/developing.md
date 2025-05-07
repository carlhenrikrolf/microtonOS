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
````



**Build Sfizz**
```bash
cd ~
git clone https://github.com/sfztools/sfizz.git
cd sfizz
cmake .
make
```
Run Sfizz:
```bash
pw-jack ~/sfizz/library/bin/sfizz_jack
```

