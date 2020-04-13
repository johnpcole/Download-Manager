from ...common_components.filesystem_framework import filesystem_module as FileSystem
from ...common_components.logging_framework import logging_module as Logging
from ...common_components.filesystem_framework import configfile_module as ConfigFile
from sqlite3 import connect as ConnectDatabase


# =========================================================================================
# Saves the current torrent config information, to a file
# =========================================================================================

def savetorrentconfigs(outputlist):
	Logging.printout("Saving Torrents Configuration Data")
	#FileSystem.writetodisk('./data/torrent_configs.db', outputlist, "Overwrite")

	currentconnection = ConnectDatabase('./data/torrent_configs.sqlite')

	currentconnection.execute('''CREATE TABLE IF NOT EXISTS torrent(
									torrentid CHAR(40) PRIMARY KEY NOT NULL,
									torrenttype CHAR(10) NOT NULL,
									torrentname CHAR(100),
									torrentseasonyear CHAR(10);''')

	currentconnection.execute('''CREATE TABLE IF NOT EXISTS file(
									fileid CHAR(40) PRIMARY KEY NOT NULL,
									torrentid CHAR(40) NOT NULL,
									filepurpose CHAR(20);''')

	databasetransaction = currentconnection.cursor()

	for databaseoperation in outputlist:

		sqlcommand = "INSERT INTO " + databaseoperation['recordtype']

		fieldlist = ""
		valuelist = ""

		for fieldname in databaseoperation.keys():
			if fieldname != 'recordtype':
				if fieldlist != "":
					fieldlist = fieldlist + ", "
					valuelist = valuelist + ", "
				fieldlist = fieldlist + fieldname
				valuelist = valuelist + "'" + databaseoperation[fieldname] + "'"
		fieldlist = " (" + fieldlist + ")"
		valuelist = " VALUES (" + valuelist + ");"

		sqlcommand = sqlcommand + fieldlist + valuelist

		databasetransaction.execute(sqlcommand)

	currentconnection.commit()

	currentconnection.close()


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
			loggingitems = ConfigFile.readgeneralfile(filename)
			outcome.extend(loggingitems)

	return outcome



