import os
import datetime
from Utilities import SetDeviceCloudConfiguration,GetDeviceCloudConfiguration

time = datetime.datetime.now()
deviceId = os.environ.get('TimelapseCameraDeviceId')
cameraName = os.environ.get('TimelapseCameraName')
metaBlobContainer = 'timelapse-device-metadata'
storageConnectionString = os.getenv('TimelapseAzureStorage')

SetDeviceCloudConfiguration(metaBlobContainer, storageConnectionString, deviceId, cameraName)

GetDeviceCloudConfiguration(metaBlobContainer, storageConnectionString, deviceId)