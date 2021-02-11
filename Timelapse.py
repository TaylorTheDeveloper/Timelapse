# Backups video footage to the cloud
from os import listdir
from os.path import isfile, join
import os, uuid
import datetime
import calendar
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

scriptStartTime = datetime.datetime.utcnow()
###

# Local Path for blobs to upload
uploadsrcpath = "./capture/"

# Get month from time
time = datetime.datetime.now()
month = time.strftime("%B")
storageConnectionString = os.getenv('TimelapseAzureStorage')
cameraName = os.environ.get('TimelapseCameraName')
blobContainer = os.environ.get('TimelapseAzureBlobContainer')

if not cameraName:
	print("missing cameraName env variable")
	exit()

if not storageConnectionString:
	print("missing storageConnectionString env variable")
	exit()

if not blobContainer:
	container = "timelapse-"

if not os.path.isdir(uploadsrcpath):
	os.mkdir(uploadsrcpath)

container = (blobContainer + month).lower()

###

try:
	# Create the BlobServiceClient object
	blob_service_client = BlobServiceClient.from_connection_string(storageConnectionString)

except Exception as ex:
	print("Failed to initate script")
	print(ex)

###
scriptEndTime = datetime.datetime.utcnow()
runtime = scriptEndTime - scriptStartTime

print(f'Complete. Runtime: {runtime.total_seconds()}')