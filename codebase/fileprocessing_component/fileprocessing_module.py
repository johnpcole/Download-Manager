from .filesystem_subcomponent import filesystem_module as FileSystem
from . import fileprocessing_class as FileManagerClass
from .logreader_subcomponent import logreader_module as LogReader
from ..functions_component import functions_module as Functions


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
	Functions.printout("Loading Deluge Daemon Connection Data")
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
	Functions.printout("Loading File-Server Connection Data")
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
	Functions.printout("Saving Torrents Configuration Data")
	FileSystem.writetodisk('./data/torrentconfigs.db', outputlist)

# =========================================================================================
# Reads the current torrent config information, from a file
# =========================================================================================

def loadconfigs():
	Functions.printout("Loading Torrents Configuration Data")
	return FileSystem.readfromdisk('./data/torrentconfigs.db')



# =========================================================================================
# Reads the configuration data for webhosting, from a file
# =========================================================================================

def getwebhostconfig():
	Functions.printout("Loading Web-Hosting Configuration Data")
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
	Functions.printout("Loading Logging Configuration Data")
	publicmode = FileSystem.readfromdisk('./data/logging.cfg')
	if publicmode[0] == "On":
		outcome = True
	else:
		outcome = False
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
	Functions.printout("Loading Logs")
	loggingoutput = FileSystem.readfromdisk('./data/Logging.log')
	outcome = LogReader.processlog(loggingoutput, loggingmode)
	return outcome

