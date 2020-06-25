from . import torrent_class as TorrentClass


def createitem(torrentid, torrentconfigurationlocation):
	return TorrentClass.DefineTorrentItem(torrentid, torrentconfigurationlocation)

