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

		return self.tvshows.discovertvshows()


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

	def updatecopyactionstatus(self, copyid, newstatus):

		self.copytracker.updateactionstatus(copyid, newstatus)



