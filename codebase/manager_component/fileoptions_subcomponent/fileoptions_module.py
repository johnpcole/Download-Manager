from . import fileoptions_class as FileOptionsClass


# =========================================================================================
# Creates the Library object, which contains file server connectivity data,
# as well as lists of tv shows, and processes copy actions
# =========================================================================================

def createfileoptions():
	return FileOptionsClass.DefineFileOptions()


