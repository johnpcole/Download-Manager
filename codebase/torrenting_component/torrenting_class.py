from deluge_subcomponent import deluge_module as DelugeClient
from torrentdata_subcomponent import torrentdata_module as TorrentData

class DefineTorrentManager:

	def __init__(self, address, port, username, password):

		if address == "dummy":
			self.delugeclient = DelugeClient.createdummy()
		else:
			self.delugeclient = DelugeClient.createinterface(address, port, username, password)

		#self.laststatustime = ???

		self.torrents = []

# =========================================================================================

	def refreshtorrentlist(self):

		outcome = self.delugeclient.openconnection()

		torrentidlist = self.delugeclient.gettorrentlist()
		for torrentiditem in torrentidlist:
			existingtorrent = self.gettorrent(torrentiditem)

			if existingtorrent is None:
				existingtorrent = self.addtorrent(torrentiditem)

			self.refreshtorrentdata(existingtorrent)

		outcome = self.delugeclient.closeconnection()
		#print "Connection closure attempted - Connection State = ", outcome

		cleanlist = []

		for existingtorrent in self.torrents:
			foundflag = False
			for torrentiditem in torrentidlist:
				if torrentiditem == existingtorrent.getid():
					cleanlist.append(existingtorrent)
					foundflag = True

			if foundflag == False:
				print "Deleting Torrent ", existingtorrent.getid()

		self.torrents = cleanlist

# =========================================================================================

	def addtorrent(self, torrentid):

		self.torrents.append(TorrentData.createitem(torrentid))
		print "Adding Torrent ", torrentid

		return self.gettorrent(torrentid)

# =========================================================================================

	def gettorrent(self, torrentid):

		outcome = None
		for existingtorrent in self.torrents:
			if existingtorrent.getid() == torrentid:
				outcome = existingtorrent

		return outcome

# =========================================================================================

	def refreshtorrentdata(self, torrentobject):

		outcome = self.delugeclient.openconnection()

		torrentdata = self.delugeclient.gettorrentdata(torrentobject.getid())
		torrentobject.updateinfo(torrentdata)

		outcome = self.delugeclient.closeconnection()
		#print "Connection closure attempted - Connection State = ", outcome


	# =========================================================================================

	def configuretorrent(self, torrentid, stuff):

		temp = stuff

# =========================================================================================

	def gettorrentlistdata(self, datamode):

		outcome = []

		for torrentitem in self.torrents:
			outcome.append(torrentitem.getheadlinedata(datamode))

		return outcome