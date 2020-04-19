from . import database_class as DatabaseClass


def createdatabase(databasefilename):
	return DatabaseClass.DefineDatabase(databasefilename)


