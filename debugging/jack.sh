#! /usr/bin/bash
jackd -d alsa -d hw:sndrpihifiberry -r 48000 -p 128 -n 2 -i 2 -o 2 -X raw
