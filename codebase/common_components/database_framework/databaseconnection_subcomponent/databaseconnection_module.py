from . import databaseconnection_class as DatabaseConnectionClass


def createdatabaseconnection(databasefilename):
	return DatabaseConnectionClass.DefineDatabaseConnection(databasefilename)


