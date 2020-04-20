from .... import database_definitions as Database
from json import loads as GetJson

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
			torrentdata[torrentid] = GetJson(torrentitem['torrentstats'])

		return torrentdata


