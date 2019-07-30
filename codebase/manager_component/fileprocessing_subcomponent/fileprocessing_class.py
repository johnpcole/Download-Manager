from .copiertracker_subcomponent import copiertracker_module as CopierTracker
from .tvshows_subcomponent import tvshows_module as TVShows



class DefineLibraryManager:

	def __init__(self):

		self.tvshows = TVShows.createtvshows()

		self.copiertracker = CopierTracker.createtracker()

# =========================================================================================
# Connects to the file server, and compiles a list of tv shows and seasons to store locally
# =========================================================================================

	def discovertvshows(self):

		self.copiertracker.queuefolderrefresh()


# =========================================================================================
# Returns the list of season names for the specified tv show
# =========================================================================================

	def gettvshowseasons(self, tvshowname):

		return self.tvshows.gettvshowseasons(tvshowname)


# =========================================================================================
# Returns all the drop-down list options for the specified tv show
# =========================================================================================

	def getdropdownlists(self, tvshowname):

		return self.tvshows.getdropdownlists(tvshowname)



# =========================================================================================

	def queuefilecopy(self, newcopyactions):

		self.copiertracker.queuenewfilecopyactions(newcopyactions)


# =========================================================================================

	def processnextcopyaction(self):

		return self.copiertracker.startnextcopieraction()


# =========================================================================================

	def importcopieroutcome(self, copyid, newstatus, resultdetail):

		self.copiertracker.updatecopieractionwithresult(copyid, newstatus, resultdetail)

		if self.copiertracker.shouldrefreshtvshowdata(copyid) is True:
			self.tvshows.importtvshows(resultdetail)


	def getcopierpageload(self, torrentidlist):

		return self.copiertracker.getcopierpagedata(torrentidlist, "initialise")

	def getcopierpageupdate(self):

		return self.copiertracker.getcopierpagedata({}, "refresh")

	def gettorrentcopystate(self, torrentid):

		return self.copiertracker.getcopysetstate(torrentid)

	def getoverallcopierstate(self):

		return self.copiertracker.getcopysetstate("")





