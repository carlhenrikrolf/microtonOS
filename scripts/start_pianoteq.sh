#!/bin/bash

exec_path="/home/pi/Pianoteq 8 STAGE/arm-64bit/Pianoteq 8 STAGE"
base_args="--multicore max --do-not-block-screensaver --midimapping TouchOSC"

base_cmd=("${exec_path}" $base_args)

sudo cpufreq-set -r -g performance

if [ "$#" -eq 0 ] ; then
    # open directly
    sudo systemctl stop pianoteq
    "${base_cmd[@]}"
    sudo systemctl start pianoteq
else
    # run from systemctl
    "${base_cmd[@]}" "$@"
fi

sudo cpufreq-set -r -g ondemand
