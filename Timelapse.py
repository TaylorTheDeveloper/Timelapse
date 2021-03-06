import os
import datetime
from Utilities import CaptureImage, UploadData

time = datetime.datetime.now()
month = time.strftime("%B")
cameraName = os.environ.get('TimelapseCameraName')
blobContainer = os.environ.get('TimelapseAzureBlobContainer')
storageConnectionString = os.getenv('TimelapseAzureStorage')
captureSrcPath =  os.getenv('TimelapseCaptureSrcPath')
useDatesInPath =  os.getenv('TimelapseUseDatesInPath')
deviceId = os.environ.get('TimelapseCameraDeviceId')

if not storageConnectionString:
	print("missing storageConnectionString env variable")
	exit()

if not cameraName:
	cameraName = "FooCam"

if not blobContainer:
	blobContainer = "timelapse-"

if not captureSrcPath:
	captureSrcPath = "./capture/"

if not useDatesInPath:
	useDatesInPath = True

if not os.path.isdir(captureSrcPath):
	os.mkdir(captureSrcPath)

container_name = (blobContainer + month).lower()

CaptureImage(captureSrcPath, time, deviceId)

UploadData(cameraName, captureSrcPath, container_name, storageConnectionString, time, useDatesInPath)