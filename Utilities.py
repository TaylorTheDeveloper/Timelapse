import os
from os import listdir
from os.path import isfile, join
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def UploadData(cameraName, srcFolder, destContainer, connectionString, time, useDatesInPath):
	# see: https://stackoverflow.com/questions/59170504/create-blob-container-in-azure-storage-if-it-is-not-exists
	try:
		blob_service_client = BlobServiceClient.from_connection_string(connectionString)
		container_client = blob_service_client.get_container_client(destContainer)
		container_client.get_container_properties()
	except Exception as iex:
		print(iex)
		container_client = blob_service_client.create_container(destContainer)

	onlyfiles = [f for f in listdir(srcFolder) if isfile(join(srcFolder, f))]

	if len(onlyfiles) > 0:
		print(f"Pushing data to secure cloud storage: {destContainer}/{cameraName}\n")

	for fname in onlyfiles:
		uploadSuccess = False
		blobFileName = cameraName + "/" + fname

		if useDatesInPath:
			blobFileName = cameraName + "/"+ str(time.year) + "/"+ str(time.month) + "/"+ str(time.day) + "/" +fname

		with open(join(srcFolder, fname), "rb") as data:
			try:
				blob_client = blob_service_client.get_blob_client(container=destContainer, blob=blobFileName)
				blob_client.upload_blob(data, overwrite=True)
				uploadSuccess = True
			except Exception as nex:
				print(nex)

		if uploadSuccess:
			os.remove(join(srcFolder, fname))

def CaptureImage(srcFolder, time):
	try:
		cmd = f'raspistill -o {srcFolder}{time:%Y-%B-%d}-{time.timestamp()}.jpg -q 100 -t 1'
		os.system(cmd)
		print(cmd)
	except Exception as ex:
		print("Failed to capture image")
		print(ex)

def SetDeviceCloudConfiguration(metadataContainer, connectionString, deviceId, cameraName, srcFolder="./"):
	# see: https://stackoverflow.com/questions/59170504/create-blob-container-in-azure-storage-if-it-is-not-exists
	try:
		blob_service_client = BlobServiceClient.from_connection_string(connectionString)
		container_client = blob_service_client.get_container_client(metadataContainer)
		container_client.get_container_properties()
	except Exception as iex:
		print(iex)
		container_client = blob_service_client.create_container(metadataContainer)

	cameraConfig = CameraCloudConfiguration(deviceId, cameraName)

	configContent = json.dumps(cameraConfig.__dict__)

	filename = join(srcFolder, f"deviceconfig-{deviceId}.json")

	file = open(filename, "w")
	file.write(configContent)
	file.close()

	uploadSuccess = False

	with open(filename, "rb") as data:
		try:
			blob_client = blob_service_client.get_blob_client(container=metadataContainer, blob=filename)
			blob_client.upload_blob(data, overwrite=True)
			uploadSuccess = True
		except Exception as nex:
			print(nex)

	if uploadSuccess:
		print(f"Cloud configuration set: {deviceId}")
	else:
		print(f"Cloud configuration not uploaded: {deviceId}")

class CameraCloudConfiguration(object):
    def __init__(self, deviceId, cameraName):
        self.deviceid = deviceId
        self.cameraname = cameraName