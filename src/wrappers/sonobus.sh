#! /usr/bin/bash

HEADLESS=true
GROUP="microtonOS"
USERNAME="pi"
CONFIG_FILE="setup.sonobus"
CONFIG_PATH="/home/pi/microtonOS/config/"
COMMAND="/usr/bin/pw-jack /usr/bin/sonobus"

if $HEADLESS
then OPTIONS="--headless"
else OPTIONS=""
fi

sleep 5
$COMMAND "--group="$GROUP "--username="$USERNAME "--load-setup="$CONFIG_PATH$CONFIG_FILE $OPTIONS
