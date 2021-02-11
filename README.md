# Timelapse
Timelapse camera system using azure.

Installation:

1. Install Python 3.x

2. Upgrade PIP and get dependant libraries

	- python -m pip install --upgrade pip
	- pip install azure-storage-blob


3. Create environment variables on your system:
*note if first time setup be sure to restart your terminal/shell after setting these*

	- TimelapseAzureStorage - (required) This should be your Azure Storage connection string
	- TimelapseAzureBlobContainer - (optional) This should be your Azure Blob container. Defaults to "timelapse-".
	- TimelapseUseDatesInPath - (optional) This should indicate weather or not you want files stored in the root of the storage container or in folders organized using YYYY/MM/DD pattern. Defaults to False.
	- TimelapseCameraName - (optional) The name of your camera. Defaults to "FooCam"
	- TimelapseCaptureSrcPath - (optional) The path where your images are saved. Defaults to "./capture/". Must end with "/"
