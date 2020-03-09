from ....common_components.filesystem_framework import filesystem_module as FileSystem



class DefineConnection:

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
			if self.determineconnectionstate() is True:
				tries = 9999
			else:
				connectionoutcome = FileSystem.mountnetworkdrive(self.mountpoint, self.networkpath, self.username,
																										self.password)
				tries = tries + 1

		if tries == 9999:
			outcome = True

		return outcome



	def disconnectfileserver(self):

		outcome = False
		tries = 0
		while tries < self.retrylimit:
			if self.determineconnectionstate() is False:
				tries = 9999
			else:
				connectionoutcome = FileSystem.unmountnetworkdrive(self.mountpoint)
				tries = tries + 1

		if tries == 9999:
			outcome = True

		return outcome



	def determineconnectionstate(self):

		outcome = False
		if FileSystem.doesexist(FileSystem.concatenatepaths(self.mountpoint, "TV Shows")) is True:
			if FileSystem.doesexist(FileSystem.concatenatepaths(self.mountpoint, "Movies")) is True:
				outcome = True

		return outcome



	def getserverpath(self, subfolder):

		return FileSystem.concatenatepaths(self.mountpoint, subfolder)



