# Qjackctl

To make connections in Qjackctl, select *Patchbay*.
Add clients from the menus.
- Sometimes clients change names. Usually a number is changed. It is possible to replace the number with `.*` to ignore it. Any regex command is accepted, so more target expressions such as `[0-9]*` can also be used.
- One or several *plugs* can be added. For MIDI, typically add one. For audio, add left and right.
- ALSA MIDI ports and JACK MIDI ports cannot be directly connected. That is why a2jmidid is needed to bridge the two frameworks.
- The *exclusive* option means that the client can only connect to one other client. Useful to avoid unwanted autamtic connections.
- The *forward* option allows you to select one client's in-connections and copy them to the one you are currently editing.
- If the clients have been added, conecctions can be edited even when said client is not connected or running.

There are other options for better visualising the connections.
I would suggest Catia.
(Raysession/Patchance is supposed to be good but I haven't managed to run it on Raspberry Pi.)
Install Catia as follows.
```bash
cd ~/Downloads
sudo apt-get update
sudo apt-get install apt-transport-https gpgv wget
wget https://launchpad.net/~kxstudio-debian/+archive/kxstudio/+files/kxstudio-repos_11.1.0_all.deb
sudo dpkg -i kxstudio-repos_11.1.0_all.deb
sudo apt update
sudo apt install catia
```
Better check https://kx.studio/Repositories as it may be subject to change.
Note that I do not recommend using the KXStudio tools for saving patchbays and automatically managing patchbays.
(The above package additionally includes Carla. However, use the repository `third_party/Carla` as the latter supports CLAP plugins.)