from .. import delugeinterface_privatefunctions as Functions


class DefineDelugeTorrent:

	def __init__(self, tid, tdata):

		self.tid = tid

		self.tdata = tdata

		self.tdata['dm_fullstatus'] = Functions.getfulltorrentstatus(tdata['state'], tdata['is_finished'])



	def getid(self):

		return self.tid



	def getdata(self):

		return self.getdata()



	def gettrackerstatus(trackerstatus, torrentstatus):

		if torrentstatus[-6:] == "active":
			if trackerstatus.find(" Announce OK") != -1:
				outcome = 'green'
			elif trackerstatus.find(" Error: ") != -1:
				if trackerstatus.find(" Error: timed out") != -1:
					outcome = 'amber'
				elif trackerstatus.find(" Error: Invalid argument") != -1:
					outcome = 'orange'
				else:
					outcome = 'red'
			else:
				outcome = 'yellow'
		else:
			outcome = 'black'

		return outcome



	def calculatefulltorrentstatus(self):

		status = self.tdata['state'].lower()
		iscompleted = self.tdata['is_finished']

		if status == "queued":
			if iscompleted is True:
				outcome = "seeding_queued"
			else:
				outcome = "downloading_queued"
		elif status == "paused":
			if iscompleted is True:
				outcome = "seeding_paused"
			else:
				outcome = "downloading_paused"
		elif status == "downloading":
			outcome = "downloading_active"
		elif status == "seeding":
			outcome = "seeding_active"
		else:
			outcome = status

		self.tdata['dm_fullstatus'] = outcome



	def getconnectionstatusdata(torrentstatus, activepeers, activeseeders):

		outcome = {'activedownloads': 0, 'activeuploads': 0, 'downloadsavailable': 0, 'uploadsavailable': 0}

		if torrentstatus[-6:] == "active":
			outcome['uploadsavailable'] = 1
			if activepeers > 0:
				outcome['activeuploads'] = 1
			if torrentstatus == "downloading_active":
				outcome['downloadsavailable'] = 1
				if activeseeders > 0:
					outcome['activedownloads'] = 1

		return outcome










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


