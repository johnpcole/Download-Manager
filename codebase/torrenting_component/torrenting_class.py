from .deluge_subcomponent import deluge_module as DelugeClient
from .torrentdata_subcomponent import torrentdata_module as TorrentData
from ..functions_component import functions_module as Functions
from .thermometer_subcomponent import thermometer_module as PiThermometer
from .sessiondatameters_subcomponent import sessiondatameters_module as SessionDataMeters


class DefineTorrentManager:

	def __init__(self, address, port, username, password):

		# The information required to connect to the deluge daemon
		if address == "dummy":
			self.delugeclient = DelugeClient.createdummy()
		else:
			self.delugeclient = DelugeClient.createinterface(address, port, username, password)

		# The list of torrents in the deluge daemon; each item contains composite torrenting data
		self.torrents = []

		# An array of meter graph data, capturing important overall torrenting stats
		self.sessiondata = SessionDataMeters.createsessiondatameters()


# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshtorrentlist(self):

		dummyoutcome = self.delugeclient.openconnection()

		self.sessiondata.updatesessionstats(self.delugeclient.getsessiondata(), PiThermometer.gettemperature())

		torrentidlist = self.delugeclient.gettorrentlist()

		dummyoutcome = self.delugeclient.closeconnection()
		#print("Connection closure attempted - Connection State = ", outcome)

		self.registermissingtorrentsandupdatetorrentdata(torrentidlist)

		self.cleantorrentlist(torrentidlist)

		self.sessiondata.updateactivitycounts(self.torrents)

# =========================================================================================
# Registers a torrent in Download-Manager, with default torrent data which is
# populated with real data later
# =========================================================================================

	def registertorrentobject(self, torrentid):

		self.torrents.append(TorrentData.createitem(torrentid))
		print("Registering Torrent in Download-Manager", torrentid)

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
# Refreshes the torrent data for the specified ID, by connecting to the Deluge client
# =========================================================================================

	def refreshtorrentdata(self, torrentid):

		torrentobject = self.gettorrentobject(torrentid)

		dummyoutcome = self.delugeclient.openconnection()

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
		torrentobject.reconfiguretorrent(newconfig)

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
				print("Ignoring Saved Config for Torrent ", datavalues[0])

# =========================================================================================

	def addnewtorrenttoclient(self, newurl):

		outcome = self.delugeclient.openconnection()
		newid = self.delugeclient.addtorrentlink(newurl)
		print("New Raw Torrent ID: ", newid)
		newobject = self.registertorrentobject(newid)
		#TO-DO = change newobject to be success/error outcome, allowing for graceful failure
		self.refreshtorrentdata(newid)
		outcome = self.delugeclient.closeconnection()

		return newid

# =========================================================================================

	def bulkprocessalltorrents(self, bulkaction):

		if bulkaction == "Stop":
			outcome = self.delugeclient.openconnection()
			self.delugeclient.pausetorrent("ALL")
			outcome = self.delugeclient.closeconnection()
		elif bulkaction == "Start":
			outcome = self.delugeclient.openconnection()
			self.delugeclient.resumetorrent("ALL")
			outcome = self.delugeclient.closeconnection()
		else:
			print("Unknown Bulk Torrent Request ", bulkaction)

# =========================================================================================

	def processonetorrent(self, torrentid, action):

		if action == "Stop":
			outcome = self.delugeclient.openconnection()
			self.delugeclient.pausetorrent(torrentid)
			outcome = self.delugeclient.closeconnection()
		elif action == "Start":
			outcome = self.delugeclient.openconnection()
			self.delugeclient.resumetorrent(torrentid)
			outcome = self.delugeclient.closeconnection()
		elif action == "Delete":
			outcome = self.delugeclient.openconnection()
			#self.delugeclient.pausetorrent(torrentid)
			self.delugeclient.deletetorrent(torrentid)
			outcome = self.delugeclient.closeconnection()
		else:
			print("Unknown Single Torrent Request ", action)

# =========================================================================================

	def getcopyactions(self, torrentid):

		torrentobject = self.gettorrentobject(torrentid)
		if torrentobject.getfinished() == 'Completed':
			outcome = torrentobject.getcopyactions()
		else:
			outcome = []

		return outcome



# =========================================================================================
# Identifies any torrents in the deluge client that aren't captured in the Download-Manager,
# and registers them in Download-Manager, and gets all the relevent torrent data (files etc)
# =========================================================================================

	def registermissingtorrentsandupdatetorrentdata(self, torrentidlist):

		for torrentiditem in torrentidlist:

			if self.validatetorrentid(torrentiditem) == False:
				dummynewtorrentobject = self.registertorrentobject(torrentiditem)

			self.refreshtorrentdata(torrentiditem)

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
				print("Deregistering Missing Torrent in Download-Manager: ", existingtorrent.getid())

		self.torrents = Functions.sortdictionary(cleanlist, 'dateadded', True)



# =========================================================================================
# Generates an array of stat numerics, required to draw the meter graphs
# =========================================================================================

	def getstats(self):

		return self.sessiondata.getstats()
