from . import delugeinterface_class as DelugeInterfaceClass


def createinterface(connectioncredentials):
	return DelugeInterfaceClass.DefineDelugeInterface(connectioncredentials['Address'], connectioncredentials['Port'],
												connectioncredentials['Username'], connectioncredentials['Password'])
