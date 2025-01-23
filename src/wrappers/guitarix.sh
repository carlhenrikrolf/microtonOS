#! /usr/bin/bash

HEADLESS=true

COMMAND="/usr/bin/pw-jack /usr/bin/guitarix"
ARGS="--bank=D:2 --auto-save"
if $HEADLESS
then OPTIONS="--nogui"
else OPTIONS=""
fi

$COMMAND $ARGS $OPTIONS
