def extractflaskoutput(logentry, linecounter, sublinecounter):
	outcome = {}
	outcome["lineindex"] = formlinecounter(linecounter, sublinecounter)

	if logentry.find("[pid: ") == 0:
		reducedlog = logentry[logentry.find("] ")+2:]
		datetime = reducedlog[reducedlog.find("[")+5:reducedlog.find("]")]
		datetime = datetime.split(" ")
		outcome["datetime"] = datetime[1] + " " + datetime[0] + " " + datetime[3] + " - " + datetime[2]
		outcome["requestipaddress"] = "From " + reducedlog[0:reducedlog.find("(")-1]
		rawdata = reducedlog[reducedlog.find("] ")+2:reducedlog.find("=>")]
		rawdata = rawdata.split(" ")
		outcome["method"] = rawdata[0]
		outcome["path"] = rawdata[1]
		resultstart = reducedlog.find("(HTTP")
		result = reducedlog[resultstart:]
		result = result.split(" ")
		result = result[1]
		result = result[:-1]
		outcome["outcome"] = result
		if (result == "200") or (result == "304"):
			outcome["entrytype"] = "success"
		else:
			outcome["entrytype"] = "failure"

	else:
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



def extractdownloadmanagerinstruction(logentry, linecounter, sublinecounter):
	outcome = {}
	outcome["lineindex"] = formlinecounter(linecounter, sublinecounter)
	outcome["entrytype"] = "invocation"
	content = logentry[21:]
	if content.find(" | ") == -1:
		outcome["instruction"] = content
		outcome["torrentid"] = ""
	else:
		splitcontent = content.split(" | ")
		outcome["instruction"] = splitcontent[0]
		outcome["torrentid"] = "(" + splitcontent[1] + ")"
	return outcome



def extractdownloadmanagerlog(logentry, linecounter, sublinecounter):
	outcome = {}
	outcome["lineindex"] = formlinecounter(linecounter, sublinecounter)
	outcome["entrytype"] = "information"
	logcontent = logentry[19:]
	if logcontent[:2] == "- ":
		outcome["content"] = logcontent[2:]
	else:
		outcome["content"] = logcontent
	return outcome



def extractotheroutput(cache, linecounter, sublinecounter):
	outcome = {}
	outcome["lineindex"] = formlinecounter(linecounter, sublinecounter)
	startingline = cache[0]
	if startingline.find("] ERROR in app:") != -1:
		outcome["entrytype"] = "error"
	else:
		outcome["entrytype"] = "other"
	outcome["content"] = cache
	return outcome
	



def determineoutputtype(outputstring, loggingmode):

	outcome = "OTHER"
	if outputstring == "--- RESTART SERVICE ---":
		outcome = "RESTART"
	elif outputstring.find("HTTP/1.1") != -1:
		outcome = "FLASK"
	else:
		if outputstring.find("[DOWNLOAD-MANAGER] ") != -1:
			if outputstring.find("[DOWNLOAD-MANAGER] > ") != -1:
				outcome = "DOWNLOAD-MANAGER-INSTRUCTION"
			else:
				if (loggingmode == True) or (outputstring.find("[DOWNLOAD-MANAGER] - ") == -1):
					outcome = "DOWNLOAD-MANAGER-LOG"
				else:
					outcome = "IGNORE"

	return outcome



def formlinecounter(linecounter, sublinecounter):

	if sublinecounter == 0:
		outcome = str(linecounter)
	else:
		outcome = "00000" + str(sublinecounter)
		outcome = str(linecounter) + "." + outcome[-2:]
	return outcome







