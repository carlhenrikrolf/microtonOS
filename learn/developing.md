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

**Music software.**
```bash
sudo apt install qpwgraph guitarix aeolus hydrogen
```



Build Sfizz:
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

