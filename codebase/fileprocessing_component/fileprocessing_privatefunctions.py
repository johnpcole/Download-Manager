def getflaskoutput(logentry, linecounter):
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
	if requestedpath[:8] == "/static/":
		outcome["importance"] = "minor"
	else:
		outcome["importance"] = "major"
	outcome["outcome"] = rawdata[3]
	if (rawdata[3] == "200") or (rawdata[3] == "304"):
		outcome["entrytype"] = "success"
	else:
		outcome["entrytype"] = "failure"
	return outcome

def getdownloadmanageroutput(logentry, linecounter):
	outcome = {}
	outcome["lineindex"] = linecounter
	outcome["entrytype"] = "information"
	outcome["content"] = logentry[19:]
	outcome["importance"] = "minor"
	return outcome

def getotheroutput(cache, linecounter):
	outcome = {}
	outcome["lineindex"] = linecounter
	outcome["entrytype"] = "other"
	outcome["content"] = cache
	outcome["importance"] = "major"
	return outcome