from .torrenting_subcomponent import torrenting_module as TorrentManager
from .fileprocessing_subcomponent import fileprocessing_module as FileManager
from .monitoring_subcomponent import monitoring_module as MonitorManager
from .operatortracker_subcomponent import operatortracker_module as DelugeManager
from ..common_components.logging_framework import logging_module as Logging
from . import manager_privatefunctions as Waste


class DefineTorrentSet:

	def __init__(self, torrentsetname):

		Logging.printinvocation("Initialising Manager for " + torrentsetname, "")

		self.managername = torrentsetname
		self.librarymanager = FileManager.createfilemanager()
		self.torrentmanager = TorrentManager.createtorrentmanager()
		self.monitormanager = MonitorManager.createmonitor()
		self.monitormanager.restoresavedhistory(FileManager.getmonitor(MonitorManager.getloadlist()))
		self.delugemanager = DelugeManager.createtracker()
		self.areconfigsloaded = False

	#===============================================================================================
	# Load the Torrents List as new page
	#===============================================================================================

	def initialiselistpage(self):

		Logging.printinvocation("Loading All Torrents List Page", "")
		self.delugemanager.queuenewrefreshaction()
		if self.areconfigsloaded == False:
			return {'waitingforinitialisation': True}
		else:
			return {'torrentlist': self.torrentmanager.gettorrentlistdata("initialise"),
				'stats': self.monitormanager.getsessionmeters(),
				'copyqueuestate': self.librarymanager.getoverallcopierstate()}



	#===============================================================================================
	# Refresh Torrents List on existing page, after performing a bulk action if required
	#===============================================================================================

	def updatelistpage(self, bulkaction):

		if bulkaction == "Start":
			Logging.printinvocation("Starting all Torrents", "")
			self.delugemanager.queuenewresumeallaction()
		elif bulkaction == "Stop":
			Logging.printinvocation("Stopping all Torrents", "")
			self.delugemanager.queuenewpauseallaction()
		elif bulkaction == "RescanFileServer":
			Logging.printinvocation("Rescanning File-Server for TV Shows & Seasons", "")
			self.librarymanager.discovertvshows()
		elif bulkaction == "Refresh":
			Logging.printinvocation("Refreshing All Torrents List Page", "")
		else:
			Logging.printinvocation("Unknown Torrents List Update Action: " + bulkaction, "")
		self.delugemanager.queuenewrefreshaction()
		return {'torrents': self.torrentmanager.gettorrentlistdata("refresh"),
				'stats': self.monitormanager.getsessionmeters(),
				'copyqueuestate': self.librarymanager.getoverallcopierstate()}



	#===============================================================================================
	# Load a Torrent with Network & Configuration Data as new page
	#===============================================================================================

	def initialisetorrentpage(self, torrentid):

		if self.areconfigsloaded == False:
			return {'waitingforinitialisation': True}
		else:
			if self.torrentmanager.validatetorrentid(torrentid) == True:
				Logging.printinvocation("Loading Specific Torrent Page", torrentid)
				self.delugemanager.queuenewrefreshaction()
				return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "initialise"),
						'copyqueuestate': self.librarymanager.gettorrentcopystate(torrentid)}
			else:
				Logging.printinvocation("Requested view of Unknown Torrent", torrentid)
				return {'waitingforinitialisation': True}


	#===============================================================================================
	# Refresh an existing Torrent page with Network Data, after performing an action if required
	#===============================================================================================

	def updatetorrentpage(self, torrentid, torrentaction):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			if torrentaction == "Start":
				Logging.printinvocation("Starting Torrent", torrentid)
				self.delugemanager.queuenewresumetorrentaction(torrentid)
			elif torrentaction == "Stop":
				Logging.printinvocation("Stopping Torrent", torrentid)
				self.delugemanager.queuenewpausetorrentaction(torrentid)
			elif torrentaction == "Refresh":
				Logging.printinvocation("Refreshing Specific Torrent Page", torrentid)
			else:
				Logging.printinvocation("Unknown Torrent Update Action: " + torrentaction, torrentid)
			self.delugemanager.queuenewrefreshaction()
			return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "refresh"),
					'copyqueuestate': self.librarymanager.gettorrentcopystate(torrentid)}
		else:
			Logging.printinvocation("Requested Update to Unknown Torrent", torrentid)



	#===============================================================================================
	# Copies Files
	#===============================================================================================

	def copytorrent(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Initiating Torrent Copy", torrentid)
			self.librarymanager.queuefilecopy(self.torrentmanager.getcopyactions(torrentid))
			return {'copydata': "Queued"}
		else:
			Logging.printinvocation("Requested Initiate Torrent Copy of Unknown Torrent", torrentid)



	#===============================================================================================
	# Delete Torrent
	#===============================================================================================

	def deletetorrent(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Deleting Torrent", torrentid)
			self.delugemanager.queuenewdeletetorrentaction(torrentid)
			return {'deletedata': "Done"}
		else:
			Logging.printinvocation("Requested Deletion of Unknown Torrent", torrentid)



	# ===============================================================================================
	# Refresh an existing Torrent page with Configuration Data, after saving new instructions
	# ===============================================================================================

	def reconfiguretorrentconfiguration(self, torrentid, newconfiguration):

		Waste.time()
		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Saving Reconfigured Torrent", torrentid)
			self.torrentmanager.reconfiguretorrent(torrentid, newconfiguration)
			FileManager.saveconfigs(self.torrentmanager.getconfigs())
			return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "reconfigure")}
		else:
			Logging.printinvocation("Requested Save Reconfiguration of Unknown Torrent", torrentid)



	# ===============================================================================================
	# Refresh an existing Torrent page with Configuration Data used to populate edit fields
	# ===============================================================================================

	def edittorrentconfiguration(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Starting Torrent Reconfiguration", torrentid)
			Waste.time()
			torrentdata = self.torrentmanager.gettorrentdata(torrentid, "prepareedit")
			return {'selectedtorrent': torrentdata,
					'listitems': self.librarymanager.getdropdownlists(torrentdata['tvshowname'])}
		else:
			Logging.printinvocation("Requested Unknown Torrent Reconfiguration", torrentid)



	# ===============================================================================================
	# Refresh an existing Torrent page with Configuration Data used to populate the Season edit field
	# ===============================================================================================

	def updatetvshowseasonslist(self, tvshow):

		Logging.printinvocation("Getting TV Show Data", "")
		Waste.time()
		return {'seasons': self.librarymanager.gettvshowseasons(tvshow)}



	# ===============================================================================================
	# Performs a Torrent Addition, and returns the new Torrent Data (to be displayed on a new Page)
	# ===============================================================================================

	def addnewtorrent(self, newurl):

		Logging.printinvocation("Adding New Torrent", "")
		self.delugemanager.queuenewaddtorrentaction(newurl)
		return {'addtorrent': 'done'}



	#===============================================================================================
	# Display the logging file contents
	#===============================================================================================

	def displaylogs(self, verboseloggingmode):

		if verboseloggingmode == True:
			logkind = "Verbose Log"
		else:
			logkind = "Log"
		Logging.printinvocation("Loading Application " + logkind + " Page", "")
		return {'loggingoutput': FileManager.getloggingdata(verboseloggingmode)}



	#===============================================================================================
	# Display the copier
	#===============================================================================================

	def displaycopier(self):

		Logging.printinvocation("Loading Copier Page", "")
		return {'copyactions': self.librarymanager.getcopierpageload(self.torrentmanager.gettorrentidlist())}



	#===============================================================================================
	# Refresh Copier List page
	#===============================================================================================

	def updatecopierpage(self):

		Logging.printinvocation("Refreshing Copier Page", "")
		return {'copyactions': self.librarymanager.getcopierpageupdate()}



	#===============================================================================================
	# Display the monitor
	#===============================================================================================

	def displaymonitor(self):

		Logging.printinvocation("Loading Monitor History Page", "")
		return {'monitoroutput': self.monitormanager.gethistorygraphics()}



	#===============================================================================================
	# Process Copy Queue
	#===============================================================================================

	def triggercopier(self, latestcopyid, copyoutcome, notes):

		Logging.printinvocation("Triggering Copier", "")
		self.librarymanager.importcopieroutcome(latestcopyid, copyoutcome, notes)
		return self.librarymanager.processnextcopyaction()



	#===============================================================================================
	# Process Operator Queue
	#===============================================================================================

	def triggeroperator(self, torrentdata, sessiondata, monitorhistory):

		Logging.printinvocation("Triggering Operator", "")

		if torrentdata is not None:
			self.torrentmanager.refreshtorrentlist(torrentdata)
			if self.areconfigsloaded == False:
				self.torrentmanager.setconfigs(FileManager.loadconfigs())
				self.areconfigsloaded = True
			if sessiondata is not None:
				self.monitormanager.refreshsessiondata(sessiondata, self.torrentmanager.getaggregates())

		if monitorhistory is True:
			outcome = self.monitormanager.addtohistory()
			FileManager.savemonitor(outcome)

		return self.delugemanager.getnextoperatoraction()




	def determinewebmode(self):

		return True # FileManager.getwebhostconfig()
