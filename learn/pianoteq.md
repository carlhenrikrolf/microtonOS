# Pianoteq

To set up Pianoteq, set `headless = False` in [src/wrappers/pianoteq.py](../src/wrappers/pianoteq.py).
Restart the wrapper script.
Suggested configuration files are in [config/Pianoteq](../config/Pianoteq/).
They can be copied to `/home/pi/.local/share/Modartt/Pianoteq`.

> [!tip]
> *Pianoteq 8 Standard* does have more extensive microtonal capabilities than the cheaper *Pianoteq 8 STAGE*. STAGE does work with the MTS-ESP, MTS, and MPE [tuning standards](tuning_standards.md). Standard additionally uses `.scl` and `.kbm` files. When using such files there is also an option called *full rebuild*. Full rebuild adjusts the piano model to the tuning, so that it sounds more natural. As of version 8, there is [no way](https://forum.modartt.com/viewtopic.php?id=11982) to dynamically switch between tunings using full rebuild. So for the time being, maybe spend those moneys on more instruments instead?