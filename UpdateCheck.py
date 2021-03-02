import os
import datetime
from Utilities import SetDeviceCloudConfiguration, SyncDeviceCloudConfiguration, InstallDeviceCloudConfiguration

time = datetime.datetime.now()
deviceId = os.environ.get('TimelapseCameraDeviceId')
cameraName = os.environ.get('TimelapseCameraName')
metaBlobContainer = 'timelapse-device-metadata'
storageConnectionString = os.getenv('TimelapseAzureStorage')

SetDeviceCloudConfiguration(metaBlobContainer, storageConnectionString, deviceId, cameraName)

SyncDeviceCloudConfiguration(metaBlobContainer, storageConnectionString, deviceId)

InstallDeviceCloudConfiguration(deviceId)