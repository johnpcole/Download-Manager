import os as OperatingSystem
from . import logging_privatefunctions as Functions




# =========================================================================================
# Prints text to the console, with a prefix that allows the logging webpage to render the content nicely
# =========================================================================================

def printout(printtext):
	if isinstance(printtext, list):
		for itementry in printtext:
			printout(itementry)
	else:
		OperatingSystem.system('echo "[DOWNLOAD-MANAGER] ' + printtext + '"')



def printinvocation(instruction, torrentid):
	printtext = "> " + instruction
	if torrentid != "":
		printtext = printtext + " | " + torrentid
		#printtext = printtext + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<small>(" + torrentid + ")</small>"
	printout(printtext)



def printrawline(printtext):
	OperatingSystem.system('echo "' + printtext + '"')







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
			elif logtype == "RESTART":
				outcome.insert(0, {"lineindex": "-", "entrytype": "restart", "content": "Restarting Service"})

	if len(cache) > 0:
		linecounter = linecounter + 1
		outcome.insert(0, Functions.extractotheroutput(cache, linecounter))

	return outcome



