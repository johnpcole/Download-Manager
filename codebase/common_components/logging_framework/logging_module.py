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
	sublinecounter = 0

	cache = []
	instructionset = []
	for logentry in loggingoutput:
		logtype = Functions.determineoutputtype(logentry, loggingmode)
		if logtype == "OTHER":
			cache.append(logentry)
		else:
			if len(cache) > 0:
				sublinecounter = sublinecounter + 1
				instructionset.append(Functions.extractotheroutput(cache, linecounter, sublinecounter))
				cache = []
			if logtype == "DOWNLOAD-MANAGER-INSTRUCTION":
				outcome = instructionset.copy()
				instructionset = []
				linecounter = linecounter + 1
				sublinecounter = 0
				instructionset.extend(outcome)
				instructionset.append(Functions.extractdownloadmanagerinstruction(logentry, linecounter, sublinecounter))
			elif logtype == "DOWNLOAD-MANAGER-LOG":
				sublinecounter = sublinecounter + 1
				instructionset.append(Functions.extractdownloadmanagerlog(logentry, linecounter, sublinecounter))
			elif logtype == "FLASK":
				sublinecounter = sublinecounter + 1
				instructionset.append(Functions.extractflaskoutput(logentry, linecounter, sublinecounter))
			elif logtype == "RESTART":
				outcome.insert(0, {"lineindex": " ", "entrytype": "restart", "content": "Restarting Service"})

#	if len(cache) > 0:
#		linecounter = linecounter + 1
#		instructionset.extend(Functions.extractotheroutput(cache, linecounter))

	return outcome



