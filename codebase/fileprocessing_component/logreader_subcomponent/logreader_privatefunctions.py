def extractflaskoutput(logentry, linecounter):
	outcome = {}
	outcome["lineindex"] = linecounter
	datetimestart = logentry.find("[")
	datetimeend = logentry.find("]")
	datetime = logentry[datetimeend - 8:datetimeend] + " - " + logentry[datetimestart + 1:datetimeend - 9]
	outcome["datetime"] = datetime.replace("/", " ")
	outcome["requestipaddress"] = "From " + logentry[:datetimestart - 4]
	rawdata = logentry[datetimeend + 3:]
	rawdata = rawdata.split(" ")
	outcome["method"] = rawdata[0]
	requestedpath = rawdata[1]
	outcome["path"] = requestedpath
	outcome["outcome"] = rawdata[3]
	if (rawdata[3] == "200") or (rawdata[3] == "304"):
		outcome["entrytype"] = "success"
	else:
		outcome["entrytype"] = "failure"
	return outcome



def extractdownloadmanageroutput(logentry, linecounter):
	outcome = {}
	outcome["lineindex"] = linecounter
	if logentry.find("[DOWNLOAD-MANAGER] > ") != -1:
		outcome["content"] = logentry[21:]
		outcome["entrytype"] = "invocation"
	else:
		outcome["content"] = logentry[19:]
		outcome["entrytype"] = "information"
	return outcome



def extractotheroutput(cache, linecounter):
	outcome = {}
	outcome["lineindex"] = linecounter
	startingline = cache[0]
	if startingline.find("] ERROR in app:") != -1:
		outcome["entrytype"] = "error"
	else:
		outcome["entrytype"] = "other"
	outcome["content"] = cache
	return outcome
	



def determineoutputtype(outputstring):

	outcome = "OTHER"
	if outputstring.find("HTTP/1.1") != -1:
		outcome = "FLASK"
	else:
		if outputstring.find("[DOWNLOAD-MANAGER] ") != -1:
			outcome = "DOWNLOAD-MANAGER"
	return outcome

