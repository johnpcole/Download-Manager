from .filedata_subcomponent import filedata_module as FileData
from ...functions_component import functions_module as Functions
from .category_subcomponent import category_module as Category
from .status_subcomponent import status_module as Status


# This class creates an object which is used to capture information about an individual torrent
# The object contains a mixture of remotely read Deluge Daemon data and local Download-Manager data


class DefineTorrentItem:

	def __init__(self, torrentid):

		# The raw name of the torrent (string)
		self.torrentname = ""

		# The GUID of the torrent, used to key the deluge daemon's list of torrents (string)
		self.torrentid = torrentid

		# The file path of the completed torrent, captured as a list, one item per folder in the hierarchical file
		# system (list/array of strings)
		self.location = "!UNKNOWN!"

		# Is a ????
		self.files = []

		# Determines if the file data of the torrent has changed since the torrent info was last read from Deluge
		# When a torrent is first added, there are zero files; Once the first peer has connected, file information
		# becomes available which needs to be read into Download-Manager
		self.filechangeflag = False

		self.torrentcategory = Category.createcategory()

		self.torrentstatus = Status.createstatus()

		self.dateadded = -99999


	# =========================================================================================

	def updateinfo(self, datalist):

		filecount = len(self.files)

		for dataitem in datalist:

			if dataitem == "name":
				self.torrentname = Functions.sanitisetext(datalist[dataitem])

			# -----------------------------------------------------------------------------------------------
			elif dataitem == "total_size":
				self.torrentstatus.setsize(datalist[dataitem])
			elif dataitem == "state":
				self.torrentstatus.setstatus(datalist[dataitem])
			elif dataitem == "progress":
				self.torrentstatus.setprogress(datalist[dataitem])
			elif dataitem == "is_finished":
				self.torrentstatus.setfinished(datalist[dataitem])
			elif dataitem == "eta":
				self.torrentstatus.seteta(datalist[dataitem])
			elif dataitem == "num_seeds":
				self.torrentstatus.setactiveseeders(datalist[dataitem])
			elif dataitem == "num_peers":
				self.torrentstatus.setactivepeers(datalist[dataitem])
			# -----------------------------------------------------------------------------------------------


			elif dataitem == "save_path":
				path = datalist[dataitem]
				self.location = path.split('/')


			elif dataitem == "files":
				self.updatefiledata(datalist[dataitem])

			#-----------------------------------------------------------------------------------------------
			elif dataitem == "torrenttype":
				self.torrentcategory.settype(datalist[dataitem])
			elif dataitem == "moviename":
				self.torrentcategory.setmoviename(datalist[dataitem])
			elif dataitem == "tvshowname":
				self.torrentcategory.setshowname(datalist[dataitem])
			elif dataitem == "year":
				self.torrentcategory.setyear(datalist[dataitem])
			elif dataitem == "season":
				self.torrentcategory.setseason(datalist[dataitem])
			#-----------------------------------------------------------------------------------------------

			elif dataitem == "time_added":
				self.dateadded = datalist[dataitem]

			else:
				outcome = "Unknown Data Label: " + dataitem
				assert 0 == 1, outcome

		if len(self.files) != filecount:
			self.filechangeflag = True

# =========================================================================================

	def getfileobject(self, fileid):

		outcome = None

		for existingfile in self.files:
			if existingfile.getid() == fileid:
				outcome = existingfile

		return outcome

# =========================================================================================

	def updatefiledata(self, filedata):

		for fileitem in filedata:
			existingfile = self.getfileobject(fileitem['index'])
			if existingfile is None:
				self.files.append(FileData.createitem(fileitem['index'], fileitem['path'], fileitem['size']))
		self.torrents = Functions.sortdictionary(self.files, 'filetype', True)

# =========================================================================================

	def updatefilepurpose(self, fileid, filepurpose):

		existingfile = self.getfileobject(int(fileid))
		if existingfile is not None:
			existingfile.updatefilepurpose(filepurpose)
		else:
			print("Cannot identify file")

# =========================================================================================

	def getid(self):

		return self.torrentid

# =========================================================================================

	def getfileobjects(self):

		return self.files

# =========================================================================================

	def gettorrenttitle(self):

		outcome = self.torrentcategory.getmovieortvshowname()
		if outcome == "":
			outcome = "New Unspecified Torrent"
		if self.torrentcategory.gettype() == "tvshow":
			episodeoutcome = ""
			for file in self.files:
				if file.getoutcome() == "copy":
					episodename = Functions.minifyepisode(file.getepisodepart(0))
					if episodename != "":
						if episodeoutcome == "":
							episodeoutcome = episodename
						else:
							if episodeoutcome != episodename:
								episodeoutcome = "(Multiple Episodes)"
			if (episodeoutcome != "") and (episodeoutcome != "(Multiple Episodes)"):
				suffix = Functions.minifyseason(self.torrentcategory.getseason(), episodeoutcome) + Functions.minifyepisode(episodeoutcome)
			else:
				suffix = self.torrentcategory.getseason()
		else:
			suffix = self.torrentcategory.getyear()
		if suffix != "":
			outcome = outcome + " - " + suffix

		return outcome

# =========================================================================================

	def getheadlinedata(self, datamode):

		if datamode == "initialise":
			outcome = { 'torrentid': self.torrentid,
						'torrenttitle': self.gettorrenttitle(),
						'torrentname': self.torrentname,
						'torrenttype': self.torrentcategory.gettype(),
						'status': self.torrentstatus.getfulltorrentstatus(),
						'progress': self.torrentstatus.progress}
		elif datamode == "refresh":
			outcome = { 'torrentid': self.torrentid,
						'status': self.torrentstatus.getfulltorrentstatus(),
						'progress': self.torrentstatus.progress}
		else:
			assert 1==0, datamode
		return outcome

