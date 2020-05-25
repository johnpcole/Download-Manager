from . import filesystem_module as FileSystem
from ..logging_framework import logging_module as Logging
from json import dumps as MakeJson


def readconfigurationfile(filepath, configlist):
	if FileSystem.doesexist(filepath):
		credentials = FileSystem.readfromdisk(filepath)
		outcome = {}
		configcount = 0
		for configitem in configlist:
			outcome[configitem] = credentials[configcount]
			configcount = configcount + 1
	else:
		Logging.printout("Cannot find configuration file " + filepath)
		outcome = {}
	return outcome


def readgeneralfile(filepath):
	if FileSystem.doesexist(filepath):
		outcome = FileSystem.readfromdisk(filepath)
	else:
		Logging.printout("Cannot find configuration file " + filepath)
		outcome = []
	return outcome


def writejsonfile(filepath, datalibrary):
	FileSystem.writetodisk(filepath, MakeJson(datalibrary), "Overwrite")

