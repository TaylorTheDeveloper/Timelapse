# Backups video footage to the cloud
from os import listdir
from os.path import isfile, join
import os, uuid
import datetime
import calendar
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

scriptStartTime = datetime.datetime.utcnow()
###

storageConnectionString = os.getenv('TimelapseAzureStorage')
cameraName = os.environ.get('TimelapseCameraName')

if not cameraName:
	print("missing cameraName env variable")
	exit()

if not storageConnectionString:
	print("missing storageConnectionString env variable")
	exit()

print(cameraName)

###
scriptEndTime = datetime.datetime.utcnow()
runtime = scriptEndTime - scriptStartTime

print(f'Complete. Runtime: {runtime.total_seconds()}')