# Channels

## Input
Channel 0 is default.
Channels 1 to 7 have notes raised by 1 to 7 steps respectively
channels 0 to 7 have keyswitches
channels 8 to 15 have notes lowered by 15 - (8 to 15) steps respectively
channels 8 to 15 shift the mapping
for uneven, 0=1=...=7 and 8=9=...=15.


## Internal

| id | function | zone |
|----|----------|------|
| 0 | master | lower |
| 1 | synth 1 | lower |
| 2 to 11 | mpe | lower |
| 12 | synth 1 alt. | special purpose |
| 13 | synth 2 alt. | special purpose |
| 14 | synth 2 | upper |
| 15 | master | upper |

"Special purpose" means that the channels are tuned differently than the MPE channels.
In particular, they are tuned such that no remapping of midi notes is necessary.

