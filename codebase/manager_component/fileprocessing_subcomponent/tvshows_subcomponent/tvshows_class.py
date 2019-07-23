from ....common_components.dataconversion_framework import dataconversion_module as Functions

class DefineTVShows:

	def __init__(self):

		self.tvshows = {}

		self.episodes = []

		self.subtitles = []

		self.discoverepisodes()
		self.discoversubtitles()

# =========================================================================================
# Connects to the file server, and compiles a list of tv shows and seasons to store locally
# =========================================================================================

	def importtvshows(self, newdictionary):

		self.tvshows = newdictionary

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
