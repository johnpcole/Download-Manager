from .deluge_subcomponent import deluge_module as DelugeClient
from .torrent_subcomponent import torrent_module as TorrentData
from ..common_components.dataconversion_framework import dataconversion_module as Functions
from .thermometer_subcomponent import thermometer_module as PiThermometer
from .sessiondatameters_subcomponent import sessiondatameters_module as SessionDataMeters
#from .monitorhistory_subcomponent import monitorhistory_module as MonitorHistory
from ..common_components.logging_framework import logging_module as Logging



class DefineTorrentManager:

	def __init__(self, address, port, username, password):

		# The information required to connect to the deluge daemon
		if address == "dummy":
			self.delugeclient = DelugeClient.createdummy()
		else:
			self.delugeclient = DelugeClient.createinterface(address, port, username, password)

		# The list of torrents in the deluge daemon; each item contains composite torrenting data (structured/layered dictionary)
		self.torrents = []

		# An array of meter graph data, capturing important overall torrenting stats
		self.sessiondata = SessionDataMeters.createsessiondatameters()

		# An array of historic monitor history
		#self.monitorhistory = MonitorHistory.createhistory()

		self.refreshtorrentlist("Download-Manager")



# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshtorrentlist(self, refreshmode):

		# Open the connection to the Deluge Daemon
		dummyoutcome = self.delugeclient.openconnection("Refresh Torrents List for " + refreshmode)

		# Get the overall session data from the Deluge Daemon (as a flat dictionary of values)
		if refreshmode == "Download-Manager":
			sessiondata = self.delugeclient.getsessiondata()

		# Get the list of torrent GUIDs from the Delude Daemon (as a flat list)
		reportedtorrentidlist = self.delugeclient.gettorrentlist()

		# Update the list of torrents to include new torrents not previously managed by Download-Manager
		self.registermissingtorrents(reportedtorrentidlist)

		# Update all the torrents' data
		if refreshmode == "Download-Manager":
			self.refreshmultipletorrentdata(reportedtorrentidlist)
		elif refreshmode == "Deluge-Monitor":
			self.refreshmonitordata(reportedtorrentidlist)
		else:
			assert 1 == 0, ("Unknown Refresh Torrents List Mode: " + refreshmode)

		# Close the connection to the Deluge Daemon
		dummyoutcome = self.delugeclient.closeconnection()
		#print("Connection closure attempted - Connection State = ", outcome)

		# Update the list of torrents to exclude torrents previously managed by Download-Manager
		self.cleantorrentlist(reportedtorrentidlist)

		# Update the session data meters with the latest Delude Daemon session data and Raspberry Pi temperature
		if refreshmode == "Download-Manager":
			self.sessiondata.updatesessiondata(sessiondata, PiThermometer.gettemperature(), self.torrents)

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

	def refreshmultipletorrentdata(self, torrentidlist):

		for torrentid in torrentidlist:
			torrentobject = self.gettorrentobject(torrentid)
			torrentdata = self.delugeclient.gettorrentdata(torrentid)
			torrentobject.updateinfo(torrentdata)

# =========================================================================================
# Refreshes the torrent data for the specified ID, by connecting to the Deluge client
# =========================================================================================

	def refreshtorrentdata(self, torrentid):

		dummyoutcome = self.delugeclient.openconnection("Refresh Torrent " + torrentid)
		self.refreshmultipletorrentdata([torrentid])
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
		self.refreshmultipletorrentdata([newid])
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
# Generates an array of stat numerics, required to draw the meter graphs
# =========================================================================================

	def getstats(self):

		return self.sessiondata.getstats()


# =========================================================================================
# Refreshes the torrent tracker/upload data for all torrents, by connecting to the Deluge client
# =========================================================================================

	def refreshmonitordata(self, torrentidlist):

		for torrentid in torrentidlist:
			torrentobject = self.gettorrentobject(torrentid)
			torrentdata = self.delugeclient.gettorrentdata(torrentid)
			torrentobject.updateinfo(torrentdata)


