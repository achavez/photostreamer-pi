#/bin/sh

if [ "$(whoami)" != "root" ]; then
  echo "This script must be executed with sudo or as root."
  exit 1
fi

echo "---------------------------------------"
echo "Updating and installing system packages"
echo "---------------------------------------"
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install python-pip python-dev libjpeg-dev

echo "------------------"
echo "Installing gphoto2"
echo "------------------"
sudo wget https://github.com/gonzalo/gphoto2-updater/releases/download/2.5.7/gphoto2-updater.sh
sudo chmod +x gphoto2-updater.sh
sudo ./gphoto2-updater.sh
sudo rm gphoto2-updater.sh

echo "-------------------------"
echo "Downloading Photostreamer"
echo "-------------------------"
git clone https://github.com/achavez/photostreamer-pi.git

echo "------------------------------"
echo "Installing Python dependencies"
echo "------------------------------"
sudo pip install -r photostreamer-pi/requirements.txt

echo "--------------------------"
echo "Creating blank config flie"
echo "--------------------------"
cp photostreamer-pi/config-sample.cfg photostreamer-pi/config.cfg

echo "--------------------"
echo "Setting up cron task"
echo "--------------------"
echo "* * * * * cd /home/pi/photostreamer-pi && python background.py"|crontab

echo "---------------------"
echo "Adding startup script"
echo "---------------------"
wget https://gist.githubusercontent.com/achavez/62e213af5a3bf5693871/raw/d20e7669a6317d1847e1c11aea766da725514c92/photostreamer
sudo cp photostreamer /etc/init.d/photostreamer
sudo chmod 755 /etc/init.d/photostreamer
sudo update-rc.d photostreamer defaults

echo ""
echo ""
echo "Installation complete. Fill out the config file then restart the Pi to begin streaming."