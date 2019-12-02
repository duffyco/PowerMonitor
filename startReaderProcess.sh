#!/bin/sh

if [ -z `pgrep -f "python readPowerMeter.py"` ]
then
   echo "Restarting reader process...."
   mount -o bind /mnt/sdb1/opt /opt
   stty -F /dev/ttyACM0 raw
   cd /mnt/sdb1/power
   /mnt/sdb1/opt/bin/python readPowerMeter.py &
fi


