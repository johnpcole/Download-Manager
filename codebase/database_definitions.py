from .common_components.database_framework import database_module as Database

def createoperatoractionsdatabase():

	actionsqueue = Database.createdatabase('./data/application_memory/operator_actions.sqlite')

	actionsqueue.adddatabasestructure('queuedaction', 'actionid', 'CHAR(20)', False, True)
	actionsqueue.adddatabasestructure('queuedaction', 'actiontype', 'CHAR(6)', False, False)
	actionsqueue.adddatabasestructure('queuedaction', 'context', 'CHAR(40)', True, False)

	actionsqueue.changedatabasestate('Live')

	actionsqueue.createentiredatabase()

	return actionsqueue



def createoperatorresultsdatabase():

	actionresults = Database.createdatabase('./data/application_memory/operator_results.sqlite')

	actionresults.adddatabasestructure('processedaction', 'actionid', 'CHAR(20)', False, True)
	actionresults.adddatabasestructure('torrent', 'torrentid', 'CHAR(40)', False, True)
	actionresults.adddatabasestructure('torrent', 'torrentstats', 'TEXT', True, False)
	actionresults.adddatabasestructure('torrent', 'lastseen', 'CHAR(14)', False, False)
	actionresults.adddatabasestructure('session', 'sessionstat', 'CHAR(20)', False, True)
	actionresults.adddatabasestructure('session', 'sessionvalue', 'CHAR(20)', True, False)

	actionresults.changedatabasestate('Live')

	actionresults.createentiredatabase()

	return actionresults



def createtorrentconfigsdatabase():

	torrentconfigs = Database.createdatabase('./data/application_memory/torrent_configs.sqlite')

	torrentconfigs.adddatabasestructure('torrent', 'torrentid', 'CHAR(40)', False, True)
	torrentconfigs.adddatabasestructure('torrent', 'torrenttype', 'CHAR(10)', False, False)
	torrentconfigs.adddatabasestructure('torrent', 'torrentname', 'CHAR(100)', True, False)
	torrentconfigs.adddatabasestructure('torrent', 'torrentseasonyear', 'CHAR(10)', True, False)
	torrentconfigs.adddatabasestructure('file', 'fileid', 'CHAR(4)', False, False)
	torrentconfigs.adddatabasestructure('file', 'torrentid', 'CHAR(40)', False, False)
	torrentconfigs.adddatabasestructure('file', 'torrentfileid', 'CHAR(45)', False, True)
	torrentconfigs.adddatabasestructure('file', 'filepurpose', 'CHAR(30)', True, False)

	torrentconfigs.changedatabasestate('Live')

	torrentconfigs.createentiredatabase()

	return torrentconfigs


