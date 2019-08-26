from .torrent_subcomponent import torrent_module as TorrentData
from ...common_components.dataconversion_framework import dataconversion_module as Functions
from ...common_components.logging_framework import logging_module as Logging



class DefineTorrentManager:

	def __init__(self):

		# The list of torrents in the deluge daemon; each item contains composite torrenting data (structured/layered dictionary)
		self.torrents = []



# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshtorrentlist(self, torrentdata):

		# Update the list of torrents to include new torrents not previously managed by Download-Manager
		self.registermissingtorrents(torrentdata.keys())

		# Update the list of torrents to exclude torrents previously managed by Download-Manager
		self.cleantorrentlist(torrentdata.keys())

		# Update all the torrents' data relevent for Download-Manager/Deluge-Monitor
		self.refreshalltorrentdata(torrentdata)


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
# Refreshes the torrent data for the specified torrent objects, by connecting to the Deluge
# client assuming there is already an open connection to Deluge
# =========================================================================================

	def refreshalltorrentdata(self, torrentdata):

		for torrentid in torrentdata.keys():
			if self.validatetorrentid(torrentid) == True:
				torrentobject = self.gettorrentobject(torrentid)
				torrentobject.updateinfo(torrentdata[torrentid])

# =========================================================================================

	def gettorrentlistdata(self, datamode):

		outcome = []

		for torrentitem in self.torrents:
			if torrentitem.isvisible() == True:
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

	def getcopyactions(self, torrentid):

		torrentobject = self.gettorrentobject(torrentid)
		return torrentobject.gettorrentcopyactions()



# =========================================================================================
# Identifies any torrents in the deluge client that aren't captured in the Download-Manager,
# and registers them in Download-Manager, and gets all the relevent torrent data (files etc)
# =========================================================================================

	def registermissingtorrents(self, torrentidlist):

		for torrentiditem in torrentidlist:

			if self.validatetorrentid(torrentiditem) == False:
				self.torrents.append(TorrentData.createitem(torrentiditem))
				Logging.printout("Registering Torrent in Download-Manager: " + torrentiditem)



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

		print("====================================================================================================")
		for tester in self.torrents:
			print(tester.torrentid, tester.torrentname, tester.dateadded)
		print("====================================================================================================")


# =========================================================================================
# Refreshes the torrenting session data, by connecting to the Deluge client and also
# extracting data from individual torrents
# =========================================================================================

	def getaggregates(self):

		outcome = {'downloadcount': 0, 'activedownloads': 0, 'uploadcount': 0, 'activeuploads': 0,
								'redcount': 0, 'orangecount': 0, 'ambercount': 0, 'yellowcount': 0, 'greencount': 0}

		for existingtorrent in self.torrents:

			currenttorrent = existingtorrent.getconnectiondata()

			for indexkey in currenttorrent:
				outcome[indexkey] = outcome[indexkey] + currenttorrent[indexkey]

		return outcome


# =========================================================================================

	def gettorrentidlist(self):

		outcome = []
		for torrentitem in self.torrents:
			outcome.append(torrentitem.getid())

		return outcome


# =========================================================================================

	def markasdeteled(self, torrentid):

		torrentobject = self.gettorrentobject(torrentid)
		torrentobject.markasdeleted()


