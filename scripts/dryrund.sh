#! /usr/bin/bash
sudo --user pi source /home/pi/microtonOS/.venv/bin/activate; DISPLAY=:0; XDG_RUNTIME_DIR="/run/user/1000"; /usr/bin/pw-jack $1
