from ...common_components.deluge_framework import deluge_module as DelugeClient
from ...common_components.logging_framework import logging_module as Logging
from ...common_components.datetime_datatypes import datetime_module as DateTime


class DefineDelugeInterface:

	def __init__(self, address, port, username, password):

		# The information required to connect to the deluge daemon
		self.delugeclient = DelugeClient.createinterface(address, port, username, password)

		# The list of torrents in the deluge daemon; each item contains composite torrenting data (structured/layered dictionary)
		self.torrents = {}

		# The dictionary of session data
		self.sessiondata = {}

		self.lastdatascrape = DateTime.createfromiso("20100101000000")

		self.isdataformonitor = False

		self.performdelugeaction("Refresh", "None")



# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def retrievealldelugedata(self):

		# Get the list of torrent GUIDs from the Delude Daemon (as a flat list)
		reportedtorrentidlist = self.delugeclient.retrievetorrentlist()

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

		self.lastdatascrape.settonow()


	def blankdata(self):
		self.torrents = None
		self.sessiondata = None
		self.isdataformonitor = False

# =========================================================================================

	def performdelugeaction(self, action, item):

		self.delugeclient.openconnection()

		if (action != "Refresh") and (action != "Monitor-History"):
			if action == "Add":
				self.addnewtorrenttoclient(item)
			else:
				self.processexistingtorrent(item, action)

		self.retrievealldelugedata()

		if action == "Monitor-History":
			self.isdataformonitor = True
		else:
			self.isdataformonitor = False

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

		outcome = {'lastpolled': self.lastdatascrape.getiso()}
		if self.torrents is not None:
			outcome['torrents'] = self.torrents
		if self.sessiondata is not None:
			outcome['sessiondata'] = self.sessiondata
		else:
			outcome['sessiondata'] = {}
		outcome['monitorhistory'] = self.isdataformonitor

		return outcome



