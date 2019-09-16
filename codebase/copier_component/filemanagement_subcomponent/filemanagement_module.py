from . import filemanagement_class as FileManagerClass


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createmanager(connectioncredentials, connectiontries):
	return FileManagerClass.DefineFileManager(connectioncredentials, connectiontries)


