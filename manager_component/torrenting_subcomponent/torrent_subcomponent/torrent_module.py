from . import torrent_class as TorrentClass


def createitem(torrentid):
	return TorrentClass.DefineTorrentItem(torrentid)

