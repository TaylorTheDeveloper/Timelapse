import os
import datetime
from Utilities import CaptureImage, UploadData

time = datetime.datetime.now()
month = time.strftime("%B")
cameraName = os.environ.get('TimelapseCameraName')
blobContainer = os.environ.get('TimelapseAzureBlobContainer')
storageConnectionString = os.getenv('TimelapseAzureStorage')
captureSrcPath =  os.getenv('TimelapseCaptureSrcPath')

if not cameraName:
	print("missing cameraName env variable")
	exit()

if not storageConnectionString:
	print("missing storageConnectionString env variable")
	exit()

if not blobContainer:
	blobContainer = "timelapse-"

if not captureSrcPath:
	captureSrcPath = "./capture/"

if not os.path.isdir(captureSrcPath):
	os.mkdir(captureSrcPath)

container_name = (blobContainer + month).lower()

CaptureImage(captureSrcPath, time)

UploadData(cameraName, captureSrcPath, container_name, storageConnectionString)