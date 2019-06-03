from .deluge_subcomponent import deluge_module as DelugeClient
from .torrent_subcomponent import torrent_module as TorrentData
from ..common_components.dataconversion_framework import dataconversion_module as Functions
from ..common_components.logging_framework import logging_module as Logging



class DefineTorrentManager:

	def __init__(self, address, port, username, password):

		# The information required to connect to the deluge daemon
		self.delugeclient = DelugeClient.createinterface(address, port, username, password)

		# The list of torrents in the deluge daemon; each item contains composite torrenting data (structured/layered dictionary)
		self.torrents = []

		# The dictionary of session data
		self.sessiondata = {}

		# The dictionary of current monitor data
		self.monitordata = {}

		self.refreshtorrentlist("Download-Manager")

# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshtorrentlist(self, refreshmode):

		# Open the connection to the Deluge Daemon
		dummyoutcome = self.delugeclient.openconnection("Refresh Torrents List for " + refreshmode)

		# Get the list of torrent GUIDs from the Delude Daemon (as a flat list)
		reportedtorrentidlist = self.delugeclient.gettorrentlist()

		# Update the list of torrents to include new torrents not previously managed by Download-Manager
		self.registermissingtorrents(reportedtorrentidlist)

		# Update the list of torrents to exclude torrents previously managed by Download-Manager
		self.cleantorrentlist(reportedtorrentidlist)

		if refreshmode == "Download-Manager":
			# Update all the torrents' data relevent for Download-Manager
			self.refreshtorrentobjectsdata(self.torrents)
			# Get the overall session data from the Deluge Daemon (as a flat dictionary of values)
			self.refreshsessiondata()

		elif refreshmode == "Deluge-Monitor":
			# Update torrents' data relevent for Deluge Monitor
			self.refreshmonitordata()

		else:
			assert 1 == 0, ("Unknown Refresh Torrents List Mode: " + refreshmode)

		# Close the connection to the Deluge Daemon
		dummyoutcome = self.delugeclient.closeconnection()
		#print("Connection closure attempted - Connection State = ", outcome)

# =========================================================================================
# Registers a torrent in Download-Manager, with default torrent data which is
# populated with real data later
# =========================================================================================

	def registertorrentobject(self, torrentid):

		self.torrents.append(TorrentData.createitem(torrentid))
		Logging.printout("Registering Torrent in Download-Manager: " + torrentid)

		return self.gettorrentobject(torrentid)

# =========================================================================================
# Confirms whether the specified torrent id is registered in Download-Manager
# =========================================================================================

	def validatetorrentid(self, torrentid):

		outcome = False
		for existingtorrent in self.torrents:
			if existingtorrent.getid() == torrentid:
				outcome = True
		return outcome

# =========================================================================================
# Returns the torrent object (containing all the torrent data) for a specified ID
# =========================================================================================

	def gettorrentobject(self, torrentid):

		outcome = None
		for existingtorrent in self.torrents:
			if existingtorrent.getid() == torrentid:
				outcome = existingtorrent

		return outcome

# =========================================================================================
# Refreshes the torrent data for the specified IDs, by connecting to the Deluge client
# assuming there is already an open connection to Deluge
# =========================================================================================

	def refreshtorrentobjectsdata(self, torrentobjects):

		for torrentobject in torrentobjects:
			torrentid = torrentobject.getid()
			torrentdata = self.delugeclient.gettorrentdata(torrentid)
			torrentobject.updateinfo(torrentdata)

# =========================================================================================
# Refreshes the torrent data for the specified ID, by connecting to the Deluge client
# =========================================================================================

	def refreshtorrentdata(self, torrentid):

		dummyoutcome = self.delugeclient.openconnection("Refresh Torrent " + torrentid)
		torrentobject = self.gettorrentobject(torrentid)
		torrentdata = self.delugeclient.gettorrentdata(torrentid)
		torrentobject.updateinfo(torrentdata)
		dummyoutcome = self.delugeclient.closeconnection()
		#print("Connection closure attempted - Connection State = ", outcome)

# =========================================================================================

	def gettorrentlistdata(self, datamode):

		outcome = []

		for torrentitem in self.torrents:
			outcome.append(torrentitem.getheadlinedata(datamode))

		return outcome

# =========================================================================================

	def gettorrentdata(self, torrentid, datamode):

		torrentobject = self.gettorrentobject(torrentid)

		return torrentobject.getextendeddata(datamode)

# =========================================================================================

	def reconfiguretorrent(self, torrentid, newconfig):

		torrentobject = self.gettorrentobject(torrentid)
		torrentobject.updateinfo(newconfig)

# =========================================================================================

	def getconfigs(self):

		outcome = []
		for torrentitem in self.torrents:
			newrows = torrentitem.getsavedata()
			for newrow in newrows:
				outcome.append(newrow)
		return outcome

