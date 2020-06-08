from ...common_components.deluge_framework import deluge_module as DelugeClient
from ...common_components.logging_framework import logging_module as Logging
from ...common_components.datetime_datatypes import datetime_module as DateTime
from . import delugeinterface_privatefunctions as Functions


class DefineDelugeInterface:

	def __init__(self, address, port, username, password):

		# The information required to connect to the deluge daemon
		self.delugeclient = DelugeClient.createinterface(address, port, username, password)

		# The list of torrents in the deluge daemon; each item contains composite torrenting data (structured/layered dictionary)
		self.torrents = {}

		# The dictionary of session data
		self.sessiondata = {}

		self.lastdatascrape = DateTime.createfromiso("20100101000000")

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
				self.torrents[torrentid]['dm_fullstatus'] = Functions.getfulltorrentstatus(torrentdata['state'], torrentdata['is_finished'])
		else:
			self.torrents = None

		# Get the overall session data from the Deluge Daemon (as a flat dictionary of values)
		# as well as summing up individual torrent data already gathered
		self.sessiondata = self.delugeclient.retrievesessiondata()
		self.sessiondata['activedownloads'] = 0
		self.sessiondata['activeuploads'] = 0
		self.sessiondata['downloadsavailable'] = 0
		self.sessiondata['uploadsavailable'] = 0

		if self.torrents is not None:
			for torrentid in self.torrents.keys():
				torrentcounts = Functions.getconnectionstatusdata(self.torrents[torrentid]['dm_fullstatus'],
																	self.torrents[torrentid]['num_peers'],
																	self.torrents[torrentid]['num_seeds'])
				for datakey in torrentcounts.keys():
					self.sessiondata[datakey] = self.sessiondata[datakey] + torrentcounts[datakey]

		self.lastdatascrape.settonow()



# =========================================================================================

	def performdelugeaction(self, action, item):

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

		outcome = {'lastpolled': self.lastdatascrape.getiso()}
		if self.torrents is not None:
			outcome['torrents'] = self.torrents
		if self.sessiondata is not None:
			outcome['sessiondata'] = self.sessiondata

		return outcome



# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def gethistorydata(self):

		self.sessiondata = self.delugeclient.retrievesessiondata()
		self.sessiondata['activedownloads'] = 0
		self.sessiondata['activeuploads'] = 0
		self.sessiondata['downloadsavailable'] = 0
		self.sessiondata['uploadsavailable'] = 0

		if self.torrents is not None:
			for torrentid in self.torrents.keys():
				torrentcounts = Functions.getconnectionstatusdata(self.torrents[torrentid]['dm_fullstatus'],
																	self.torrents[torrentid]['num_peers'],
																	self.torrents[torrentid]['num_seeds'])
				for datakey in torrentcounts.keys():
					self.sessiondata[datakey] = self.sessiondata[datakey] + torrentcounts[datakey]

		self.lastdatascrape.settonow()


