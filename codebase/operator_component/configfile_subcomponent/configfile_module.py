from ...common_components.filesystem_framework import filesystem_module as FileSystem
from ...common_components.logging_framework import logging_module as Logging



# =========================================================================================
# Reads the configuration data for connecting to the torrent daemon, from a file
# =========================================================================================

def gettorrentconnectionconfig():
	Logging.printout("Loading Deluge Daemon Connection Data")
	credentials = FileSystem.readfromdisk('./data/application_config/operator_connection.cfg')
	outcome = { 'Address': credentials[0],
				'Port': int(credentials[1]),
				'Username': credentials[2],
				'Password': credentials[3]}
	return outcome


