#!/bin/bash

# Monitor GPIO pin 23
# Reserve GPIO 23
echo "23" > /sys/class/gpio/export
# Set the input/output direction to input
echo "in" > /sys/class/gpio/gpio23/direction
# Set the starting value of the pin
echo "1" > /sys/class/gpio/gpio23/value

# Repeat for GPIO pin 22
echo "22" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio22/direction
echo "1" > /sys/class/gpio/gpio22/value

# Repeat for GPIO pin 21
echo "21" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio21/direction
echo "1" > /sys/class/gpio/gpio21/value

# Repeat for GPIO pin 18
echo "18" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio18/direction
echo "1" > /sys/class/gpio/gpio18/value

# Wait for pin to go low
while [ true ]
do
  if [ "$(cat /sys/class/gpio/gpio23/value)" == '0' ]
  then
  	echo "Button 1 pushed"
    gphoto2 --capture-tethered --hook-script="/home/pi/photostreamer-pi/thumbs.py"
  elif [ "$(cat /sys/class/gpio/gpio22/value)" == '0' ]
  then
	echo "Button 2 pushed"
  elif [ "$(cat /sys/class/gpio/gpio21/value)" == '0' ]
  then
	echo "Button 3 pushed"
  elif [ "$(cat /sys/class/gpio/gpio18/value)" == '0' ]
  then
	echo "Shutting down"
	halt &
	exit 0
  fi
  # Throttle it back a little and only poll every 1 second
  sleep 1
done