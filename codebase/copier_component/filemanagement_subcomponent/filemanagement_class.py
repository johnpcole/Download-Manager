from ...common_components.filesystem_framework import filesystem_module as FileSystem




class DefineFileManager:

	def __init__(self, mountpoint, networkpath, username, password, connectiontries):

		self.mountpoint = mountpoint

		self.networkpath = networkpath

		self.username = username

		self.password = password

		self.retrylimit = connectiontries





	def connecttofileserver(self, reason):

		outcome = False
		tries = 0
		while tries < self.retrylimit:
			if self.determineconnectionstate() == True:
				tries = 9999
			else:
				actionoutcome = FileSystem.mountnetworkdrive(self.mountpoint, self.networkpath, self.username,
																								self.password, reason)
				tries = tries + 1

		if tries == 9999:
			outcome = True

		return outcome



	def disconnectfileserver(self):

		outcome = False
		tries = 0
		while tries < self.retrylimit:
			if self.determineconnectionstate() == False:
				tries = 9999
			else:
				actionoutcome = FileSystem.unmountnetworkdrive(self.mountpoint)
				tries = tries + 1

		if tries == 9999:
			outcome = True

		return outcome



	def determineconnectionstate(self):

		outcome = False
		if FileSystem.doesexist(FileSystem.concatenatepaths(self.mountpoint, "TV Shows")) == True:
			if FileSystem.doesexist(FileSystem.concatenatepaths(self.mountpoint, "Movies")) == True:
				outcome = True

		return outcome



	def performcopy(self, sourcelocation, targetsublocation, forcemode):

		outcome = "Failed"
		targetlocation = FileSystem.concatenatepaths(self.mountpoint, targetsublocation)
		connectionoutcome = self.connecttofileserver("Copy Files")
		proceedwithcopy = False

		if connectionoutcome == True:

			if FileSystem.doesexist(targetlocation) == True:
				if forcemode == True:
					proceedwithcopy = True
				else:
					outcome = "Confirm"
			else:
				proceedwithcopy = True

		if proceedwithcopy == True:
			actionoutcome = self.copyafile(sourcelocation, targetlocation)
			if actionoutcome == True:
				outcome = "Succeeded"

		return outcome



	def copyafile(self, sourcelocation, targetlocation):

		outcome = False
		tries = 0
		while tries < self.retrylimit:
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

		connectionoutcome = self.connecttofileserver("Scrape TV Shows")
		if connectionoutcome == True:
			rootfolder = FileSystem.concatenatepaths(self.mountpoint, "TV Shows")
			rootlisting = FileSystem.getfolderlisting(rootfolder)
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

		return tvshows


