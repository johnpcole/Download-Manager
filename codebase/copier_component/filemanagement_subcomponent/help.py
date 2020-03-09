from .filesystem_subcomponent import filesystem_module as FileSystem
from .copyaction_subcomponent import copyaction_module as CopyAction
from ..common_components.dataconversion_framework import dataconversion_module as Functions

class DefineLibraryManager:

	def __init__(self, mountpoint, networkpath, username, password):

		self.tvshows = {}

		self.episodes = []

		self.subtitles = []

		self.mountpoint = mountpoint

		self.networkpath = networkpath

		self.username = username

		self.password = password

		self.copyactions = []

		self.discovertvshows()
		self.discoverepisodes()
		self.discoversubtitles()

# =========================================================================================
# Connects to the file server, and compiles a list of tv shows and seasons to store locally
# =========================================================================================

	def discovertvshows(self):

		self.tvshows = {}
		FileSystem.mountnetworkdrive(self.mountpoint, self.networkpath, self.username, self.password, "Discover TV Shows")
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
				for key in sorted(seasonlist, reverse = True):
					orderedlist.append(seasonlist[key])
				self.tvshows[rootitem] = orderedlist
		FileSystem.unmountnetworkdrive(self.mountpoint)

# =========================================================================================
# Returns the list of tv shows and seasons
# =========================================================================================

	def gettvshowlists(self):

		return self.tvshows

# =========================================================================================
# Returns the list of tv show names
# =========================================================================================

	def gettvshows(self):

		newshowlist = []
		for showitem in self.tvshows.keys():
			newshowlist.append(Functions.dearticle(showitem))
		sortednewshowlist = sorted(newshowlist)
		outcome = []
		for showitem in sortednewshowlist:
			outcome.append(Functions.rearticle(showitem))

		return outcome

# =========================================================================================
# Returns the list of season names for the specified tv show
# =========================================================================================

	def gettvshowseasons(self, tvshowname):

		if tvshowname in self.tvshows:
			outcome = self.tvshows[tvshowname]
		else:
			outcome = []
		return outcome

# =========================================================================================
# Returns all the drop-down list options for the specified tv show
# =========================================================================================

	def getdropdownlists(self, tvshowname):

		outcome = {}
		outcome['tvshows'] = self.gettvshows()
		outcome['episodes'] = self.episodes
		outcome['subtitles'] = self.subtitles
		outcome['tvshowseasons'] = self.gettvshowseasons(tvshowname)
		return outcome

# =========================================================================================
# Generates a list of episodes for the episode drop-down list
# =========================================================================================

	def discoverepisodes(self):

		for x in range(1, 41):
			self.episodes.append("Episode "+str(x))
		for x in range(1, 40):
			self.episodes.append("Ep. "+str(x)+" & "+str(x+1))
		for x in range(1, 100):
			self.episodes.append("Special "+str(x))

# =========================================================================================
# Generates a list of subtitle types for the subtitle drop-down list
# =========================================================================================

	def discoversubtitles(self):

		self.subtitles.append("Standard")
		self.subtitles.append("English")
		self.subtitles.append("SDH")
		self.subtitles.append("Eng-SDH")

# =========================================================================================

	def queuefilecopy(self, copyactions):

		if copyactions == []:
			print("No copy actions to perform this time")
		else:
			self.copyactions = []

			self.copyactions.append(CopyAction.createconnectaction())

			for action in copyactions:
				copysource = FileSystem.createpathfromlist(action['source'])
				rawtarget = FileSystem.createpathfromlist(action['target'])
				copytarget = FileSystem.concatenatepaths(self.mountpoint, rawtarget)
				self.copyactions.append(CopyAction.createcopyaction(copysource, copytarget, action['size'], rawtarget))

			self.copyactions.append(CopyAction.createdisconnectaction())


# =========================================================================================

	def getcopyprocessinfo(self):

		copystates = []
		for copyaction in self.copyactions:
			copystates.append(copyaction.getinfo())

		return copystates



# =========================================================================================

	def processfilecopylist(self):

		continueprocessing = False

		actionoutcome = self.processstartedfilecopyaction()

		startnewitem = True
		for copyitem in self.copyactions:
			if copyitem.getstatus() == "copying":
				startnewitem = False

		if startnewitem is True:
			for copyitem in self.copyactions:
				if continueprocessing is False:
					if copyitem.startaction() is True:
						continueprocessing = True

		if actionoutcome is True:
			continueprocessing = True

		return continueprocessing



# =========================================================================================

	def processstartedfilecopyaction(self):

		anychange = False
		for copyitem in self.copyactions:
			if copyitem.getstatus() == "copying":
				anychange = True

				if copyitem.getactiontype() == "Connect":
					actionoutcome = FileSystem.mountnetworkdrive(self.mountpoint, self.networkpath, self.username, self.password, "Copy Files")
				elif copyitem.getactiontype() == "Disconnect":
					actionoutcome = FileSystem.unmountnetworkdrive(self.mountpoint)
				else:
					actionoutcome = FileSystem.copyfile(copyitem.getsource(), copyitem.gettarget())

				copyitem.updateaction(actionoutcome)

		return anychange

