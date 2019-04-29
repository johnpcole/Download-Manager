from ....functions_component import functions_module as Functions


# This class creates an object which is used to capture information about an individual torrent that is captured
# or managed within the Deluge Daemon - This is the data that Download-Manager manages
# The object contains enough information to determine what folder any files should be copied to
# and allows for file data to be read/written in a file friendly format

class DefineCategory:

	def __init__(self):

		# Determines whether the torrent is a TV Show, Movie or Other (string)
		self.torrenttype = "Unknown"

		# The specified movie name, or tv show name (string)
		self.movieorshowname = ""

		# The specified movie year, or tv show season (???)
		self.seasonoryear = ""


# =========================================================================================
# Returns the torrent type as a string
# =========================================================================================

	def gettype(self):

		return self.torrenttype



# =========================================================================================
# If the torrent is a movie, returns the movie name (string)
# Otherwise return blank (string)
# =========================================================================================

	def getmoviename(self):

		if self.torrenttype == "movie":
			outcome = self.movieorshowname
		else:
			outcome = ""
		return outcome



# =========================================================================================
# If the torrent is a tv show, returns the tv show name (string)
# Otherwise return blank (string)
# =========================================================================================

	def getshowname(self):

		if self.torrenttype == "tvshow":
			outcome = self.movieorshowname
		else:
			outcome = ""
		return outcome



# =========================================================================================
# If the torrent is a tv show, returns the tv show season (???)
# Otherwise return blank (string)
# =========================================================================================

	def getseason(self):

		if self.torrenttype == "tvshow":
			outcome = self.seasonoryear
		else:
			outcome = ""
		return outcome



# =========================================================================================
# If the torrent is a movie, returns the movie year (???)
# Otherwise return blank (string)
# =========================================================================================

	def getyear(self):

		if self.torrenttype == "movie":
			outcome = self.seasonoryear
		else:
			outcome = ""
		return outcome



# =========================================================================================
# Returns the name, whether tv show or movie (string)
# =========================================================================================

	def gettorrenttitle(self, episodesuffix):

		if self.movieorshowname == "":
			outcome = "New Unspecified Torrent"
		else:
			outcome = self.movieorshowname

		if episodesuffix == "":
			suffix = self.seasonoryear
		else:
			suffix = episodesuffix

		if suffix != "":
			outcome = outcome + " - " + suffix

		return outcome



# =========================================================================================
# Sets the torrentype (string)
# =========================================================================================

	def settype(self, newvalue):

		if (newvalue == "tvshow") or (newvalue == "movie") or (newvalue == "unknown"):
			self.torrenttype = newvalue
		else:
			assert 1 == 0, "Inappropriate Torrent Type " + newvalue




# =========================================================================================
# If the torrent is a movie, sets the movie name (string)
# =========================================================================================

	def setmoviename(self, newvalue):

		if self.torrenttype != "movie":
			assert 1 == 0, "Cannot set movie name for non-movie"
		self.movieorshowname = newvalue



# =========================================================================================
# If the torrent is a tv show, sets the tv show name (string)
# =========================================================================================

	def setshowname(self, newvalue):

		if self.torrenttype != "tvshow":
			assert 1 == 0, "Cannot set show name for non-tv-show"
		self.movieorshowname = newvalue



# =========================================================================================
# If the torrent is a tv show, sets the tv show season (???)
# =========================================================================================

	def setseason(self, newvalue):

		if self.torrenttype != "tvshow":
			assert 1 == 0, "Cannot set season for non-tv-show"
		self.seasonoryear = newvalue



# =========================================================================================
# If the torrent is a movie, sets the movie year (???)
# =========================================================================================

	def setyear(self, newvalue):

		if self.torrenttype != "movie":
			assert 1 == 0, "Cannot set year for non-movie"
		self.seasonoryear = newvalue



# =========================================================================================
# Returns the category data in file writable format (pipe delimited string)
# =========================================================================================

	def getsavedata(self):

		outcome = self.torrenttype + "|" + self.movieorshowname + "|" + self.seasonoryear
		return outcome



# =========================================================================================
# Sets the category data read from a file (strings) - No validation of data
# =========================================================================================

	def setsavedata(self, typedata, namedata, otherdata):

		self.torrenttype = typedata
		self.movieorshowname = namedata
		self.seasonoryear = otherdata



# =========================================================================================
# Returns the root folder that any files are copied into, as an array of strings
# =========================================================================================

	def getdestinationfolder(self):

		folders = []
		if self.torrenttype == "movie":
			folders.append("Movies")
			folders.append(Functions.getinitial(self.movieorshowname))
		elif self.torrenttype == "tvshow":
			folders.append("TV Shows")
			folders.append(self.movieorshowname)
			if self.seasonoryear != "":
				folders.append(self.seasonoryear)

		return folders
