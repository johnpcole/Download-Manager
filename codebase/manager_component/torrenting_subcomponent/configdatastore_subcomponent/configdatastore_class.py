from .... import database_definitions as Database
from ....common_components.logging_framework import logging_module as Logging


class DefineTorrentConfigsDatabase:

	def __init__(self):

		self.torrentconfigs = Database.createtorrentconfigsdatabase()





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
