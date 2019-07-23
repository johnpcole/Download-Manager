from .copytracker_subcomponent import copytracker_module as CopyTracker
from .tvshows_subcomponent import tvshows_module as TVShows



class DefineLibraryManager:

	def __init__(self):

		self.tvshows = TVShows.createtvshows()

		self.copytracker = CopyTracker.createtracker()

# =========================================================================================
# Connects to the file server, and compiles a list of tv shows and seasons to store locally
# =========================================================================================

	def discovertvshows(self):

		self.copytracker.queuefolderrefresh()


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

		self.copytracker.queuenewactions(newcopyactions)


# =========================================================================================

	def processnextcopyaction(self):

		return self.copytracker.startnextaction()


# =========================================================================================

	def importcopieroutcome(self, copyid, newstatus, notes):

		refreshdata = self.copytracker.updatecopyaction(copyid, newstatus)
		if refreshdata is True:
			self.tvshows.importtvshows(notes)



	def getcopierpagedata(self):

		return self.copytracker.getcopierpagedata()

	def getcopierpageupdatedata(self):

		return self.copytracker.getcopierpageupdatedata()






