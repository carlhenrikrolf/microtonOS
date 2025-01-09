Install Helvum through flatpak.
Install [flatpack](https://flathub.org/setup/Raspberry%20Pi%20OS)
```bash
sudo apt install flatpak
sudo flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo reboot
```
Then:
```bash
flatpak install flathub org.pipewire.Helvum
```
To run:
```bash
flatpak run org.pipewire.Helvum
```
__

Install [Pi-Apps](https://pi-apps.io/install/):
```bash
wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash
```
Uninstall with `~/pi-apps/uninstall`.

Install Box64 from Pi-Apps to run Intel Linux applications.
(Install Box86 to run Windows applications.)
Run
```bash
sudo systemctl restart systemctl-binfmt
```
to run Box64 automatically when it is needed.
Otherwise prepending `box64` to the command should work.

As for DecentSampler, I get error that `libnghttp2.so.14` is a shared library that does not load correctly.
Using `box64 ./DecentSampler BOX64_NOPULSE=1 BOX64_LD_PRELOAD=libnghttp2.so.14` does not help.

___

Install sfizz from openbuild by running:
```bash
echo 'deb http://download.opensuse.org/repositories/home:/sfztools:/sfizz/Raspbian_12/ /' | sudo tee /etc/apt/sources.list.d/home:sfztools:sfizz.list
curl -fsSL https://download.opensuse.org/repositories/home:sfztools:sfizz/Raspbian_12/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/home_sfztools_sfizz.gpg > /dev/null
sudo apt update
sudo apt install sfizz
```
However, it is possible to use:
```bash
git clone https://github.com/sfztools/sfizz.git
cd sfizz
cmake .
make
cd library/bin/
```
Not clear how to microtune though.
