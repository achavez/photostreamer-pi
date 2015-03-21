#!/bin/bash

if [ "$(whoami)" != "root" ]; then
  echo "This script must be executed with sudo or as root."
  exit 1
fi

echo "---------------------------------------"
echo "Updating and installing system packages"
echo "---------------------------------------"
apt-get -y update
apt-get -y upgrade
apt-get -y install python-pip python-dev libjpeg-dev

echo "------------------"
echo "Installing gphoto2"
echo "------------------"
wget https://github.com/gonzalo/gphoto2-updater/releases/download/2.5.7/gphoto2-updater.sh
chmod +x gphoto2-updater.sh
./gphoto2-updater.sh
rm gphoto2-updater.sh

echo "-------------------------"
echo "Downloading Photostreamer"
echo "-------------------------"
git clone https://github.com/achavez/photostreamer-pi.git
chown -R pi:pi photostreamer

echo "------------------------------"
echo "Installing Python dependencies"
echo "------------------------------"
pip install -r photostreamer-pi/requirements.txt

echo "--------------------------"
echo "Creating blank config flie"
echo "--------------------------"
cp photostreamer-pi/config-sample.cfg photostreamer-pi/config.cfg

echo "--------------------"
echo "Setting up cron task"
echo "--------------------"
echo "* * * * * cd /home/pi/photostreamer-pi && python background.py"|crontab -u pi

echo "---------------------"
echo "Adding startup script"
echo "---------------------"
cp photostreamer-pi/photostreamer /etc/init.d/photostreamer
chmod 755 /etc/init.d/photostreamer
update-rc.d photostreamer defaults

echo ""
echo ""
echo "Installation complete. Fill out the config file then restart the Pi to begin streaming."