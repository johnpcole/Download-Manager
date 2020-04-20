from .... import database_definitions as Database

class DefineSessionDatabase:

	def __init__(self):

		self.delugedata = Database.createoperatorresultsdatabase()






	def getlatest(self):

		getter = []
		getter.append({'recordtype': 'session'})
		rawtorrentdata = self.delugedata.extractdatabaserows(getter)
		torrentdata = {}
		for torrentitem in rawtorrentdata:
			torrentid = torrentitem['sessionstat']
			torrentdata[torrentid] = torrentitem['sessionvalue']

		return torrentdata


