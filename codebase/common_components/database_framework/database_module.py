from . import database_class as DatabaseClass

def createdatbase(databasefile):
	return DatabaseClass.DefineDatabase(databasefile)


