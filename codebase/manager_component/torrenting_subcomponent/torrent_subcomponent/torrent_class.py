from .files_subcomponent import files_module as Files
from ....common_components.dataconversion_framework import dataconversion_module as Functions
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

		self.dateadded = -99999

		self.torrentcategory = Category.createcategory()

		self.torrentstatus = Status.createstatus()

		self.torrentfiles = Files.createfilesdata()

		self.istorrentvisible = True


# =========================================================================================

	def updateinfo(self, datalist):

		# Some values are only valid for certain torrent types; so to ensure there isn't
		# an error (because we cannot guarantee the order data is passed through), the
		# torrenttype is updated before the rest of the data dictionary is processed
		if "torrenttype" in datalist:
			self.torrentcategory.settype(datalist["torrenttype"])


		for dataitem in datalist:

			if dataitem == "name":
				self.torrentname = Functions.sanitisetext(datalist[dataitem])
			elif dataitem == "time_added":
				self.dateadded = datalist[dataitem]
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
			elif dataitem == "tracker_status":
				self.torrentstatus.settrackerstatus(datalist[dataitem])
			# -----------------------------------------------------------------------------------------------
			elif dataitem == "save_path":
				self.torrentfiles.settorrentfilespath(datalist[dataitem])
			elif dataitem == "files":
				self.torrentfiles.updatefileslist(datalist[dataitem])
			elif dataitem == "fileinstructions":
				self.torrentfiles.updatefilespurposes(datalist[dataitem])
			# -----------------------------------------------------------------------------------------------
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
			# -----------------------------------------------------------------------------------------------
			else:
				outcome = "Unknown Data Label: " + dataitem
				assert 0 == 1, outcome

# =========================================================================================

	def getid(self):

		return self.torrentid

# =========================================================================================

	def gettorrenttitle(self):

		episodesuffix = ""

		if self.torrentcategory.gettype() == "tvshow":
			episodeoutcome = self.torrentfiles.buildtorrenttitleepisodesuffix()
			if (episodeoutcome != "") and (episodeoutcome != "(Multiple Episodes)"):
				episodesuffix = Functions.minifyseason(self.torrentcategory.getseason(), episodeoutcome) + Functions.minifyepisode(episodeoutcome)

		return self.torrentcategory.buildtorrenttitle(episodesuffix)

# =========================================================================================

	def getheadlinedata(self, datamode):

		if datamode == "initialise":
			outcome = { 'torrentid': self.torrentid,
						'torrenttitle': self.gettorrenttitle(),
						'torrentname': self.torrentname,
						'torrenttype': self.torrentcategory.gettype(),
						'status': self.torrentstatus.getfulltorrentstatus(),
						'progress': self.torrentstatus.getprogress()}
		elif datamode == "refresh":
			outcome = { 'torrentid': self.torrentid,
						'status': self.torrentstatus.getfulltorrentstatus(),
						'progress': self.torrentstatus.getprogress()}
		else:
			assert 1 == 0, datamode
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
						'copyinfo': self.getcopydestinationlist(),
						'files': self.torrentfiles.getextendedfiledata(datamode, self.torrentcategory.getseason())}
		elif datamode == "refresh":
			outcome = { 'status': self.torrentstatus.getfulltorrentstatus(),
						'progress': self.torrentstatus.getprogresssizeeta(),
						'filechangealert': self.torrentfiles.getfilechangealert()}
		elif datamode == "reconfigure":
			outcome = { 'torrenttitle': self.gettorrenttitle(),
						'torrenttype': self.torrentcategory.gettype(),
						'copyinfo': self.getcopydestinationlist(),
						'files': self.torrentfiles.getextendedfiledata(datamode, self.torrentcategory.getseason())}
		elif datamode == "prepareedit":
			outcome = { 'moviename': self.torrentcategory.getmoviename(),
						'movieyear': self.torrentcategory.getyear(),
						'tvshowname': self.torrentcategory.getshowname(),
						'tvshowseason': self.torrentcategory.getseason(),
						'torrenttype': self.torrentcategory.gettype(),
						'files': self.torrentfiles.getextendedfiledata(datamode, self.torrentcategory.getseason())}
		else:
			assert 1 == 0, datamode
		return outcome

# =========================================================================================

	def getsavedata(self):

		outcomelist = []
		outcomelist.append(self.getid() + "|-|" + self.torrentcategory.getcategorysavedata())
		filesavedata = self.torrentfiles.getfilesavedata()
		for fileitem in filesavedata:
			outcomelist.append(self.getid() + "|" + fileitem)
		return outcomelist

# =========================================================================================

	def setsavedata(self, dataarray):

		if dataarray[1] == "-":
			self.torrentcategory.setcategorysavedata(dataarray[2], dataarray[3], dataarray[4])
		else:
			self.torrentfiles.updatefilespurposes({dataarray[1]: dataarray[2]})



# =========================================================================================

	def getconnectiondata(self):
		return self.torrentstatus.getconnectionstatusdata()

# =========================================================================================

	def gettorrentcopyactions(self):
		if self.torrentstatus.getfinished() == 'Completed':
			outcome = self.torrentfiles.buildcopyactions(self.torrentname,
														self.torrentid,
														self.torrentcategory.gettype(),
														self.torrentcategory.getdestinationfolder(),
														self.torrentcategory.getmoviename(),
														self.torrentcategory.getyear(),
														self.torrentcategory.getseason())
		else:
			outcome = []

		return outcome



	def getcopydestinationlist(self):
		outcome = []
		copylist = self.gettorrentcopyactions()
		for action in copylist:
			newdestination = ""
			for pathnode in action['target']:
				newdestination = newdestination + " / " + pathnode
			outcome.append(newdestination)
		return outcome


	def markasdeleted(self):

		self.istorrentvisible = False


	def isvisible(self):

		return self.istorrentvisible



