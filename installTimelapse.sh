#!/bin/bash

# Install software prerequisites
apt-get update
apt install -y python3-pip
pip3 install azure-storage-blob

# Setup cron job
crobtab -e root &> /dev/null
(crontab -l ; echo "$TimelapseCameraFrequency /usr/bin/python3 /root/Timelapse/Timelapse.py > /root/out.txt") | sort - | uniq - | crontab -


