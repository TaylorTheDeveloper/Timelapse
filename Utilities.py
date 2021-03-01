import os
from os import listdir
from os.path import isfile, join
import os.path
from os import path
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

def InstallDeviceCloudConfiguration(deviceId, srcFolder="./"):
	filename = join(srcFolder, f"deviceconfig-{deviceId}.json")
	changes = False

	with open(filename, "rb") as data:
		content = data.read().decode()
		print(content)
		configSettings = json.loads(content)

		# Setting
		print(configSettings["cameraname"])
		configLines = list()

		with open("/root/.bashrc", "rb") as data:
			configLines = data.readlines()

		for line in configLines:
			decoded = line.decode()
			if ("TimelapseCameraName" in decoded and not configSettings["cameraname"] in decoded):				
				print(decoded)
				idx = configLines.index(line)
				#decoded = configLines[idx].decode()
				eqlidx = decoded.index("=")
				configLines[idx] = (decoded[:eqlix + 1] + "\'" + configSettings["cameraname"] +"\'").encode()
				print(configLines[idx].decode())
				changes = True

		with open("/root/.bashrc", "wb") as bashrc:
			bashrc.writelines(configLines)

		if changes:
			os.system("reboot now")

def GetDeviceCloudConfiguration(metadataContainer, connectionString, deviceId, srcFolder="./"):
	# see: https://stackoverflow.com/questions/59170504/create-blob-container-in-azure-storage-if-it-is-not-exists
	try:
		blob_service_client = BlobServiceClient.from_connection_string(connectionString)
		container_client = blob_service_client.get_container_client(metadataContainer)
		container_client.get_container_properties()
	except Exception as iex:
		print(iex)
		container_client = blob_service_client.create_container(metadataContainer)

	filename = join(srcFolder, f"deviceconfig-{deviceId}.json")

	downloadSuccess = False

	try:
		blob_client = blob_service_client.get_blob_client(container=metadataContainer, blob=filename)
		with open(filename, "wb") as download_file:
			download_file.write(blob_client.download_blob().readall())

		downloadSuccess = True
	except Exception as nex:
		print(nex)

	if downloadSuccess:
		print(f"Cloud configuration synced: {deviceId}")
	else:
		print(f"Cloud configuration not synced: {deviceId}")

def SetDeviceCloudConfiguration(metadataContainer, connectionString, deviceId, cameraName, srcFolder="./"):	
	filename = join(srcFolder, f"deviceconfig-{deviceId}.json")

	# if config exists return
	if path.isfile(filename):
		print("Cloud configuration")
		return;

	print("No Cloud configuration exists")

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