from ...common_components.deluge_framework import deluge_module as DelugeClient
from ...common_components.logging_framework import logging_module as Logging


class DefineDelugeInterface:

	def __init__(self, address, port, username, password):

		# The information required to connect to the deluge daemon
		self.delugeclient = DelugeClient.createinterface(address, port, username, password)

		# The list of torrents in the deluge daemon; each item contains composite torrenting data (structured/layered dictionary)
		self.torrents = {}

		# The dictionary of session data
		self.sessiondata = {}

		self.performdelugeaction("Refresh", "None")






# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def retrievealldelugedata(self):

		# Get the list of torrent GUIDs from the Delude Daemon (as a flat list)
		reportedtorrentidlist = self.delugeclient.retrievetorrentlist()
		print("TORRENTLIST: " + str(len(reportedtorrentidlist)))

		# Update all the torrents' data relevent
		if reportedtorrentidlist is not None:
			self.torrents = {}
			for torrentid in reportedtorrentidlist:
				torrentdata = self.delugeclient.retrievetorrentdata(torrentid)
				self.torrents[torrentid] = torrentdata
		else:
			self.torrents = None

		# Get the overall session data from the Deluge Daemon (as a flat dictionary of values)
		# as well as summing up individual torrent data already gathered
		self.sessiondata = self.delugeclient.retrievesessiondata()

# =========================================================================================

	def performdelugeaction(self, action, item):

		print(self.delugeclient)

		self.delugeclient.openconnection()

		if action != "Refresh":
			if action == "Add":
				self.addnewtorrenttoclient(item)
			else:
				self.processexistingtorrent(item, action)

		self.retrievealldelugedata()

		#self.delugeclient.closeconnection()



# =========================================================================================

	def addnewtorrenttoclient(self, newurl):

		newid = self.delugeclient.addtorrentlink(newurl)
		Logging.printout("New Raw Torrent ID: " + newid)



# =========================================================================================

	def processexistingtorrent(self, torrentid, action):

		if action == "Stop":
			self.delugeclient.pausetorrent(torrentid)
		elif action == "Start":
			self.delugeclient.resumetorrent(torrentid)
		elif action == "Delete":
			self.delugeclient.deletetorrent(torrentid)
		else:
			Logging.printout("Unknown Torrent Request " + action + " on " + torrentid)



# =========================================================================================

	def getdelugedata(self):

		return {'sessiondata': self.sessiondata, 'torrents': self.torrents}



