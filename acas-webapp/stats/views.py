from django.shortcuts import render


import speedtest
import subprocess


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


# Function: statsView()
# Description: Returns the components for the statistics page
def statsView(request):
	command = 'ls'
	commandResult = execute(command)
	uploadSpeedbps = getUploadSpeed()
	downloadSpeedbps = getDownloadSpeed()
	uploadSpeedMbps = convert2Mega(uploadSpeedbps)
	downloadSpeedMbps = convert2Mega(downloadSpeedbps)

	context = {
		'uploadSpeedbps': "{:.0f}".format(uploadSpeedbps),
		'downloadSpeedbps': "{:.0f}".format(downloadSpeedbps),
		'uploadSpeedMbps': "{:.2f}".format(uploadSpeedMbps),
		'downloadSpeedMbps': "{:.2f}".format(downloadSpeedMbps),
		'commandResult': commandResult,
	}

	return render(request, "statistics.html", context)
