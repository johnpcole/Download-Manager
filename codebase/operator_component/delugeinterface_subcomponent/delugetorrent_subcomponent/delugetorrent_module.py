from . import delugetorrent_class as DelugeTorrentClass


def createtorrent(tid, tdata):
	return DelugeTorrentClass.DefineDelugeTorrent(tid, tdata)
