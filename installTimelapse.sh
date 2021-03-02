#!/bin/bash

# Install software prerequisites
apt-get update
apt install -y python3-pip
apt install -y uuid-runtime
pip3 install azure-storage-blob

# Expose environment variables to cron job
env >> /etc/environment

# Setup cron jobs
crontab -l | grep -v '/root/Timelapse/'  | crontab -
crontab -e root &> /dev/null
(crontab -l ; echo "$TimelapseCameraFrequency /usr/bin/python3 /root/Timelapse/Timelapse.py > /root/cameralog.txt") | sort - | uniq - | crontab -
(crontab -l ; echo "$TimelapseCameraCloudUpdateFrequency /usr/bin/python3 /root/Timelapse/UpdateCheck.py > /root/updatechecklog.txt") | sort - | uniq - | crontab -
(crontab -l ; echo "@reboot /root/Timelapse/installTimelapse.sh > /root/bootlog.txt") | sort - | uniq - | crontab -


