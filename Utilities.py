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

def CaptureImage(srcFolder, time, deviceId):
	try:
		config = GetDeviceCloudConfiguration(deviceId)
		print(config.deviceid)
		print(config.cameraname)

		options = '-q 100 --timeout 1 --nopreview '
		options += f'--sharpness {config.sharpness} '
		options += f'--contrast {config.contrast} '
		options += f'--brightness {config.brightness} '
		options += f'--saturation {config.saturation} '
		options += f'--ISO {config.ISO} '
		options += f'--exposure {config.exposure} '
		options += f'--flicker {config.flicker} '
		options += f'--awb {config.autowhitebalance} '

		outputfilename = f'-o {srcFolder}{time:%Y-%B-%d}-{time.timestamp()}.jpg '
		cmd = 'raspistill ' + outputfilename + options
		os.system(cmd)
		print(cmd)
	except Exception as ex:
		print("Failed to capture image")
		print(ex)

class Dict2Obj(object):
	def __init__(self, dictionary):
		for key in dictionary:
			setattr(self, key, dictionary[key])

	def __repr__(self):
		return "<dict2obj: %s="">" % self.__dict__

def GetDeviceCloudConfiguration(deviceId, srcFolder="./"):
	filename = join(srcFolder, f"deviceconfig-{deviceId}.json")
	configSettings = None
	with open(filename, "rb") as data:
		content = data.read().decode()
		configSettings = json.loads(content)

	return Dict2Obj(configSettings)

def InstallDeviceCloudConfiguration(deviceId, srcFolder="./"):
	config = GetDeviceCloudConfiguration(deviceId)
	updateHostname = False
	changesRequireRestart = False

	# Setting
	configLines = list()

	# Bashrc Update for Environment variables
	with open("/root/.bashrc", "rb") as data:
		configLines = data.readlines()

	for line in configLines:
		decoded = line.decode()
		if ("TimelapseCameraName" in decoded and not config.cameraname in decoded):				
			BashUpdate(configLines, line, decoded, "TimelapseCameraName", config.cameraname)
			changesRequireRestart = True
			updateHostname = True
		if ("TimelapseCameraFrequency" in decoded and not config.timelapsefrequency in decoded):				
			BashUpdate(configLines, line, decoded, "TimelapseCameraFrequency", config.timelapsefrequency)
			changesRequireRestart = True
		if ("TimelapseCameraCloudUpdateFrequency" in decoded and not config.cloudconfigupdatefrequency in decoded):				
			BashUpdate(configLines, line, decoded, "TimelapseCameraCloudUpdateFrequency", config.cloudconfigupdatefrequency)
			changesRequireRestart = True

	with open("/root/.bashrc", "wb") as bashrc:
		bashrc.writelines(configLines)

	# Update for environment file for cron job
	configLines = list()
	with open("/etc/environment", "rb") as data:
		configLines = data.readlines()

	for line in configLines:
		decoded = line.decode()
		if ("TimelapseCameraName" in decoded and not config.cameraname in decoded):				
			EnvUpdate(configLines, line, decoded, "TimelapseCameraName", config.cameraname)
			changesRequireRestart = True
			updateHostname = True
		if ("TimelapseCameraFrequency" in decoded and not config.timelapsefrequency in decoded):				
			EnvUpdate(configLines, line, decoded, "TimelapseCameraFrequency", config.timelapsefrequency)
			changesRequireRestart = True
		if ("TimelapseCameraCloudUpdateFrequency" in decoded and not config.cloudconfigupdatefrequency in decoded):				
			EnvUpdate(configLines, line, decoded, "TimelapseCameraCloudUpdateFrequency", config.cloudconfigupdatefrequency)
			changesRequireRestart = True

	with open("/etc/environment", "wb") as envfile:
		envfile.writelines(configLines)

	if updateHostname:
		hostcmd = "raspi-config nonint do_hostname " + config.cameraname
		os.system(hostcmd)
		changesRequireRestart = True

	if changesRequireRestart:
		# Note: 1) cronjobs will finish installing after reboot. 2) If running this from a cron job we need to access shutdown command with path.
		os.system("/sbin/shutdown -r now")

def BashUpdate(configLines, line, decoded, ckey, cvalue):
	if (ckey in decoded and not cvalue in decoded):
		try:
			idx = configLines.index(line)
			eqlidx = decoded.index("=")
			configLines[idx] = (decoded[:eqlidx + 1] + "\'" + cvalue +"\'\n").encode()
		except Exception:
			pass

def EnvUpdate(configLines, line, decoded, ckey, cvalue):
	if (ckey in decoded and not cvalue in decoded):
		try:
			idx = configLines.index(line)
			eqlidx = decoded.index("=")
			configLines[idx] = (decoded[:eqlidx + 1] + cvalue +"\n").encode()
		except Exception:
			pass


def SyncDeviceCloudConfiguration(metadataContainer, connectionString, deviceId, srcFolder="./"):
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
		print("Cloud configuration local file exists")
		return;

	# see: https://stackoverflow.com/questions/59170504/create-blob-container-in-azure-storage-if-it-is-not-exists
	try:
		blob_service_client = BlobServiceClient.from_connection_string(connectionString)
		container_client = blob_service_client.get_container_client(metadataContainer)
		container_client.get_container_properties()
	except Exception as iex:
		print(iex)
		container_client = blob_service_client.create_container(metadataContainer)

	try:
		blob_client = blob_service_client.get_blob_client(container=metadataContainer, blob=filename)

		# if config exists return
		if blob_client.exists():
			print("Cloud configuration exist on server... downloading")
			return;
	except Exception as iex:
		print(iex)

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
        self.timelapsefrequency = "*/1 * * * *"
        self.cloudconfigupdatefrequency = "*/5 * * * *"
        self.sharpness = 0 # -100 to 100
        self.contrast = 0 # -100 to 100
        self.brightness = 50 # 0 to 100
        self.saturation = 0 # -100 to 100
        self.ISO = 100 # 100 to 3200
        self.exposure = "auto" # off,auto,night,nightpreview,backlight,spotlight,sports,snow,beach,verylong,fixedfps,antishake,fireworks
        self.flicker = "auto" # off,auto,50hz,60hz
        self.autowhitebalance = "auto" # off,auto,sun,cloud,shade,tungsten,fluorescent,incandescent,flash,horizon,greyworld