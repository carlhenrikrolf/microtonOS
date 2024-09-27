#! /usr/bin/bash

systemctl stop tuneBfree_wrapper.service
pgrep -f '/home/pi/microtonOS/tuneBfree_wrapper.py' | xargs --no-run-if-empty kill
/home/pi/microtonOS/tuneBfree_wrapper.py &
pgrep -f '/home/pi/microtonOS/surge_xt_wrapper.py' | xargs --no-run-if-empty kill
systemctl stop surge_xt_wrapper.service
/home/pi/microtonOS/surge_xt_wrapper.py &
systemctl stop pianoteq.service
pgrep -f '/home/pi/microtonOS/start_pianoteq.sh' | xargs --no-run-if-empty kill
pgrep -f '/home/pi/Pianoteq 8 STAGE/arm-64bit/Pianoteq 8 STAGE' | xargs --no-run-if-empty kill
sudo --user 'pi' '/home/pi/microtonOS/start_pianoteq.sh' --headless &

echo 'Engines restarted'

