# IoT Timelapse Camera
IoT Timelapse camera system using azure.

# Installation:
This guide will help you set up your timelapse camera in a few minutes. 
You will need to attach either a usb or raspberry pi native camera do the device.
Most steps have been automated. Follow the below steps on the device you wish to make a timelapse camera.
After installTimelapse.sh is complete, the camera will automatically snap and save pictures to azure for your timelapses whenever it has a power source. 

Full local setup:  
`*Log in*`  
`passwd pi # optional but recommend changing password`  
`sudo -i`  
`mount /dev/sdb1 /media`  
`cp -r /media/Timelapse ~`  
`sed -i -e 's/\r$//' Timelapse/* # note (HOLD RIGHT ALT + "-") to get '\' if your model has en_GB keyboard layout.`  
`./Timelapse/setup.sh usewifi`  
`*Log in*`  
`sudo -i`  
`./Timelapse/installTimelapse.sh`  

Optionally if internet is already enabled on device:  
`*Log in*`  
`passwd pi # optional but recommend changing password`  
`sudo -i`  
`apt-get update`  
`apt-get install git -y`  
`git clone https://github.com/TaylorTheDeveloper/Timelapse`  
`sed -i -e 's/\r$//' Timelapse/* # note (HOLD RIGHT ALT + "-") to get '\' if your model has en_GB keyboard layout.`  
`./Timelapse/setup.sh`  
`*Log in*`  
`sudo -i`  
`./Timelapse/installTimelapse.sh`  

# Remarks:
Cron is your friend! Two things to know:
1) https://crontab.guru/ - great interactive tool for writing cron syntax.
2) This project uses cron as root user. This is because the job needs permissions to write image files to the file system during exectution. It took me a while to figure out both how to use environment variables during a cron job and how to install them properly ;). I installed variables to root's .bashrc file and they were not available to the env command until reboot so they are copied to the env file in the installTimelapse.sh script. I think this makes sense anyways, as they don't need to be their until you want to run the script as a cron job. After running setup, you can just run Timelapse.py anytime to snap a picture.

My raspberry pi's usually come with EN_GB as the default keyboard layout. It's very difficult to enter '\' without first going through the raspi-config setup (which this automates). If you need to type '\\' before running setup you can with `(HOLD RIGHT ALT + "-")` or using numpad `(HOLD RIGHT ALT) + press NUM9 + press NUM2`.

Environment variables were used in the setup. If you want to change the job frequency after setup has been complete, you will need to modify the root crontab. Use `sudo crontab -e`

Often I work cross platform. Line endings may need to be fixed before you run the software. This is easily done in linux from the root of the project directory with "sed -i -e 's/\r$//' *"

Password update has not been automated:
It's possible to do this but I don't recommend it: https://www.systutorials.com/changing-linux-users-password-in-one-command-line/
You must be aware that the full command line can be viewed by all users in the Linux system and the password in the command line can be potentially leased. Only for cases where this is okay, you may consider using the method here.[source](https://www.systutorials.com/changing-linux-users-password-in-one-command-line/)

There are other ways to acomplish timelapses using raspistill. I specifically didn't want my timelapse to be a long running process and wanted to implement it more like an 'agent' that wakes up and takes a picture from time to time, as 99% of the time I don't need to take a picture. Eventually, I will connect this to Azure IoT Hub or similar offering so that I can remotly configure, manage, and view the camera's output. I'll share progress here.

Environment Variables:
Required variables are set automatically for you. Other variables used by the software defined below. 

*note if first time setup be sure to restart your terminal/shell after setting these*

`TimelapseAzureStorage - (required) This should be your Azure Storage connection string`  
`TimelapseAzureBlobContainer - (optional) This should be your Azure Blob container. Defaults to "timelapse-".`  
`TimelapseUseDatesInPath - (optional) This should indicate weather or not you want files stored in the root of the storage container or in folders organized using YYYY/MM/DD pattern. Defaults to False.`  
`TimelapseCameraName - (optional) The name of your camera. Defaults to "timelapsecam".`  
`TimelapseCaptureSrcPath - (optional) The path where your images are saved. Defaults to "./capture/". Must end with "/".`  
`TimelapseCameraFrequency - (optional) The cron job frequency configuration"`  
