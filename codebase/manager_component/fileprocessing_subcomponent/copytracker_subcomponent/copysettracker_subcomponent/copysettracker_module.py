from . import copysettracker_class as CopySetTrackerClass


def createtorrentcopytracker(torrentid):
	return CopySetTrackerClass.DefineSetTracker(torrentid, "")

def createglobalcopytracker(ignoreid):
	return CopySetTrackerClass.DefineSetTracker("", ignoreid)
