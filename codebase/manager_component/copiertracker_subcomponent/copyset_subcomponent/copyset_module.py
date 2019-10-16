from . import copyset_class as CopySetClass


def createtorrentcopytracker(torrentid):
	return CopySetClass.DefineSet(torrentid)

def createglobalactiontracker():
	return CopySetClass.DefineSet("< ALL ACTION ITEMS >")

def createrefreshtracker():
	return CopySetClass.DefineSet("< REFRESH FOLDERS >")