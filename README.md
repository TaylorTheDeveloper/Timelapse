# Timelapse
Timelapse camera system using azure.

Installation:

If your setting up a pi from scratch, use:

setup.sh

If you already have wifi/ethernet enabled, use:

setup-skipwifi.sh

1. Log into pi
2. Copy files from usb or download them from git
3. Ensure line endings are correct with "sed -i -e 's/\r$//' *" from the root project directory. 
4. Once you have the files, run the './setup-*.sh' script to set up the pi.
5. Setup will enable all the pi features you need, set environment variables, and reboot the device
6. After reboot, run './installTimelapse.sh' to get required software dependancies and install the Timelapse cron job

Remarks:
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
