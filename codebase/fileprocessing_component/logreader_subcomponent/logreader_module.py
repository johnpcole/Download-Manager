from . import logreader_privatefunctions as Functions



def processlog(loggingoutput, loggingmode):

	outcome = []
	linecounter = 0

	cache = []
	for logentry in loggingoutput:
		logtype = Functions.determineoutputtype(logentry, loggingmode)
		if logtype == "OTHER":
			cache.append(logentry)
		else:
			if len(cache) > 0:
				linecounter = linecounter + 1
				outcome.insert(0, Functions.extractotheroutput(cache, linecounter))
				cache = []
			if logtype == "DOWNLOAD-MANAGER-INSTRUCTION":
				linecounter = linecounter + 1
				outcome.insert(0, Functions.extractdownloadmanagerinstruction(logentry, linecounter))
			elif logtype == "DOWNLOAD-MANAGER-LOG":
				linecounter = linecounter + 1
				outcome.insert(0, Functions.extractdownloadmanagerlog(logentry, linecounter))
			elif logtype == "FLASK":
				linecounter = linecounter + 1
				outcome.insert(0, Functions.extractflaskoutput(logentry, linecounter))

	if len(cache) > 0:
		linecounter = linecounter + 1
		outcome.insert(0, Functions.extractotheroutput(cache, linecounter))

	return outcome



