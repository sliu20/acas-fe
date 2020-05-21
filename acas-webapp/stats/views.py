from django.shortcuts import render


import speedtest
import subprocess
import re


st = speedtest.Speedtest()


# Function: execute(str)
# Description: Returns a string of the output of the executed command
def execute(command):
	command = command.split(' ')
	result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
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
			status[i] = (status[i][0], "active")
		else:
			status[i] = (status[i][0], "inactive")

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


# Function: statsView()
# Description: Returns the components for the statistics page
def statsView(request):
	command = 'sudo ovs-appctl bond/show bond0'
	commandResult = execute(command)
	uploadSpeedbps = getUploadSpeed()
	downloadSpeedbps = getDownloadSpeed()
	uploadSpeedMbps = convert2Mega(uploadSpeedbps)
	downloadSpeedMbps = convert2Mega(downloadSpeedbps)
	bondPortStatus = getBondPortStatus(commandResult)
	activeSlave = getActiveSlave(commandResult)

	context = {
		'uploadSpeedbps': "{:.0f}".format(uploadSpeedbps),
		'downloadSpeedbps': "{:.0f}".format(downloadSpeedbps),
		'uploadSpeedMbps': "{:.2f}".format(uploadSpeedMbps),
		'downloadSpeedMbps': "{:.2f}".format(downloadSpeedMbps),
		'commandResult': commandResult,
		'bondPortStatus': bondPortStatus,
		'activeSlave': activeSlave,
	}

	return render(request, "statistics.html", context)
