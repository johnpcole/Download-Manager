from .filesystem_subcomponent import filesystem_module as FileSystem
from . import fileprocessing_class as FileManagerClass

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
	FileSystem.writetodisk('./data/torrentconfigs.db', outputlist)

# =========================================================================================
# Reads the current torrent config information, from a file
# =========================================================================================

def loadconfigs():
	return FileSystem.readfromdisk('./data/torrentconfigs.db')

# =========================================================================================
# Reads the configuration data for webhosting, from a file
# =========================================================================================

def getwebhostconfig():
	publicmode = FileSystem.readfromdisk('./data/webhost.cfg')
	if publicmode[0] == "Public":
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

def getloggingdata():
	loggingoutput = FileSystem.readfromdisk('./data/Logging.log')
	outcome = []
	linecounter = 0

	cache = []
	for logentry in loggingoutput:
		searchoutcome = logentry.find("HTTP/1.1")
		if searchoutcome == -1:
			cache.append(logentry)
		else:
			if len(cache) > 0:
				linecounter = linecounter + 1
				outcome.insert(0, {"lineindex": linecounter, "entrytype": "information", "content": cache})
				cache = []
			flaskoutput = {}
			datetimestart = logentry.find("[")
			datetimeend = logentry.find("]")
			linecounter = linecounter + 1
			flaskoutput["lineindex"] = linecounter
			flaskoutput["datetime"] = logentry[datetimestart + 1:datetimeend]
			flaskoutput["requestipaddress"] = "From " + logentry[:datetimestart - 4]
			rawdata = logentry[datetimeend + 3:]
			rawdata = rawdata.split(" ")
			flaskoutput["method"] = rawdata[0]
			flaskoutput["path"] = rawdata[1]
			flaskoutput["outcome"] = rawdata[3]
			if rawdata[3] == "200":
				flaskoutput["entrytype"] = "success"
			else:
				flaskoutput["entrytype"] = "failure"

			outcome.insert(0, flaskoutput)
	if len(cache) > 0:
		linecounter = linecounter + 1
		outcome.insert(0, {"lineindex": linecounter, "entrytype": "information", "content": cache})


	return outcome



