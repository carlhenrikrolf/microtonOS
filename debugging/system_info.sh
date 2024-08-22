#! /bin/bash
echo HOST
echo
echo hostname: $(hostname)
echo ip-address: $(hostname --ip-address)
echo all ip-adresses: $(hostname --all-ip-addresses)
echo
echo OS
echo 
cat /etc/os-release
echo
echo STORAGE
echo 
df -h
