from ..enumeration_datatype import enumeration_module as Enumeration
from ..datetime_datatypes import datetime_module as DateTime
from ..filesystem_framework import filesystem_module as FileSystem


class DefineQueue:

	def __init__(self, location, role):

		self.location = location

		self.role = Enumeration.createenum(["Queuer", "Reader"], role)



	def createqueueditem(self, data):

		if self.role.get("Queuer") is True:
			duplicatefilename = True
			fullfilepath = "./"
			while duplicatefilename == True:
				currenttime = DateTime.getnow()
				draftfilename = currenttime.getiso()
				fullfilepath = FileSystem.concatenatepaths(self.location, draftfilename)
				if (FileSystem.doesexist(fullfilepath + ".queued") == False):
					if (FileSystem.doesexist(fullfilepath + ".draft") == False):
						if (FileSystem.doesexist(fullfilepath + ".processed") == False):
							duplicatefilename = False
			FileSystem.writejsontodisk(FileSystem.doesexist(fullfilepath + ".draft"), data)
			FileSystem.movefile(fullfilepath + ".draft", fullfilepath + ".queued")

		else:
			assert(1 == 0, "Cannot add a queued item when the role is not Queuer")



	def readfromqueue(self):

		if self.role.get("Reader") is True:
			latestallowedtime = DateTime.getnow()
			latestallowedtime.adjustseconds(-1)
			filelisting = FileSystem.getfolderlisting(self.location)
			oldestqueuedfile = "29991231235959"
			for filenameandextension in filelisting.keys():
				if FileSystem.getextension(filenameandextension) == "queued":
					filename = FileSystem.getname(filenameandextension)
					if oldestqueuedfile > filename:
						fullfilepath = FileSystem.concatenatepaths(self.location, filenameandextension)
						filedatetime = FileSystem.getmodifytimedate(fullfilepath)
						if DateTime.isfirstlaterthansecond(latestallowedtime, filedatetime) == True:
							oldestqueuedfile = filename
			if oldestqueuedfile == "29991231235959":
				outcome = []
			else:
				fullfilepath = FileSystem.concatenatepaths(self.location, oldestqueuedfile)
				outcome = FileSystem.readjsonfromdisk(fullfilepath + ".queued")
				FileSystem.movefile(fullfilepath + ".queued", fullfilepath + ".processed")
		else:
			assert (1 == 0, "Cannot read from queue when the role is not Reader")
			outcome = []

		return outcome




	def cleanupqueue(self):

		if self.role.get("Reader") is True:
			latestallowedtime = DateTime.getnow()
			latestallowedtime.adjusthours(-24)
			filelisting = FileSystem.getfolderlisting(self.location)
			for filenameandextension in filelisting.keys():
				if FileSystem.getextension(filenameandextension) == "processed":
					fullfilepath = FileSystem.concatenatepaths(self.location, filenameandextension)
					filedatetime = FileSystem.getmodifytimedate(fullfilepath)
					if DateTime.isfirstlaterthansecond(latestallowedtime, filedatetime) == True:
						FileSystem.deletefile(fullfilepath)




