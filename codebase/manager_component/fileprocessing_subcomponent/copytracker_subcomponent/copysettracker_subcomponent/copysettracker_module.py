from . import copysettracker_class as CopySetTrackerClass


def createtorrentcopytracker(torrentid):
	return CopySetTrackerClass.DefineSetTracker(torrentid, "< DONT IGNORE ANYTHING >")

def createglobalcopytracker(ignoreid):
	return CopySetTrackerClass.DefineSetTracker("< ALL TORRENTS >", ignoreid)
