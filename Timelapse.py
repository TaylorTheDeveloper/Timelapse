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
	blobContainer = "timelapse-"

if not os.path.isdir(uploadsrcpath):
	os.mkdir(uploadsrcpath)

container_name = (blobContainer + month).lower()

def UploadData(srcFolder, destContainer ):
	# see: https://stackoverflow.com/questions/59170504/create-blob-container-in-azure-storage-if-it-is-not-exists
	try:
		blob_service_client = BlobServiceClient.from_connection_string(storageConnectionString)
		container_client = blob_service_client.get_container_client(destContainer)
		container_client.get_container_properties()
	except Exception as iex:
		print(iex)
		container_client = blob_service_client.create_container(destContainer)

	print("Pushing data to secure cloud storage: " + destContainer + "/" + cameraName + '\n')

	# Get all files in local path
	onlyfiles = [f for f in listdir(srcFolder) if isfile(join(srcFolder, f))]
	for fname in onlyfiles:
		print("\nUploading to Azure Storage as blob:\n\t" + srcFolder + fname)

		uploadSuccess = False
		# Create a blob client using the local file name as the name for the blob
		blob_client = blob_service_client.get_blob_client(container=destContainer, blob=cameraName + "/" +fname)

		# Upload the created file if it doesn't already exist
		# Delete on successful upload
		with open(join(srcFolder, fname), "rb") as data:
			try:
				uploadSuccess = True
				blob_client.upload_blob(data, overwrite=True)
			except Exception as nex:
				print(nex)

		if uploadSuccess:
			os.remove(join(srcFolder, fname))

def CaptureImage(srcFolder, time):
	try:
		cmd = f'raspistill -o ./capture/{time:%Y-%B-%d}-{time.timestamp()}.jpg -q 100 -t 1'
		print(cmd)
		os.system(cmd)
		print("picture captured")
	except Exception as ex:
		print("Failed to take capture")
		print(ex)

CaptureImage(uploadsrcpath, time)

UploadData(uploadsrcpath, container_name)

###
scriptEndTime = datetime.datetime.utcnow()
runtime = scriptEndTime - scriptStartTime

print(f'Complete. Runtime: {runtime.total_seconds()}')