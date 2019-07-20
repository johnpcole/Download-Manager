from . import manager_class as ManagerClass

def createmanager(setname):

	return ManagerClass.DefineTorrentSet(setname)

