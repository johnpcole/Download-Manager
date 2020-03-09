from ...common_components.filesystem_framework import filesystem_module as FileSystem
from ...common_components.logging_framework import logging_module as Logging
from ...common_components.filesystem_framework import configfile_module as ConfigFile


# =========================================================================================
# Saves the current torrent config information, to a file
# =========================================================================================

def savetorrentconfigs(outputlist):
	Logging.printout("Saving Torrents Configuration Data")
	FileSystem.writetodisk('./data/torrent_configs.db', outputlist, "Overwrite")

# =========================================================================================
# Reads the current torrent config information, from a file
# =========================================================================================

def loadtorrentconfigs():
	Logging.printout("Loading Torrents Configuration Data")
	return ConfigFile.readgeneralfile("./data/torrent_configs.db")



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
# Reads the logging data, from a file
# =========================================================================================

def getloggingdata(loggingmode):
	Logging.printout("Loading Logs")
	loggingoutput = []
	logcontents = ConfigFile.readgeneralfile('./data/application_logs/manager.log')
	loggingoutput.extend(logcontents)
	outcome = Logging.processlog(loggingoutput, loggingmode)
	return outcome


# =========================================================================================
# Writes monitor data
# =========================================================================================

def savemonitor(monitordata):

	datestamp = monitordata[:8]
	filename = './data/monitor_history/history_' + datestamp + '.db'

	if FileSystem.doesexist(filename) is True:
		appendflag = "Append"
	else:
		appendflag = "Overwrite"

	FileSystem.writetodisk(filename, [monitordata], appendflag)



def getmonitor(filenamelist):

	Logging.printout("Loading Recent Deluge Monitor History")
	outcome = []

	for filenameitem in filenamelist:
		filename = './data/monitor_history/history_' + filenameitem + '.db'

		if FileSystem.doesexist(filename) is True:
			loggingitems = ConfigFile.readgeneralfile(filename)
			outcome.extend(loggingitems)

	return outcome



