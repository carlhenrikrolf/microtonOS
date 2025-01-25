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

while (( $(wpctl status | grep "Pianoteq" --count) < 1 ))
do sleep 1
done
$COMMAND "--group="$GROUP "--username="$USERNAME "--load-setup="$CONFIG_PATH$CONFIG_FILE $OPTIONS
