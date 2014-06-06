#!/bin/bash

# Monitor GPIO pin 23
echo "23" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio23/direction
echo "high" > /sys/class/gpio/gpio23/direction

# Wait for pin to go low
while [ true ]
do
if [ "$(cat /sys/class/gpio/gpio23/value)" == '0' ]
then
 gphoto2 --capture-tethered --hook-script="thumbs.py"
fi
done
