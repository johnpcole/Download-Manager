from .filesystem_subcomponent import filesystem_module as FileSystem
from . import fileprocessing_class as FileManagerClass
from ..common_components.logging_framework import logging_module as Logging


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createmanager(connectioncredentials):
	return FileManagerClass.DefineLibraryManager(connectioncredentials['Mountpoint'],
													connectioncredentials['Address'],connectioncredentials['Username'],
													connectioncredentials['Password'])



# =========================================================================================
# Reads the configuration data for connecting to the torrent daemon, from a file
# =========================================================================================

def gettorrentconnectionconfig():
	Logging.printout("Loading Deluge Daemon Connection Data")
	credentials = FileSystem.readfromdisk('./data/torrentconnection.cfg')
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
	credentials = FileSystem.readfromdisk('./data/libraryconnection.cfg')
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
	FileSystem.writetodisk('./data/torrentconfigs.db', outputlist)

# =========================================================================================
# Reads the current torrent config information, from a file
# =========================================================================================

def loadconfigs():
	Logging.printout("Loading Torrents Configuration Data")
	return FileSystem.readfromdisk('./data/torrentconfigs.db')



# =========================================================================================
# Reads the configuration data for webhosting, from a file
# =========================================================================================

def getwebhostconfig():
	Logging.printout("Loading Web-Hosting Configuration Data")
	publicmode = FileSystem.readfromdisk('./data/webhost.cfg')
	if publicmode[0] == "Public":
		outcome = True
	else:
		outcome = False
	return outcome



# =========================================================================================
# Reads the configuration data for logging, from a file
# =========================================================================================

def getloggingconfig():
	Logging.printout("Loading Logging Configuration Data")
	publicmode = FileSystem.readfromdisk('./data/logging.cfg')
	if publicmode[0] == "On":
		outcome = True
		Logging.printrawline("Verbose Logging Enabled")
	else:
		outcome = False
		Logging.printrawline("Verbose Logging Disabled")
	return outcome



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
		logcontents = FileSystem.readfromdisk('./data/logging-' + filename + '.log')
		print('---', filename, '---', logcontents)
		if (filename != '0') and (logcontents != ""):
			loggingoutput.append('--- RESTART ---')
			loggingoutput.extend(logcontents)
	outcome = Logging.processlog(loggingoutput, loggingmode)
	return outcome

