from . import torrenting_class as TorrentManagerClass


def createmanager(connectioncredentials):
	return TorrentManagerClass.DefineTorrentManager(connectioncredentials['Address'], connectioncredentials['Port'],
												connectioncredentials['Username'], connectioncredentials['Password'])
