import os
from os import listdir
from os.path import isfile, join
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

	print("Pushing data to secure cloud storage: " + destContainer + "/" + cameraName + '\n')

	onlyfiles = [f for f in listdir(srcFolder) if isfile(join(srcFolder, f))]
	for fname in onlyfiles:
		blobFileName = cameraName + "/" + fname

		if useDatesInPath:
			blobFileName = cameraName + "/"+ str(time.year) + "/"+ str(time.month) + "/"+ str(time.day) + "/" +fname
			
		print("\nUploading to Azure Storage as blob:\n\t" + srcFolder + fname)
		print("\nBlob path:\n" + blobFileName)
		uploadSuccess = False
		blob_client = blob_service_client.get_blob_client(container=destContainer, blob=blobFileName)

		with open(join(srcFolder, fname), "rb") as data:
			try:
				blob_client.upload_blob(data, overwrite=True)
				uploadSuccess = True
			except Exception as nex:
				print(nex)

		if uploadSuccess:
			os.remove(join(srcFolder, fname))

def CaptureImage(srcFolder, time):
	try:
		cmd = f'raspistill -o ./capture/{time:%Y-%B-%d}-{time.timestamp()}.jpg -q 100 -t 1'
		os.system(cmd)
		print(cmd)
	except Exception as ex:
		print("Failed to capture image")
		print(ex)