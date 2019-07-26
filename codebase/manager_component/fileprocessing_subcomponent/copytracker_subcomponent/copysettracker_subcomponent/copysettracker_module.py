from . import copysettracker_class as CopySetTrackerClass


def createtorrentcopytracker(torrentid):
	return CopySetTrackerClass.DefineSetTracker(torrentid)

def createglobalcopytracker():
	return CopySetTrackerClass.DefineActionItem("")
