from . import manager_class as ManagerClass

def createmanager(copierhistory, copieractionqueue, filesystemdataqueue, operatoractionqueue, sessiondataqueue,
																								torrentconfigurations):

	return ManagerClass.DefineTorrentSet(copierhistory, copieractionqueue, filesystemdataqueue, operatoractionqueue,
																				sessiondataqueue, torrentconfigurations)

