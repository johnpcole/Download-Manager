from ....common_components.dataconversion_framework import dataconversion_module as Functions
from .file_subcomponent import file_module as File


# This class creates an object which is used to capture information about an individual torrent's files
# The object contains a mixture of remotely read Deluge Daemon data and local Download-Manager data


class DefineFiles:

	def __init__(self):

		# The file path of the completed torrent, captured as a list, one item per folder in the hierarchical file
		# system (list/array of strings)
		self.location = "!UNKNOWN!"

		# Is a ????
		self.files = []

		# Determines if the file data of the torrent has changed since the torrent info was last read from Deluge
		# When a torrent is first added, there are zero files; Once the first peer has connected, file information
		# becomes available which needs to be read into Download-Manager
		self.filechangeflag = False



# =========================================================================================

	def settorrentfilespath(self, newvalue):

		self.location = newvalue.split('/')

# =========================================================================================

	def getfilechangealert(self):

		outcome = self.filechangeflag
		self.filechangeflag = False
		return outcome

# =========================================================================================

	def getfileobject(self, fileid):

		outcome = None

		for existingfile in self.files:
			if existingfile.getid() == fileid:
				outcome = existingfile

		return outcome

# =========================================================================================

	def updatefileslist(self, filedata):

		for fileitem in filedata:
			existingfile = self.getfileobject(fileitem['index'])
			if existingfile is None:
				self.files.append(File.createfile(fileitem['index'], fileitem['path'], fileitem['size']))
				self.filechangeflag = True
		if self.filechangeflag == True:
			self.files = Functions.sortdictionary(self.files, 'sanitisedfilename', False)
			outcome = {}
			for currentfiletype in ["video", "subtitle", "none"]:
				for existingfile in self.files:
					if existingfile.gettype() == currentfiletype:
						outcome.append(existingfile)
			self.files = outcome

# =========================================================================================

	def updatefilespurposes(self, filedata):

		for fileid in filedata:
			existingfile = self.getfileobject(int(fileid))
			if existingfile is not None:
				existingfile.updatefilepurpose(filedata[fileid])
			else:
				print("Cannot identify file" + fileid + " to update purpose")

# =========================================================================================

	def getfilesavedata(self):

		outcomelist = []
		for fileitem in self.files:
			outcomelist.append(fileitem.getsavedata())
		return outcomelist

# =========================================================================================

	def buildtorrenttitleepisodesuffix(self):

		episodeoutcome = ""
		for file in self.files:
			if file.getoutcome() == "copy":
				episodename = Functions.minifyepisode(file.getepisodepart())
				if episodename != "":
					if episodeoutcome == "":
						episodeoutcome = episodename
					else:
						if episodeoutcome != episodename:
							episodeoutcome = "(Multiple Episodes)"

		return episodeoutcome


# =========================================================================================

	def getextendedfiledata(self, datamode, tvshowseason):
		outcome = []
		for file in self.files:
			if (file.gettype() != "none") or (datamode != "prepareedit"):
				filedata = {}
				filedata["fileid"] = file.getid()
				if datamode == "initialise":
					filedata["filename"] = file.getsanitisedfilename()
					filedata["filetype"] = file.gettype()
					filedata["size"] = file.getsize()
					filedata["filetitle"] = file.getfiletitle(tvshowseason)
					filedata["outcome"] = file.getoutcome()
				elif datamode == "reconfigure":
					filedata["filetitle"] = file.getfiletitle(tvshowseason)
					filedata["outcome"] = file.getoutcome()
				elif datamode == "prepareedit":
					filedata["outcome"] = file.getoutcome()
					filedata["filetype"] = file.gettype()
					filedata["episodeselector"] = file.getepisodepart()
					filedata["subtitleselector"] = file.getsubtitlepart()
				else:
					assert 1 == 0, datamode
				outcome.append(filedata)
		return outcome


	# =========================================================================================

	def buildcopyactions(self, torrenttype, destinationfolder, moviename, movieyear, tvseason):

		outcome = []
		for file in self.files:
			filedestination = file.getcopydestination(torrenttype, destinationfolder, moviename, movieyear, tvseason)
			if filedestination != []:
				instruction = {'source': self.location + file.getpath(), 'target': filedestination,
																						'size': file.getrawsize()}
				outcome.append(instruction)
		return outcome
