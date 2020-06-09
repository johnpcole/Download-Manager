from ...common_components.deluge_framework import deluge_module as DelugeClient
from ...common_components.logging_framework import logging_module as Logging
from ...common_components.datetime_datatypes import datetime_module as DateTime
from .delugetorrent_subcomponent import delugetorrent_module as DelugeTorrent



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
				self.torrents[torrentid] = DelugeTorrent.createtorrent(torrentdata)
		else:
			self.torrents = None

		# Get the overall session data from the Deluge Daemon (as a flat dictionary of values)
		# as well as summing up individual torrent data already gathered
		self.sessiondata = self.delugeclient.retrievesessiondata()

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
			torrentdata = {}
			for torrentid in self.torrents.keys():
				torrentdata[torrentid] = self.torrents[torrentid].gettorrentdata()
			outcome['torrents'] = torrentdata
		if self.sessiondata is not None:
			outcome['sessiondata'] = self.calculateaggregatetorrentdata()

		return outcome



	def calculateaggregatetorrentdata(self):

		sessiondata = self.sessiondata.copy()
		sessiondata['activedownloads'] = 0
		sessiondata['activeuploads'] = 0
		sessiondata['downloadsavailable'] = 0
		sessiondata['uploadsavailable'] = 0

		if self.torrents is not None:
			for torrentid in self.torrents.keys():
				torrentcounts = self.torrents[torrentid].getconnectionstatusdata()
				for datakey in torrentcounts.keys():
					sessiondata[datakey] = sessiondata[datakey] + torrentcounts[datakey]

		return sessiondata



	def gethistorydata(self):

		sessiondata = {'red': 0, 'orange': 0, 'amber': 0, 'yellow': 0, 'green': 0, 'black': 0}
		sessiondata['uploadedtotal'] = self.sessiondata['uploadedtotal']

		if self.torrents is not None:
			for torrentid in self.torrents.keys():
				torrentcolour = self.torrents[torrentid].gettrackerstatus()
				sessiondata[torrentcolour] = sessiondata[torrentcolour] + 1

		return sessiondata