# =========================================================================================

	def getextendeddata(self, datamode):

		if datamode == "initialise":
			outcome = { 'torrentid': self.torrentid,
						'torrenttitle': self.gettorrenttitle(),
						'torrentname': self.torrentname,
						'torrenttype': self.torrentcategory.gettype(),
						'status': self.torrentstatus.getfulltorrentstatus(),
						'progress': self.torrentstatus.getprogresssizeeta(),
						'files': self.getextendedfiledata(datamode)}
		elif datamode == "refresh":
			outcome = { 'status': self.torrentstatus.getfulltorrentstatus(),
						'progress': self.torrentstatus.getprogresssizeeta(),
						'filechangealert': self.filechangeflag}
			self.filechangeflag = False
		elif datamode == "reconfigure":
			outcome = { 'torrenttitle': self.gettorrenttitle(),
						'torrenttype': self.torrentcategory.gettype(),
						'files': self.getextendedfiledata(datamode)}
		elif datamode == "prepareedit":
			outcome = { 'moviename': self.torrentcategory.getmoviename(),
						'movieyear': self.torrentcategory.getyear(),
						'tvshowname': self.torrentcategory.getshowname(),
						'tvshowseason': self.torrentcategory.getseason(),
						'torrenttype': self.torrentcategory.gettype(),
						'files': self.getextendedfiledata(datamode)}
		else:
			assert 1 == 0, datamode
		return outcome


# =========================================================================================

	def getextendedfiledata(self, datamode):
		outcome = []
		for file in self.files:
			if (file.gettype() != "none") or (datamode != "prepareedit"):
				filedata = {}
				filedata["fileid"] = file.getid()
				if datamode == "initialise":
					filedata["filename"] = file.getsanitisedfilename()
					filedata["filetype"] = file.gettype()
					filedata["size"] = file.getsize()
					filedata["filetitle"] = self.getfiletitle(file)
					filedata["outcome"] = file.getoutcome()
				elif datamode == "reconfigure":
					filedata["filetitle"] = self.getfiletitle(file)
					filedata["outcome"] = file.getoutcome()
				elif datamode == "prepareedit":
					filedata["outcome"] = file.getoutcome()
					filedata["filetype"] = file.gettype()
					filedata["episodeselector"] = file.getepisodepart(0)
					filedata["subtitleselector"] = file.getepisodepart(1)
				else:
					assert 1 == 0, datamode
				outcome.append(filedata)
		return outcome

# =========================================================================================

	def getfiletitle(self, fileobject):

		outcome = fileobject.gettitle()
		if self.torrentcategory.gettype() == "tvshow":
			if outcome[:6] != "Ignore":
				outcome = Functions.minifyseason(self.torrentcategory.getseason(), fileobject.getepisodepart(0)) + outcome
		return outcome


# =========================================================================================

	def reconfiguretorrent(self, instructions):
		for indexkey in instructions:
			if indexkey == "files":
				files = instructions[indexkey]
				for fileindexkey in files:
					self.updatefilepurpose(fileindexkey, files[fileindexkey])
			else:
				self.updateinfo({indexkey: instructions[indexkey]})

# =========================================================================================

	def getsavedata(self):

		outcome = self.getid() + "|-|" + self.torrentcategory.getsavedata()
		outcomelist = []
		outcomelist.append(outcome)
		for fileitem in self.files:
			outcome = self.getid() + "|" + fileitem.getsavedata()
			outcomelist.append(outcome)
		return outcomelist

# =========================================================================================

	def setsavedata(self, dataarray):

		if dataarray[1] == "-":
			self.torrentcategory.setsavedata(dataarray[2], dataarray[3], dataarray[4])
		else:
			existingfile = self.getfileobject(int(dataarray[1]))
			if existingfile is not None:
				existingfile.updatefilepurpose(dataarray[2])
			else:
				print("Ignoring Saved File Config for torrent ", dataarray[0], ", file ",dataarray[1])

# =========================================================================================

	def getdestinationfilename(self, fileobject):

		rawfilename = self.getfiletitle(fileobject)
		filename = ""
		rawsplit = rawfilename.split(" ")
		if rawsplit[0] != "Ignored":
			if rawsplit[0] == "Film":
				filename = self.torrentcategory.getmoviename()
				if self.torrentcategory.getyear() != "":
					filename = filename + " (" + self.torrentcategory.getyear() + ")"
			else:
				filename = rawsplit[0]
			if rawsplit[len(rawsplit)-2] == "Subtitle":
				if rawsplit[len(rawsplit)-3] != "Standard":
					filename = filename + " - " + rawsplit[len(rawsplit)-3]
			filename = filename + "." + fileobject.getextension()

		return filename


# =========================================================================================

	def getdestination(self, fileobject):

		if (self.torrentcategory.gettype() != "none") and (fileobject.getoutcome() == "copy"):
			outcome = self.torrentcategory.getdestinationfolder()
			outcome.append(self.getdestinationfilename(fileobject))
		else:
			outcome = []
		return outcome

# =========================================================================================

	def getcopyactions(self):

		outcome = []
		for file in self.files:
			filedestination = self.getdestination(file)
			if filedestination != []:
				instruction = {'source': self.location + file.getpath(), 'target': filedestination,
																							'size': file.getrawsize()}
				outcome.append(instruction)
		return outcome



	def getconnectiondata(self):
		return self.torrentstatus.getconnectiondata()
