# Timelapse
Timelapse camera system using azure.

Installation:
This guide will help you set up your timelapse camera. Most steps have been automated.

Do note: 
If you want to configure wireless during setip, call 'setup.sh wifi'
If you already have internet access, just call 'setup.sh'

1. Log into pi
2. Copy files from usb or download them from git
3. If using usb, you can find the device path to mount using 'sudo fdisk -l'
3. If using usb, you can copy the files using 'sudo mount /dev/sdb1 /media; cp -r /media/Timelapse /root/'
4. If using internet, you can clone the repo using git. 
3. Ensure line endings are correct after cloning with sed: "sed -i -e 's/\r$//' Timelapse/*" 
3. Configure the setup script to include your required storage account settings, your wifi information, and optional configurations. 
4. Once you've set your intended values, run the './Timelapse/setup.sh' script to set up the pi device for Timelapse work.
5. Setup will enable all the pi features you need, set environment variables, and reboot the device
6. After reboot, enter sudo -i again
7. Then run './Timelapse/installTimelapse.sh' to get required software dependancies and install the Timelapse cron job on your system

Remarks:
My raspberry pi's usually come with EN_GB as the default keyboard layout. It's very difficult to enter '\' without first going through the raspi-config setup (which this automates). If you need to type '\' before running setup you can do so with by '(HOLD LEFT ALT) + NUM9 + NUM2'. If you don't have a numpad, this doesn't work. 

Environment variables were used in the setup. If you want to change the job frequency after setup has been complete, you will need to modify the root crontab.

Often I work cross platform. Line endings may need to be fixed before you run the software. This is easily done in linux from the root of the project directory with "sed -i -e 's/\r$//' *"


There are other ways to acomplish timelapses using raspistill. I specifically didn't want my timelapse to be a long running process and wanted to implement it more like an 'agent' that wakes up and takes a picture from time to time, as 99% of the time I don't need to take a picture. Eventually, I will connect this to Azure IoT Hub or similar offering so that I can remotley configure, manage, and view the camera's output. I'll share progress here.


LICENSE is GNU GPLv3

Environment Variables:
Required variables are set automatically for you. Other variables used by the software defined below. 

*note if first time setup be sure to restart your terminal/shell after setting these*

	- TimelapseAzureStorage - (required) This should be your Azure Storage connection string
	- TimelapseAzureBlobContainer - (optional) This should be your Azure Blob container. Defaults to "timelapse-".
	- TimelapseUseDatesInPath - (optional) This should indicate weather or not you want files stored in the root of the storage container or in folders organized using YYYY/MM/DD pattern. Defaults to False.
	- TimelapseCameraName - (optional) The name of your camera. Defaults to "FooCam".
	- TimelapseCaptureSrcPath - (optional) The path where your images are saved. Defaults to "./capture/". Must end with "/".
	- TimelapseCameraFrequency - (optional) The cron job frequency configuration"
