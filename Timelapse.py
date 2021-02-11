# Backups video footage to the cloud
from os import listdir
from os.path import isfile, join
import os, uuid
import datetime
import calendar
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

storageConnectionString = os.getenv('TimelapseAzureStorage')
cameraName = os.environ.get('TimelapseCameraName')

if not cameraName:
	print("missing cameraName env variable")
	exit()

if not storageConnectionString:
	print("missing storageConnectionString env variable")
	exit()

print(cameraName)