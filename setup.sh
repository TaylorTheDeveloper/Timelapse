#!/bin/bash

# Configuration
ssid=""
passphrase=""
azureStorageConnectionString=""
frequency="*/1 * * * *"
cameraName="timelapsecam"
locale=en_US.UTF-8
layout=us
enableSSH=0
enableCamera=0
wifiCountryCode=US
enableWifi=$1

# Set keyboard layout and locale
raspi-config nonint do_change_locale $locale &> /dev/null
raspi-config nonint do_configure_keyboard $layout &> /dev/null

# Enable SSH
raspi-config nonint do_ssh $enableSSH

# Enable camera
raspi-config nonint do_camera $enableCamera

# Set hostname from environment variable
raspi-config nonint do_hostname $cameraName

# Wifi setup
if [ ! -z $enableWifi ]
then
# Enable wifi country
raspi-config nonint do_wifi_country $wifiCountryCode &> /dev/null

# Set Wifi if pass any flag  to this script
echo -en "\nnetwork={\n\tssid=\"$ssid\"\n\tpsk=\"$passphrase\"\n}" >> /etc/wpa_supplicant/wpa_supplicant.conf
fi

# Set environment variables
echo -en "export TimelapseCameraName='$cameraName'\n" >> /root/.bashrc
echo -en "export TimelapseAzureStorage='$azureStorageConnectionString'\n" >> /root/.bashrc
echo -en "export TimelapseCameraFrequency='$frequency'\n" >> /root/.bashrc

# Reboot
sync
reboot
