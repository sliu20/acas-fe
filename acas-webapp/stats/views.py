from django.shortcuts import render


import speedtest
import subprocess
import re


st = speedtest.Speedtest()


# Function: execute(str)
# Description: Returns a string of the output of the executed command
def execute(command):
	command = command.split(' ')
	output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	result = output.stdout.decode('utf-8')
	if len(result) == 0:
		result = output.stderr.decode('utf-8')
	return result


# Function: getUpload():
# Description: Returns a float of the upload bandwidth (bps)
def getUploadSpeed():
	return st.upload()


# Function: getDownload():
# Description: Returns a float of the download bandwidth (bps)
def getDownloadSpeed():
	return st.download()


# Function: convert2Mega(float)
# Description: Returns a float of the number given converted with the metric prefix Mega
def convert2Mega(x):
	return x / (10**6)


# Function: getBondPortStatus(str)
# Description: Returns a list of tuples for the ports used and the status of each port in the bond
def getBondPortStatus(bondCommandOutput):
	status = re.findall(r"\nslave (.*): (.*)\n", bondCommandOutput)

	if len(status) == 0:
		return None

	for i in range(len(status)):
		if status[i][1] == "enabled":
			status[i] = (status[i][0], "available")
		else:
			status[i] = (status[i][0], "unavailable")

	return status


# Function: getActiveSlave(str)
# Description: Returns a list of the active slave port in the bond
def getActiveSlave(bondCommandOutput):
	active = re.findall(r"\nslave (.*): enabled\s+active slave\n", bondCommandOutput)
	if len(active) == 0:
		active = None
	else:
		active = active[0]

	return active


# Function: getConfigureActiveSlave(str, str)
# Description: Returns a string of the success message of the configuration of the active slave
def getConfigureActiveSlaveMessage(configureCommandOutput, port):
	message = re.findall(r"(.*)\n", configureCommandOutput)
	message = message[0]

	if message == "done":
		message = "Success: The active slave is now " + port + "."
	elif message == "no change":
		message = "Warning: Port " + port + " is already the active slave."
	elif message == "no such slave":
		message = "Error: There was no such port " + port + " used in the bond. Please select an available port that is used in the bond."
	elif message == "cannot make disabled slave active":
		message = "Error: Port " + port + " is unavailable. Please select an available port."
	else:
		message = "Error: Something went wrong. Try again or contact system admin to resolve persisting issues."

	return message


# GLOBAL VARIABLES
uploadSpeedbps = None
downloadSpeedbps = None
uploadSpeedMbps = None
downloadSpeedMbps = None
bondPortStatus = None
activeSlave = None
configureActiveSlaveMessage = None


# Function: statsView()
# Description: Returns the components for the statistics page
def statsView(request):
	global uploadSpeedbps
	global downloadSpeedbps
	global uploadSpeedMbps
	global downloadSpeedMbps
	global bondPortStatus
	global activeSlave
	global configureActiveSlaveMessage

	configureActiveSlaveMessage = None

	if request.POST.get("run_speed_test"):
		upload = getUploadSpeed()
		download = getDownloadSpeed()
		uploadSpeedbps = "{:.0f}".format(upload)
		downloadSpeedbps = "{:.0f}".format(download)
		uploadSpeedMbps = "{:.2f}".format(convert2Mega(upload))
		downloadSpeedMbps = "{:.2f}".format(convert2Mega(download))
	elif request.POST.get("get_ovs_information"):
		command = "sudo ovs-appctl bond/show bond0"
		commandResult = execute(command)
		bondPortStatus = getBondPortStatus(commandResult)
		activeSlave = getActiveSlave(commandResult)
	elif request.POST.get("configure_active_slave"):
		port = request.POST.get("port")
		command = "sudo ovs-appctl bond/set-active-slave bond0 " + port
		commandResult = execute(command)
		configureActiveSlaveMessage = getConfigureActiveSlaveMessage(commandResult, port)

	context = {
		'uploadSpeedbps': uploadSpeedbps,
		'downloadSpeedbps': downloadSpeedbps,
		'uploadSpeedMbps': uploadSpeedMbps,
		'downloadSpeedMbps': downloadSpeedMbps,
		'bondPortStatus': bondPortStatus,
		'activeSlave': activeSlave,
		'configureActiveSlaveMessage': configureActiveSlaveMessage,
	}

	return render(request, "statistics.html", context)
