from ..enumeration_datatype import enumeration_module as Enumeration
from ..datetime_datatypes import datetime_module as DateTime
from ..filesystem_framework import filesystem_module as FileSystem


class DefineQueue:

	def __init__(self, location, role):

		self.location = location

		self.role = Enumeration.createenum(["Queuer", "Reader"], role)



	def createqueueditem(self, data):

		if self.role.get("Queuer") is True:
			fullfilepath = FileSystem.concatenatepaths(self.location, self.getuniquefileid())
			FileSystem.writejsontodisk(FileSystem.doesexist(fullfilepath + ".draft"), data)
			FileSystem.movefile(fullfilepath + ".draft", fullfilepath + ".queued")

		else:
			assert(1 == 0, "Cannot add a queued item when the role is not Queuer")


	def getuniquefileid(self):

		outcome = ""
		while outcome == "":
			currenttime = DateTime.getnow()
			draftfilename = currenttime.getiso()
			fullfilepath = FileSystem.concatenatepaths(self.location, draftfilename)
			if (FileSystem.doesexist(fullfilepath + ".queued") == False):
				if (FileSystem.doesexist(fullfilepath + ".draft") == False):
					if (FileSystem.doesexist(fullfilepath + ".processed") == False):
						if (FileSystem.doesexist(fullfilepath + ".ignored") == False):
							outcome = draftfilename

		print("UNIQUE FILE ID FOR QUEUE: ",outcome)
		return outcome



	def getqueueend(self, which):

		latestallowedtime = DateTime.getnow()
		latestallowedtime.adjustseconds(-1)
		filelisting = FileSystem.getfolderlisting(self.location)
		oldestqueuedfile = "29991231235959"
		newestqueuedfile = "19991231235959"
		for filenameandextension in filelisting.keys():
			if FileSystem.getextension(filenameandextension) == "queued":
				filename = FileSystem.getname(filenameandextension)
				if (oldestqueuedfile > filename) or (filename > newestqueuedfile):
					fullfilepath = FileSystem.concatenatepaths(self.location, filenameandextension)
					filedatetime = FileSystem.getmodifytimedate(fullfilepath)
					if DateTime.isfirstlaterthansecond(latestallowedtime, filedatetime) == True:
						if oldestqueuedfile > filename:
							oldestqueuedfile = filename
						if newestqueuedfile < filename:
							newestqueuedfile = filename
		if which == "oldest":
			if oldestqueuedfile == "29991231235959":
				outcome = ""
			else:
				outcome = oldestqueuedfile
		else:
			if oldestqueuedfile == "19991231235959":
				outcome = ""
			else:
				outcome = newestqueuedfile

		return outcome


	def getqueuebacklog(self, latestfilename):
		outcome = []
		filelisting = FileSystem.getfolderlisting(self.location)
		for filenameandextension in filelisting.keys():
			if FileSystem.getextension(filenameandextension) == "queued":
				filename = FileSystem.getname(filenameandextension)
				if latestfilename > filename:
					outcome.append(FileSystem.concatenatepaths(self.location, filename))

		return outcome




	def readfromqueue(self):

		outcome = {}
		if self.role.get("Reader") is True:
			selectedfile = self.getqueueend("oldest")
			if selectedfile != "":
				fullfilepath = FileSystem.concatenatepaths(self.location, selectedfile)
				outcome['result'] = FileSystem.readjsonfromdisk(fullfilepath + ".queued")
				FileSystem.movefile(fullfilepath + ".queued", fullfilepath + ".processed")
		else:
			assert (1 == 0, "Cannot read from queue when the role is not Reader")

		return outcome




	def readqueuelatest(self):

		outcome = {}
		if self.role.get("Reader") is True:
			selectedfile = self.getqueueend("newest")
			if selectedfile != "":
				fullfilepath = FileSystem.concatenatepaths(self.location, selectedfile)
				outcome['result'] = FileSystem.readjsonfromdisk(fullfilepath + ".queued")
				FileSystem.movefile(fullfilepath + ".queued", fullfilepath + ".processed")
				ignorelist = self.getqueuebacklog(selectedfile)
				for fullfilepath in ignorelist:
					FileSystem.movefile(fullfilepath + ".queued", fullfilepath + ".ignored")
		else:
			assert (1 == 0, "Cannot read from queue when the role is not Reader")

		return outcome




	def cleanupqueue(self):

		if self.role.get("Reader") is True:
			latestallowedtime = DateTime.getnow()
			latestallowedtime.adjusthours(-24)
			filelisting = FileSystem.getfolderlisting(self.location)
			for filenameandextension in filelisting.keys():
				fileextension = FileSystem.getextension(filenameandextension)
				if (fileextension == "processed") or (fileextension == "ignored"):
					fullfilepath = FileSystem.concatenatepaths(self.location, filenameandextension)
					filedatetime = FileSystem.getmodifytimedate(fullfilepath)
					if DateTime.isfirstlaterthansecond(latestallowedtime, filedatetime) == True:
						FileSystem.deletefile(fullfilepath)




