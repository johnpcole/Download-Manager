from .... import database_definitions as Database
from ....common_components.logging_framework import logging_module as Logging

class DefineTorrentConfigsDatabase:

	def __init__(self):

		self.torrentconfigs = Database.createtorrentconfigsdatabase()

	# =========================================================================================
	# Saves the current torrent config information, to a sqlite file
	# =========================================================================================

	def savetorrentconfigs(self, outputlist):

		Logging.printout("Saving Torrents Configuration Data")

		for databaseoperation in outputlist:
			self.deletetorrentconfigs(databaseoperation['torrentid'])

		self.torrentconfigs.insertdatabaserows(outputlist)



	# =========================================================================================
	# Deletes the current torrent config information, from a sqlite file
	# =========================================================================================

	def deletetorrentconfigs(self, torrentid):

		Logging.printout("Deleting Torrents Configuration Data")

		torrentdeleteset = []
		torrentdeleteset.append({'recordtype': 'torrent', 'torrentid': torrentid})
		torrentdeleteset.append({'recordtype': 'file', 'torrentid': torrentid})
		self.torrentconfigs.deletedatabaserows(torrentdeleteset)



	# =========================================================================================
	# Reads the current torrent config information, from a sqlite file
	# =========================================================================================

	def loadtorrentconfigs(self, torrentid):

		Logging.printout("Loading Torrents Configuration Data")

		torrentlookupset = []
		torrentlookupset.append({'recordtype': 'torrent', 'torrentid': torrentid})
		torrentlookupset.append({'recordtype': 'file', 'torrentid': torrentid})

		torrentdata = self.torrentconfigs.extractdatabaserows(torrentlookupset)
		return torrentdata
