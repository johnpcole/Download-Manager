from . import serverconnection_class as ServerConnectionClass


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createconnection(connectioncredentials, connectiontries):
	return ServerConnectionClass.DefineConnection(connectioncredentials['Mountpoint'],
												connectioncredentials['Address'],
												connectioncredentials['Username'],
												connectioncredentials['Password'],
												connectiontries)


