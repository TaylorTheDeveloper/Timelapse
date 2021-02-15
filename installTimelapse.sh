#!/bin/bash

# Install software prerequisites
apt-get update
#apt-get upgrade -y
apt install -y python3-pip
pip3 install azure-storage-blob

# Set cron job (warning this will also clear your crontab of other jobs update '>' to '>>' to append)
echo "$frequency /usr/bin/python3 /home/pi/Timelapse/Timelapse.py > /home/pi/out.txt" > /var/spool/cron/crontabs/pi