from . import databaseconnection_class as DatabaseConnectionClass


def createdatabaseconnection(databasefilename, turn):
	return DatabaseConnectionClass.DefineDatabaseConnection(databasefilename, turn)


