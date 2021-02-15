#!/bin/bash

# Setting
ssid=""
passphrase=""
frequency="*/1 * * * *" #cron frequency
cameraName="timelapsecam"
locale=en_US.UTF-8
layout=us
enableSSH=0
enableCamera=0

# Install software prerequisites
apt-get update
apt install -y python3-pip
pip3 install azure-storage-blob

# Set keyboard layout and locale
raspi-config nonint do_change_locale $locale &> /dev/null
raspi-config nonint do_configure_keyboard $layout &> /dev/null

# Enable SSH
raspi-config nonint do_ssh $enableSSH

# Enable camera
raspi-config nonint do_camera $enableCamera

# Set hostname from environment variable
raspi-config nonint do_hostname $cameraName

# Enable wifi country
countryCode=US
raspi-config nonint do_wifi_country $countryCode &> /dev/null

# Set Wifi
echo -en "\nnetwork={\n\tssid=\"$ssid\"\n\tpsk=\"$passphrase\"\n}" >> /etc/wpa_supplicant/wpa_supplicant.conf

# Set cron job (warning this will also clear your crontab of other jobs update '>' to '>>' to append)
echo "$frequency /usr/bin/python3 /home/pi/Timelapse/Timelapse.py > /home/pi/out.txt" > /var/spool/cron/crontabs/root
echo "" > /var/spool/cron/crontabs/pi

# Reboot
sync
reboot
