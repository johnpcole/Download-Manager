from ...common_components.filesystem_framework import filesystem_module as FileSystem
from . import fileprocessing_class as FileManagerClass
from ...common_components.logging_framework import logging_module as Logging


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createmanager():
	return FileManagerClass.DefineLibraryManager()



# =========================================================================================
# Reads the configuration data for connecting to the torrent daemon, from a file
# =========================================================================================

def gettorrentconnectionconfig():
	Logging.printout("Loading Deluge Daemon Connection Data")
	credentials = FileSystem.readfromdisk('./data/application_config/torrent_connection.cfg')
	outcome = { 'Address': credentials[0],
				'Port': int(credentials[1]),
				'Username': credentials[2],
				'Password': credentials[3]}
	return outcome



# =========================================================================================
# Reads the configuration data for connecting to the file server, from a file
# =========================================================================================

def getlibraryconnectionconfig():
	Logging.printout("Loading File-Server Connection Data")
	credentials = FileSystem.readfromdisk('./data/application_config/library_connection.cfg')
	outcome = { 'Mountpoint': credentials[0],
				'Address': credentials[1],
				'Username': credentials[2],
				'Password': credentials[3]}
	return outcome



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

def buildpath(nodelist):
	outcome = "-"
	for node in nodelist:
		outcome = FileSystem.concatenatepaths(outcome, node)

	return outcome[2:]



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


