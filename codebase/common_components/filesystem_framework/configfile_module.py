from . import filesystem_module as FileSystem

def readconfigurationfile(filepath, configlist):
	credentials = FileSystem.readfromdisk(filepath)
	outcome = {}
	configcount = 0
	for configitem in configlist:
		outcome[configitem] = credentials[configcount]
		configcount = configcount + 1
	return outcome




