from ...common_components.filesystem_framework import filesystem_module as FileSystem
from ...common_components.logging_framework import logging_module as Logging
from ...common_components.filesystem_framework import configfile_module as ConfigFile
from sqlite3 import connect as ConnectDatabase


def operatedatabase(databaseconnection, sqlcommand):

	print("============================================")
	print("============================================")
	print("============================================")
	print("NEW SQL COMMAND")
	print("============================================")
	print(sqlcommand)
	print("============================================")

	databaseconnection.execute(sqlcommand)

	print("============================================")

	databaseconnection.commit()

	print("============================================")
	print("============================================")
	print("============================================")

def operatedatabasewithparameters(databaseconnection, sqlcommand, sqlparameters):

	print("============================================")
	print("============================================")
	print("============================================")
	print("NEW SQL COMMAND WITH PARAMETERS")
	print("============================================")
	print(sqlcommand)
	print("============================================")
	print(sqlparameters)
	print("============================================")

	databaseconnection.execute(sqlcommand, sqlparameters)

	print("============================================")

	databaseconnection.commit()

	print("============================================")
	print("============================================")
	print("============================================")

# =========================================================================================
# Saves the current torrent config information, to a file
# =========================================================================================

def savetorrentconfigs(outputlist):
	Logging.printout("Saving Torrents Configuration Data")
	#FileSystem.writetodisk('./data/torrent_configs.db', outputlist, "Overwrite")

	currentconnection = ConnectDatabase('./data/application_memory/torrent_configs.sqlite')

	sqlcommand = "CREATE TABLE IF NOT EXISTS torrent("
	sqlcommand = sqlcommand + "torrentid CHAR(40) PRIMARY KEY NOT NULL, "
	sqlcommand = sqlcommand + "torrenttype CHAR(10) NOT NULL, "
	sqlcommand = sqlcommand + "torrentname CHAR(100), "
	sqlcommand = sqlcommand + "torrentseasonyear CHAR(10));"

	operatedatabase(currentconnection, sqlcommand)

	sqlcommand = "CREATE TABLE IF NOT EXISTS file("
	sqlcommand = sqlcommand + "fileid CHAR(4) NOT NULL, "
	sqlcommand = sqlcommand + "torrentid CHAR(40) NOT NULL, "
	sqlcommand = sqlcommand + "torrentfileid CHAR(45) PRIMARY KEY NOT NULL, "
	sqlcommand = sqlcommand + "filepurpose CHAR(20));"

	operatedatabase(currentconnection, sqlcommand)

	sqlcommand = "DELETE FROM torrent WHERE torrentid != ''"

	operatedatabase(currentconnection, sqlcommand)

	sqlcommand = "DELETE FROM file WHERE torrentid != ''"

	operatedatabase(currentconnection, sqlcommand)


	for databaseoperation in outputlist:

		sqlcommand = "INSERT INTO " + databaseoperation['recordtype']

		fieldlist = ""
		valuelist = []
		parameterlist = ""

		for fieldname in databaseoperation.keys():
			if fieldname != 'recordtype':
				if fieldlist != "":
					fieldlist = fieldlist + ", "
					parameterlist = parameterlist + ", "
				fieldlist = fieldlist + fieldname
				parameterlist = parameterlist + "?"
				valuelist.append(databaseoperation[fieldname])
		fieldlist = " (" + fieldlist + ")"
		parameterlist = " VALUES (" + parameterlist + ");"

		sqlcommand = sqlcommand + fieldlist + parameterlist

		operatedatabasewithparameters(currentconnection, sqlcommand, tuple(valuelist))

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



