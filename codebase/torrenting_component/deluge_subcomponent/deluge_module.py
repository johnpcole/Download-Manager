from . import deluge_class as DelugeInterfaceClass



# ---------------------------------------------
# Builds a DelugeRPCClient object
# ---------------------------------------------

def createinterface(address, port, username, password):
	return DelugeInterfaceClass.DefineDelugeInterface(address, port, username, password)


