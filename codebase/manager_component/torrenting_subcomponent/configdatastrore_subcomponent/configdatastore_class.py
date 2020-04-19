from ....common_components.database_framework import database_module as Database
from ....common_components.logging_framework import logging_module as Logging

class DefineTorrentConfigsDatabase:

	def __init__(self):

		self.torrentconfigs = Database.createdatabase('./data/application_memory/torrent_configs.sqlite')

		self.torrentconfigs.adddatabasestructure('torrent', 'torrentid', 'CHAR(40)', False, True)
		self.torrentconfigs.adddatabasestructure('torrent', 'torrenttype', 'CHAR(10)', False, False)
		self.torrentconfigs.adddatabasestructure('torrent', 'torrentname', 'CHAR(100)', True, False)
		self.torrentconfigs.adddatabasestructure('torrent', 'torrentseasonyear', 'CHAR(10)', True, False)
		self.torrentconfigs.adddatabasestructure('file', 'fileid', 'CHAR(4)', False, False)
		self.torrentconfigs.adddatabasestructure('file', 'torrentid', 'CHAR(40)', False, False)
		self.torrentconfigs.adddatabasestructure('file', 'torrentfileid', 'CHAR(45)', False, True)
		self.torrentconfigs.adddatabasestructure('file', 'filepurpose', 'CHAR(30)', True, False)

		self.torrentconfigs.changedatabasestate('Live')

		self.torrentconfigs.createentiredatabase()

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

	def loadtorrentconfigs(self, torrentid, recordtype):

		Logging.printout("Loading Torrents Configuration Data")

		torrentlookupset = []
		torrentlookupset.append({'recordtype': recordtype, 'torrentid': torrentid})

		torrentdata = self.torrentconfigs.extractdatabaserows(torrentlookupset)
		return torrentdata
