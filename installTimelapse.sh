#!/bin/bash

# Install software prerequisites
apt-get update
apt install -y python3-pip
apt install -y uuid-runtime
pip3 install azure-storage-blob

# Expose environment variables to cron job
env >> /etc/environment

# Setup cron job
crontab -e root &> /dev/null
(crontab -l ; echo "$TimelapseCameraFrequency /usr/bin/python3 /root/Timelapse/Timelapse.py > /root/out.txt") | sort - | uniq - | crontab -
(crontab -l ; echo "$TimelapseCameraCloudUpdateFrequency /usr/bin/python3 /root/Timelapse/UpdateCheck.py > /root/updatecheck.txt") | sort - | uniq - | crontab -


