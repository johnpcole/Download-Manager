from . import torrenting_class as TorrentManagerClass


def createtorrentmanager(torrentconfigurationslocation):
	return TorrentManagerClass.DefineTorrentManager(torrentconfigurationslocation)
