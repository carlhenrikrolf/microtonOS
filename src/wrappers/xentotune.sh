#! /usr/bin/bash

HEADLESS=true
CARLA="carla-jack-single"
CONFIG_PATH="/home/pi/microtonOS/config/"
THRU="thru.carxp"
XENTOTUNE="xentotune.carxp"
COMMAND="/usr/bin/pw-jack /home/pi/microtonOS/third_party/Carla/source/frontend/"$CARLA

if $HEADLESS
then OPTIONS="--no-gui"
else OPTIONS=""
fi

if $1
then ARGS=$CONFIG_PATH$XENTOTUNE
else ARGS=$CONFIG_PATH$THRU
fi

$COMMAND $ARGS $OPTIONS
