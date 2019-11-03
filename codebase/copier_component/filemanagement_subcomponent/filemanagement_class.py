from ...common_components.filesystem_framework import filesystem_module as FileSystem
from ...common_components.logging_framework import logging_module as Logging
from .serverconnection_subcomponent import serverconnection_module as ServerConnection
from ...common_components.datetime_datatypes import datetime_module as DateTime



class DefineFileManager:

	def __init__(self, connectioncredentials, connectiontries):

		self.serverconnection = ServerConnection.createconnection(connectioncredentials, connectiontries)

		self.copyretrylimit = connectiontries




	def performcopy(self, sourcelocation, targetsublocation, forcemode):

		outcome = "Failed"
		copydetail = {}

		targetlocation = self.serverconnection.getserverpath(targetsublocation)
		connectionoutcome = self.serverconnection.connecttofileserver("Copy Files")
		proceedwithcopy = False

		copydetail["Source File"] = self.getfiledetails(sourcelocation)

		if connectionoutcome == True:

			if FileSystem.doesexist(targetlocation) == True:
				copydetail["Existing File"] = self.getfiledetails(targetlocation)
				if forcemode == True:
					proceedwithcopy = True
				else:
					outcome = "Confirm"
			else:
				proceedwithcopy = True
		else:
			copydetail["Error"] = "Cannot connect to Server"


		if proceedwithcopy == True:
			actionoutcome = self.copyafile(sourcelocation, targetlocation)
			if actionoutcome == True:
				outcome = "Succeeded"
				copydetail["New Copied File"] = self.getfiledetails(targetlocation)
			else:
				copydetail["Error"] = "Cannot copy file"

		return {"outcome": outcome, "feedback": copydetail}



	def copyafile(self, sourcelocation, targetlocation):

		space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
		arrows = space + space + "&darr;"
		indent = space + space + space + space + space
		lineofarrows = arrows + arrows + arrows + arrows + arrows
		Logging.printout(
			"Copying File:&nbsp;" + space + sourcelocation + "</br>" + indent + lineofarrows
																					+ "</br>" + indent + targetlocation)

		outcome = False
		tries = 0
		while tries < self.copyretrylimit:
			actionoutcome = FileSystem.copyfile(sourcelocation, targetlocation)
			if actionoutcome == 0:  # OS returns zero if successful
				tries = 9999
			else:
				tries = tries + 1

		if tries == 9999:
			outcome = True

		return outcome



	def scrapetvshows(self):

		tvshows = {}
		outcome = "Failed"
		connectionoutcome = self.serverconnection.connecttofileserver("Scrape TV Shows")
		if connectionoutcome == True:
			rootfolder = self.serverconnection.getserverpath("TV Shows")
			rootlisting = FileSystem.getfolderlisting(rootfolder)
			outcome = "Succeeded"
			for rootitem in rootlisting:
				if rootlisting[rootitem] == "Folder":
					subfolder = FileSystem.concatenatepaths(rootfolder, rootitem)
					sublisting = FileSystem.getfolderlisting(subfolder)
					seasonlist = {}
					for subitem in sublisting:
						if sublisting[subitem] == "Folder":
							if subitem[:7] == "Season ":
								seasonindex = ("000" + subitem[7:])[-2:]
								seasonlist[seasonindex] = subitem
							elif subitem[:7] == "Special":
								seasonlist["000"] = subitem
					orderedlist = []
					for key in sorted(seasonlist, reverse=True):
						orderedlist.append(seasonlist[key])
					tvshows[rootitem] = orderedlist

		return {"outcome": outcome, "feedback": tvshows}



	def gotosleep(self):

		self.serverconnection.disconnectfileserver()


	def getfiledetails(self, fullpath):

		try:
			rawfilesize = FileSystem.getsize(fullpath)
			rawdatetime = FileSystem.getmodifytimedate(fullpath)

			filedatetime = DateTime.createfromsextuplet(rawdatetime["Day"], rawdatetime["Month"], rawdatetime["Year"],
													rawdatetime["Hour"], rawdatetime["Minute"], rawdatetime["Second"])

		except:
			rawfilesize = 0
			filedatetime = DateTime.createfromsextuplet(1, 1, 2000, 0, 0, 0)

		return {'datetime': filedatetime.getiso(), 'filesize': rawfilesize}


