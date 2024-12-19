# Tuning Standards

|    | polyphony | midi | dynamic
|----|-----------|------|--------
| pitchbend | no | yes | yes
| midi polyphonic expression (MPE) | 15 | yes | yes
| general midi (GM1, GM2) | 14–15 | yes | yes
| multitimbral (not guaranteed!) | 16 | yes | yes
| midi tuning standard (MTS) | 127–12x16 | yes (sysex) | both dynamic and static
| midi tuning standard extraperipheral sensing (MTS-ESP) | 127--127x16 | no (shared object for Linux/Mac/Windows) | both dynamic and static
| Scala files (.scl + .kbm) | limited by other components | no (Linux/Mac/Windows file) | no
| tuning file (.tun) | limited by other components | no (Linux/Mac/Windows file) | no
| midi 2.0 | per note | backwards-compatible | yes
