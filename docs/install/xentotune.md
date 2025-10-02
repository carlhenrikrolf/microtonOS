# XentoTune

To edit XentoTune, set `headless = False` in [src/wrappers/xentotune.py](../src/wrappers/xentotune.py), and (re)start the wrapper.
Note that it alternates between an 'audio through' option and XentoTune with the former as default.
To change the order set `thru_on_init = False`.
Sugguested settings for are in [config/xentotune.carxp](../config/xentotune.carxp) and [config/thru.carxp](../config/thru.carxp).

[Patchstorage LV2 plugins](https://patchstorage.com/platform/lv2-plugins/) is a good collection of effects.
Once downloaded, copy to the appropriate location.
```bash
sudo cp -r <plugin>.lv2 /usr/lib/lv2
```
For a set of effects to get started install the following.
```bash
sudo apt install guitarix aida-x dragonfly-reverb calf-plugins shiro-plugins airwindows-lv2 tap-lv2 caps-lv2 mda-lv2
```
