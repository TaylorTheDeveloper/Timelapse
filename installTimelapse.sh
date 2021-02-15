#!/bin/bash

# Install software prerequisites
apt-get update
apt install -y python3-pip
pip3 install azure-storage-blob

# Setup cron job
(crontab -l ; echo "$TimelapseCameraFrequency /usr/bin/python3 /home/pi/Timelapse/Timelapse.py > /root/out.txt") | sort - | uniq - | crontab -


