from .....functions_component import functions_module as Functions

class DefineFile:

	def __init__(self, fileid, path, size):

		# The deluge ID of the file
		self.fileid = fileid

		# The reported source path of the file, once the torrent has completed downloading
		# This is stored as an array, with each level of folder/file captured as a string element
		self.path = path.split('/')

		# The reported size of the file
		self.rawsize = size

		# The type of file - NONE, SUBTITLE, VIDEO; Derived from the reported filename extension
		self.filetype = "NOT PROCESSED"
		self.updatefiletype()

		# The purpose of the file - ignore, ???????? etc
		self.filepurpose = "ignore"

		# ????????????????
		self.sanitisedfilename = Functions.sanitisetext(self.getshortpath())


# =========================================================================================
# Changes the purpose of the file
# =========================================================================================

	def updatefilepurpose(self, newpurpose):

		self.filepurpose = newpurpose

# =========================================================================================
# Returns the purpose of the file
# =========================================================================================

	def getpurpose(self):

		return self.filepurpose

# =========================================================================================
# Returns the filetype - NONE, SUBTITLE, VIDEO
# =========================================================================================

	def gettype(self):

		return self.filetype

# =========================================================================================
# Returns the ID of the file
# =========================================================================================

	def getid(self):

		return self.fileid

# =========================================================================================
# Returns the source path of the saved file, once the torrent has completed downloading
# This is a string array, with each level of folder/file captured as a string element
# =========================================================================================

	def getpath(self):

		return self.path

# =========================================================================================
# Returns the source path of the saved file's parent folder, once the torrent has completed downloading
# This is a string array, with each level of folder captured as a string element
# =========================================================================================

	def getshortpath(self):

		pathsplit = self.path
		return pathsplit[len(pathsplit)-1]

# =========================================================================================
# Returns the sanitised filename???????????????
# =========================================================================================

	def getsanitisedfilename(self):

		return self.sanitisedfilename

# =========================================================================================
# Returns the reported filesize
# =========================================================================================

	def getrawsize(self):

		return self.rawsize

# =========================================================================================
# Returns the sanitised filesize
# =========================================================================================

	def getsize(self):

		return Functions.sanitisesize(self.rawsize)

# =========================================================================================
# Returns the filename extension
# =========================================================================================

	def getextension(self):

		shortpath = self.getshortpath()
		filenamesplit = shortpath.split('.')
		if len(filenamesplit) > 1:
			extension = filenamesplit[len(filenamesplit)-1]
		else:
			extension = ""

		return extension

# =========================================================================================
# Sets the filetype, based on the filename extension
# =========================================================================================

	def updatefiletype(self):

		extension = self.getextension()
		outcome = "NONE"

		if extension == "srt":
			outcome = "SUBTITLE"
		elif extension == "sub":
			outcome = "SUBTITLE"

		elif extension == "avi":
			outcome = "VIDEO"
		elif extension == "divx":
			outcome = "VIDEO"
		elif extension == "m4v":
			outcome = "VIDEO"
		elif extension == "mkv":
			outcome = "VIDEO"
		elif extension == "mov":
			outcome = "VIDEO"
		elif extension == "mp4":
			outcome = "VIDEO"

		self.filetype = outcome.lower()

# =========================================================================================

	def getsavedata(self):

		outcome = str(self.fileid) + "|" + self.filepurpose
		return outcome

# =========================================================================================
# Returns the computed title of the file: Ignored File, Ignored Video File, Ignored Subtitle File
# WHAT ABOUT FILMS??????????????????????????????????????????
# This is the "Title" that is displayed on the torrent webpage?????
# =========================================================================================

	def gettitlebase(self):

		outcome = ""
		if self.gettype() != "none":
			if self.filepurpose == "ignore":
				outcome = "Ignored"
			else:
				outcome = Functions.minifyepisode(self.getepisodepart())
				subtitle = self.getsubtitlepart()
				if subtitle != "":
					outcome = outcome + " " + subtitle
			if self.gettype() == "video":
				outcome = outcome + " Video File"
			elif self.gettype() == "subtitle":
				outcome = outcome + " Subtitle File"
		else:
			outcome = "Ignored File"
		return outcome

# =========================================================================================
# Returns the outcome of the file, either "ignore" or "copy", based on the file purpose
# =========================================================================================

	def getoutcome(self):

		outcome = ""
		if self.filepurpose == "ignore":
			outcome = "ignore"
		else:
			outcome = "copy"
		return outcome

# =========================================================================================
# Returns a sub-string of the processed file purpose equating to the EPISODE
# =========================================================================================

	def getepisodepart(self):

		outcome = ""
		rawsplit = self.filepurpose.split("_")
		return rawsplit[0]

# =========================================================================================
# Returns a sub-string of the processed file purpose equating to the SUBTITLE DESIGNATION
# =========================================================================================

	def getsubtitlepart(self):

		outcome = ""
		if self.filetype == "subtitle":
			outcome = "Unknown"
			rawsplit = self.filepurpose.split("_")
			if len(rawsplit) > 1:
				if rawsplit[1] != "":
					outcome = rawsplit[1]
		return outcome

# =========================================================================================
# Returns the full computed title of the file: Ignored File, Ignored Video File, Ignored Subtitle File
# WHAT ABOUT FILMS??????????????????????????????????????????
# This is the filename that the file is copied to?????
# =========================================================================================

	def getfiletitle(self, tvshowseason):

		outcome = self.gettitlebase()
		if tvshowseason != "":
			if outcome[:6] != "Ignore":
				outcome = Functions.minifyseason(tvshowseason, self.getepisodepart()) + outcome
		return outcome

# =========================================================================================

	def getdestinationfilename(self, moviename, movieyear, tvshowseason):

		rawfilename = self.getfiletitle(tvshowseason)
		filename = ""
		rawsplit = rawfilename.split(" ")
		if rawsplit[0] != "Ignored":
			if rawsplit[0] == "Film":
				filename = moviename
				if movieyear != "":
					filename = filename + " (" + movieyear + ")"
			else:
				filename = rawsplit[0]
			if rawsplit[len(rawsplit)-2] == "Subtitle":
				if rawsplit[len(rawsplit)-3] != "Standard":
					filename = filename + " - " + rawsplit[len(rawsplit)-3]
			filename = filename + "." + self.getextension()

		return filename

# =========================================================================================

	def getcopydestination(self, torrenttype, destinationfolder, moviename, movieyear, tvseason):

		if (torrenttype != "none") and (self.getoutcome() == "copy"):
			outcome = destinationfolder.copy()
			outcome.append(self.getdestinationfilename(moviename, movieyear, tvseason))
		else:
			outcome = []
		return outcome
