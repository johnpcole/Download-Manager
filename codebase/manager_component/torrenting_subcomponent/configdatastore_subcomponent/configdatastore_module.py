from . import configdatastore_class as TorrentConfigsDatastore


def createtorrentconfigdatabase():
	return TorrentConfigsDatastore.DefineTorrentConfigsDatabase()


