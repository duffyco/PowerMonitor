#!/bin/sh

cd /mnt/sdb1/power/
tail -n 6000 powerlog.txt > powerlog-hourly.txt
python $1
