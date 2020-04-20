from .... import database_definitions as Database

class DefineDelugeDatabase:

	def __init__(self):

		self.delugedata = Database.createoperatorresultsdatabase()






	def getlatest(self):

		getter = []
		getter.append({'recordtype': 'torrent'})
		rawtorrentdata = self.delugedata.extractdatabaserows(getter)
		torrentdata = {}
		for torrentitem in rawtorrentdata:
			torrentid = torrentitem['torrentid']
			torrentdata[torrentid] = torrentitem['torrentstats']

		return torrentdata


