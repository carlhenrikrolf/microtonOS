#! /usr/bin/bash

systemctl stop pianoteq.service
'/home/pi/Pianoteq 8 STAGE/arm-64bit/Pianoteq 8 STAGE' --headless &
systemctl stop tuneBfree_wrapper.service
/home/pi/microtonOS/tuneBfree_wrapper.py &
systemctl stop surge_xt_wrapper.service
/home/pi/microtonOS/surge_xt_wrapper.py &

