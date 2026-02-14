# Effects

There are many useable effects for Linux.
For a set of effects to get started install the following. [^patchstorage]
```bash
sudo apt install guitarix aida-x dragonfly-reverb calf-plugins shiro-plugins airwindows-lv2 tap-lv2 caps-lv2 mda-lv2
```
I strongly recommend the Calf Studio Gear plugins.
Dragonly and Shiro have some good reverbs.

There are also good effects at [x42](https://x42-plugins.com/x42/) (e.g. the rotary speaker) and [LSP](https://lsp-plug.in/index.php) (e.g. the impulse response reverb).
Once downloaded, copy to the appropriate location.
```bash
sudo cp -r <plugin>.lv2 /usr/lib/lv2
sudo cp -r <plugin>.clap /usr/lib/clap
sudo cp -r <plugin>.vst3 /usr/lib/vst3
```
There are other locations that could also be used, but it does not make much of a difference.
Do not add one plugin to multiple sources though.

[^patchstorage]: [Patchstorage LV2 plugins](https://patchstorage.com/platform/lv2-plugins/) is a collection of effects with a big overlap to these. Can be used for an overview.