# =========================================================================================

	def setconfigs(self, datalist):

		for dataitem in datalist:
			datavalues = dataitem.split("|")
			torrentobject = self.gettorrentobject(datavalues[0])
			if torrentobject is not None:
				torrentobject.setsavedata(datavalues)
			else:
				Logging.printout("Ignoring Saved Config for Torrent " + datavalues[0])

# =========================================================================================

	def addnewtorrenttoclient(self, newurl):

		outcome = self.delugeclient.openconnection("Add Torrent")
		newid = self.delugeclient.addtorrentlink(newurl)
		Logging.printout("New Raw Torrent ID: " + newid)
		newobject = self.registertorrentobject(newid)
		#TO-DO = change newobject to be success/error outcome, allowing for graceful failure
		self.refreshtorrentobjectsdata([newobject])
		outcome = self.delugeclient.closeconnection()

		return newid

# =========================================================================================

	def bulkprocessalltorrents(self, bulkaction):

		if bulkaction == "Stop":
			outcome = self.delugeclient.openconnection("Stop All Torrents")
			self.delugeclient.pausetorrent("ALL")
			outcome = self.delugeclient.closeconnection()
		elif bulkaction == "Start":
			outcome = self.delugeclient.openconnection("Start All Torrents")
			self.delugeclient.resumetorrent("ALL")
			outcome = self.delugeclient.closeconnection()
		else:
			Logging.printout("Unknown Bulk Torrent Request " + bulkaction)

# =========================================================================================

	def processonetorrent(self, torrentid, action):

		if action == "Stop":
			outcome = self.delugeclient.openconnection("Stop Torrent " + torrentid)
			self.delugeclient.pausetorrent(torrentid)
			outcome = self.delugeclient.closeconnection()
		elif action == "Start":
			outcome = self.delugeclient.openconnection("Start Torrent " + torrentid)
			self.delugeclient.resumetorrent(torrentid)
			outcome = self.delugeclient.closeconnection()
		elif action == "Delete":
			outcome = self.delugeclient.openconnection("Delete Torrent " + torrentid)
			#self.delugeclient.pausetorrent(torrentid)
			self.delugeclient.deletetorrent(torrentid)
			outcome = self.delugeclient.closeconnection()
		else:
			Logging.printout("Unknown Single Torrent Request " + action)

# =========================================================================================

	def getcopyactions(self, torrentid):

		torrentobject = self.gettorrentobject(torrentid)
		return torrentobject.getcopyactions()



# =========================================================================================
# Identifies any torrents in the deluge client that aren't captured in the Download-Manager,
# and registers them in Download-Manager, and gets all the relevent torrent data (files etc)
# =========================================================================================

	def registermissingtorrents(self, torrentidlist):

		for torrentiditem in torrentidlist:

			if self.validatetorrentid(torrentiditem) == False:
				dummynewtorrentobject = self.registertorrentobject(torrentiditem)

# =========================================================================================
# Identifies any torrents in Download-Manager which are no longer in the deluge client,
# and deregisters them from Download-Manager; Also orders the torrent list by date added
# =========================================================================================

	def cleantorrentlist(self, torrentidlist):

		cleanlist = []

		for existingtorrent in self.torrents:
			foundflag = False
			for torrentiditem in torrentidlist:
				if torrentiditem == existingtorrent.getid():
					cleanlist.append(existingtorrent)
					foundflag = True

			if foundflag == False:
				Logging.printout("Deregistering Missing Torrent in Download-Manager: " + existingtorrent.getid())

		self.torrents = Functions.sortdictionary(cleanlist, 'dateadded', True)


# =========================================================================================
# Refreshes the torrent tracker/upload data for all torrents, by connecting to the Deluge client
# =========================================================================================

	def refreshmonitordata(self):

		outcome = {'uploadeddelta': 0, 'redcount': 0, 'ambercount': 0, 'greencount': 0}

		for torrentobject in self.torrents:
			torrentid = torrentobject.getid()
			torrentdata = self.delugeclient.getmonitordata(torrentid)
			torrentoutcome = torrentobject.updatemonitor(torrentdata)
			outcome['uploadeddelta'] = outcome['uploadeddelta'] + torrentoutcome['uploadeddelta']
			trackerstatus = torrentoutcome['trackerstatus'] + "count"
			outcome[trackerstatus] = outcome[trackerstatus] + 1

		self.monitordata = outcome


	def getmonitordata(self):

		return self.monitordata

# =========================================================================================
# Refreshes the torrenting session data, by connecting to the Deluge client and also
# extracting data from individual torrents
# =========================================================================================

	def refreshsessiondata(self):

		torrentkeylist = ['downloadcount', 'activedownloads', 'uploadcount', 'activeuploads']

		outcome = self.delugeclient.getsessiondata()
		for indexkey in torrentkeylist:
			outcome[indexkey] = 0

		for existingtorrent in self.torrents:

			currenttorrent = existingtorrent.getconnectiondata()

			for indexkey in torrentkeylist:
				outcome[indexkey] = outcome[indexkey] + currenttorrent[indexkey]

		self.sessiondata = outcome


	def getsessiondata(self):

		return self.sessiondata


