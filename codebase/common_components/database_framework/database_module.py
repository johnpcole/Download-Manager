from . import database_class as DatabaseClass


def createdatabase(databasefilename):
	return DatabaseClass.DefineDatabase(databasefilename, 0)


def createshareddatabase(databasefilename, turn):
	return DatabaseClass.DefineDatabase(databasefilename, turn)

