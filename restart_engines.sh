#! /usr/bin/bash

systemctl stop pianoteq.service
#pgrep -f '/home/pi/Pianoteq 8 STAGE/arm-64bit/Pianoteq 8 STAGE' | xargs kill
#sleep 1
sudo -u 'pi' '/home/pi/Pianoteq 8 STAGE/arm-64bit/Pianoteq 8 STAGE' --headless &
systemctl stop tuneBfree_wrapper.service
pgrep -f '/home/pi/microtonOS/tuneBfree_wrapper.py' | xargs kill
#sleep 1
/home/pi/microtonOS/tuneBfree_wrapper.py &
pgrep -f '/home/pi/microtonOS/surge_xt_wrapper.py' | xargs kill
systemctl stop surge_xt_wrapper.service
#sleep 1
/home/pi/microtonOS/surge_xt_wrapper.py &
echo 'Engines restarted'

