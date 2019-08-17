from ...common_components.filesystem_framework import filesystem_module as FileSystem
from . import fileprocessing_class as FileManagerClass
from ...common_components.logging_framework import logging_module as Logging


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createfilemanager():
	return FileManagerClass.DefineLibraryManager()



# =========================================================================================
# Saves the current torrent config information, to a file
# =========================================================================================

def saveconfigs(outputlist):
	Logging.printout("Saving Torrents Configuration Data")
	FileSystem.writetodisk('./data/torrent_configs.db', outputlist, "Overwrite")

# =========================================================================================
# Reads the current torrent config information, from a file
# =========================================================================================

def loadconfigs():
	Logging.printout("Loading Torrents Configuration Data")
	return FileSystem.readfromdisk('./data/torrent_configs.db')



# =========================================================================================
# Reads the configuration data for webhosting, from a file
# =========================================================================================

#def getwebhostconfig():
	#Logging.printout("Loading Web-Hosting Configuration Data")
	#publicmode = FileSystem.readfromdisk('./data/webhost.cfg')
	#if publicmode[0] == "Public":
	#	outcome = True
	#else:
	#	outcome = False
	#return outcome


# =========================================================================================
# Creates a filepath from a list of nodes, using the appropriate filesystem symbol
# =========================================================================================

# def buildpath(nodelist):
# 	outcome = "-"
# 	for node in nodelist:
# 		outcome = FileSystem.concatenatepaths(outcome, node)
#
# 	return outcome[2:]



# =========================================================================================
# Reads the logging data, from a file
# =========================================================================================

def getloggingdata(loggingmode):
	Logging.printout("Loading Logs")
	loggingoutput = []
	for filename in ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0']:
		logcontents = FileSystem.readfromdisk('./data/application_logs/manager_' + filename + '.log')
		if len(logcontents) > 0:
			if filename != '9':
				loggingoutput.append('--- RESTART SERVICE ---')
			loggingoutput.extend(logcontents)
	outcome = Logging.processlog(loggingoutput, loggingmode)
	return outcome


# =========================================================================================
# Writes monitor data
# =========================================================================================

def savemonitor(monitordata):

	datestamp = monitordata[:8]
	filename = './data/monitor_history/history_' + datestamp + '.db'

	if FileSystem.doesexist(filename) == True:
		appendflag = "Append"
	else:
		appendflag = "Overwrite"

	FileSystem.writetodisk(filename, [monitordata], appendflag)



def getmonitor(filenamelist):

	Logging.printout("Loading Recent Deluge Monitor History")
	outcome = []

	for filenameitem in filenamelist:
		filename = './data/monitor_history/history_' + filenameitem + '.db'

		if FileSystem.doesexist(filename) == True:
			loggingitems = FileSystem.readfromdisk(filename)
			outcome.extend(loggingitems)

	return outcome



