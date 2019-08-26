from ...common_components.filesystem_framework import filesystem_module as FileSystem
from . import filemanagement_class as FileManagerClass
from ...common_components.logging_framework import logging_module as Logging


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createmanager(connectioncredentials, connectiontries):
	return FileManagerClass.DefineFileManager(connectioncredentials['Mountpoint'],
												connectioncredentials['Address'],
												connectioncredentials['Username'],
												connectioncredentials['Password'],
												connectiontries)



# =========================================================================================
# Reads the configuration data for connecting to the file server, from a file
# =========================================================================================

def getlibraryconnectionconfig():
	Logging.printout("Loading File-Server Connection Data")
	credentials = FileSystem.readfromdisk('./data/application_config/copier_connection.cfg')
	outcome = { 'Mountpoint': credentials[0],
				'Address': credentials[1],
				'Username': credentials[2],
				'Password': credentials[3]}
	return outcome



