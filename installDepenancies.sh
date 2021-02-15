#!/bin/bash

# Install software prerequisites
apt-get update
#apt-get upgrade -y
apt install -y python3-pip
pip3 install azure-storage-blob