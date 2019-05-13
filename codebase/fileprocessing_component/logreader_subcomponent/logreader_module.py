from . import logreader_privatefunctions as Functions

def processlog(loggingoutput):

	outcome = []
	linecounter = 0

	cache = []
	for logentry in loggingoutput:
		logtype = Functions.determineoutputtype(logentry)
		if logtype == "OTHER":
			cache.append(logentry)
		else:
			if len(cache) > 0:
				linecounter = linecounter + 1
				outcome.insert(0, Functions.extractotheroutput(cache, linecounter))
				cache = []
			linecounter = linecounter + 1
			if logtype == "DOWNLOAD-MANAGER":
				outcome.insert(0, Functions.extractdownloadmanageroutput(logentry, linecounter))
			else:
				outcome.insert(0, Functions.extractflaskoutput(logentry, linecounter))
	if len(cache) > 0:
		linecounter = linecounter + 1
		outcome.insert(0, Functions.extractotheroutput(cache, linecounter))

	return outcome



