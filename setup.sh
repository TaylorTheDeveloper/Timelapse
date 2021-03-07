#!/bin/bash

# Configuration
ssid=""
passphrase=""
azureStorageConnectionString=""
frequency="*/1 * * * *"
cloudUpdateFrequency="*/5 * * * *"
cameraName="timelapsecam1"
locale=en_US.UTF-8
layout=us
enableSSH=0
enableCamera=0
wifiCountryCode=US
enableWifi=$1
countConnectionAttempts=0
maxCountConnectionAttempts=20

# Wifi setup
if [ ! -z $enableWifi ]
then
# Enable wifi country
raspi-config nonint do_wifi_country $wifiCountryCode &> /dev/null

# Set Wifi if pass any flag  to this script
echo -en "\nnetwork={\n\tssid=\"$ssid\"\n\tpsk=\"$passphrase\"\n}" >> /etc/wpa_supplicant/wpa_supplicant.conf
fi

while [ "$(hostname -I)" = "" ]; do
  countConnectionAttempts += 1
  if [ countConnectionAttempts -gt maxCountConnectionAttempts]
  then
  echo "\nNo network connection established";
  exit
  fi
  echo -e "\nWaiting for network connection..."
  sleep 1
done

echo "\nNetwork connection established";

# Set keyboard layout and locale
raspi-config nonint do_change_locale $locale &> /dev/null
raspi-config nonint do_configure_keyboard $layout &> /dev/null

# Enable SSH
raspi-config nonint do_ssh $enableSSH

# Enable camera
raspi-config nonint do_camera $enableCamera

# Set hostname from environment variable
raspi-config nonint do_hostname $cameraName

# Update and install pip, uuid runtime
apt-get update
apt install -y python3-pip
apt install -y uuid-runtime

# Set environment variables
echo -en "export TimelapseCameraName='$cameraName'\n" >> /root/.bashrc
echo -en "export TimelapseAzureStorage='$azureStorageConnectionString'\n" >> /root/.bashrc
echo -en "export TimelapseCameraFrequency='$frequency'\n" >> /root/.bashrc
echo -en "export TimelapseCameraCloudUpdateFrequency='$cloudUpdateFrequency'\n" >> /root/.bashrc

if [[ -z "$TimelapseCameraDeviceId" ]]
then
  uuid=$(uuidgen)
  echo -en "export TimelapseCameraDeviceId='$uuid'\n" >> /root/.bashrc
fi

# Kick off install on reboot
(crontab -l ; echo "@reboot /root/Timelapse/installTimelapse.sh > /root/bootlog.txt") | sort - | uniq - | crontab -

# Reboot
sync
reboot
