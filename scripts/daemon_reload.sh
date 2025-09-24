#! /usr/bin/bash
s="/home/pi/microtonOS/config/systemd/"
t="/lib/systemd/system/"
for d in $(ls $s); do
systemctl stop $d
systemctl disable $d
cp $s$d $t
systemctl enable $d
done
for d in $(ls $s); do
systemctl start $d
done