#! /usr/bin/bash
grep --recursive --before-context=1 --after-context=1 "ERROR" .error_logs/
grep --recursive --before-context=1 --after-context=1 "failed" .error_logs/
