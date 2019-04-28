from ....functions_component import functions_module as Functions

class DefineFileItem:

	def __init__(self, fileid, path, size):

		self.fileid = fileid

		self.path = path.split('/')

		self.rawsize = size

		self.filetype = "NOT PROCESSED"
		self.updatefiletype()

		self.episode = "ignore"

		self.sanitisedfilename = Functions.sanitisetext(self.getshortpath())


# =========================================================================================

	def updatefilepurpose(self, episode):

		self.episode = episode

# =========================================================================================

	def getpurpose(self):

		return self.episode

# =========================================================================================

	def gettype(self):

		return self.filetype

# =========================================================================================

	def getid(self):

		return self.fileid

# =========================================================================================

	def getpath(self):

		return self.path

# =========================================================================================

	def getshortpath(self):

		pathsplit = self.path
		return pathsplit[len(pathsplit)-1]

# =========================================================================================

	def getsanitisedfilename(self):

		return self.sanitisedfilename

# =========================================================================================

	def getrawsize(self):

		return self.rawsize

# =========================================================================================

	def getsize(self):

		return Functions.sanitisesize(self.rawsize)

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

		outcome = str(self.getid()) + "|" + self.getpurpose()
		return outcome

# =========================================================================================

	def gettitle(self):

		outcome = ""
		if self.gettype() != "none":
			if self.getpurpose() == "ignore":
				outcome = "Ignored"
			else:
				outcome = Functions.minifyepisode(self.getepisodepart(0))
				subtitle = self.getepisodepart(1)
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

	def getoutcome(self):

		outcome = ""
		if self.getpurpose() == "ignore":
			outcome = "ignore"
		else:
			outcome = "copy"
		return outcome

# =========================================================================================

	def getepisodepart(self, part):

		outcome = ""
		rawstring = self.getpurpose()
		rawsplit = rawstring.split("_")
		if part == 0:
			outcome = rawsplit[0]
		elif (part == 1) and (self.gettype() == "subtitle"):
			outcome = "Unknown"
			if len(rawsplit) > 1:
				if rawsplit[1] != "":
					outcome = rawsplit[1]
		return outcome


