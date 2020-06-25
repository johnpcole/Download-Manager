from ..enumeration_datatype import enumeration_module as Enumeration
from ..datetime_datatypes import datetime_module as DateTime
from ..filesystem_framework import filesystem_module as FileSystem


class DefineQueue:

	def __init__(self, location, role, hourstimelimit):

		self.location = location

		self.role = Enumeration.createenum(["Queuer", "Reader"], role)

		self.queuetimelimit = 0 - hourstimelimit



	def createqueueditem(self, data):

		if self.role.get("Queuer") is True:
			self.cleanupqueue()
			fullfilepath = FileSystem.concatenatepaths(self.location, self.getuniquefileid())
			FileSystem.writejsontodisk(fullfilepath + ".draft", data)
			FileSystem.movefile(fullfilepath + ".draft", fullfilepath + ".queued")

		else:
			print("Cannot add a queued item when the role is not Queuer")



	def getuniquefileid(self):

		outcome = ""
		currenttime = DateTime.getnow()
		currenttimetext = currenttime.getiso()
		draftfilenameprefix = currenttimetext[:8] + "_" + currenttimetext[-6:]
		indexer = -1
		while outcome == "":
			indexer = indexer + 1
			if indexer < 1000:
				draftfilenamesuffix = "0000" + str(indexer)
				draftfilename = draftfilenameprefix + "_" + draftfilenamesuffix[-3:]
				fullfilepath = FileSystem.concatenatepaths(self.location, draftfilename)
				if (FileSystem.doesexist(fullfilepath + ".queued") == False):
					if (FileSystem.doesexist(fullfilepath + ".draft") == False):
						if (FileSystem.doesexist(fullfilepath + ".processed") == False):
							if (FileSystem.doesexist(fullfilepath + ".ignored") == False):
								outcome = draftfilename
			else:
				print("Run out of unique file ids for " + draftfilenameprefix + ". Trying again...")
				outcome = self.getuniquefileid()

		return outcome



	def getqueueend(self, whichend):

		outcome = ""
		latestallowedtime = DateTime.getnow()
		latestallowedtime.adjustseconds(-1)
		filelisting = FileSystem.getfolderlisting(self.location)
		oldestqueuedfile = "29991231_235959_000"
		newestqueuedfile = "19991231_235959_000"
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
		if whichend == "oldest":
			if oldestqueuedfile != "29991231_235959_000":
				outcome = oldestqueuedfile
		else:
			if newestqueuedfile != "19991231_235959_000":
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

		outcome = None
		if self.role.get("Reader") is True:
			selectedfile = self.getqueueend("oldest")
			if selectedfile != "":
				fullfilepath = FileSystem.concatenatepaths(self.location, selectedfile)
				outcome = FileSystem.readjsonfromdisk(fullfilepath + ".queued")
				FileSystem.movefile(fullfilepath + ".queued", fullfilepath + ".processed")
		else:
			print("Cannot read from queue when the role is not Reader")

		return outcome



	def readqueuelatest(self):

		outcome = None
		if self.role.get("Reader") is True:
			selectedfile = self.getqueueend("newest")
			if selectedfile != "":
				fullfilepath = FileSystem.concatenatepaths(self.location, selectedfile)
				outcome = FileSystem.readjsonfromdisk(fullfilepath + ".queued")
				FileSystem.movefile(fullfilepath + ".queued", fullfilepath + ".processed")
				ignorelist = self.getqueuebacklog(selectedfile)
				for fullfilepath in ignorelist:
					FileSystem.movefile(fullfilepath + ".queued", fullfilepath + ".ignored")
		else:
			print("Cannot read from queue when the role is not Reader")

		return outcome



	def cleanupqueue(self):

		if self.role.get("Reader") is True:
			latestallowedtime = DateTime.getnow()
			latestallowedtime.adjusthours(self.queuetimelimit)
			filelisting = FileSystem.getfolderlisting(self.location)
			for filenameandextension in filelisting.keys():
				fileextension = FileSystem.getextension(filenameandextension)
				if (fileextension == "processed") or (fileextension == "ignored"):
					fullfilepath = FileSystem.concatenatepaths(self.location, filenameandextension)
					filedatetime = FileSystem.getmodifytimedate(fullfilepath)
					if DateTime.isfirstlaterthansecond(latestallowedtime, filedatetime) is True:
						FileSystem.deletefile(fullfilepath)




