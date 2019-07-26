from .torrenting_subcomponent import torrenting_module as TorrentManager
from .fileprocessing_subcomponent import fileprocessing_module as FileManager
from .monitoring_subcomponent import monitoring_module as MonitorManager
from ..common_components.logging_framework import logging_module as Logging
from . import manager_privatefunctions as Waste


class DefineTorrentSet:

	def __init__(self, torrentsetname):

		Logging.printinvocation("Initialising Manager for " + torrentsetname, "")

		self.managername = torrentsetname
		self.librarymanager = FileManager.createmanager()
		self.torrentmanager = TorrentManager.createmanager(FileManager.gettorrentconnectionconfig())
		self.torrentmanager.setconfigs(FileManager.loadconfigs())
		self.monitormanager = MonitorManager.createmonitor()
		self.monitormanager.restoresavedhistory(FileManager.getmonitor(MonitorManager.getloadlist()))


	#===============================================================================================
	# Load the Torrents List as new page
	#===============================================================================================

	def initialiselistpage(self):

		Logging.printinvocation("Loading All Torrents List Page", "")
		self.torrentmanager.refreshtorrentlist("Manager")
		self.monitormanager.refreshsessionmeters(self.torrentmanager.getsessiondata())
		return {'torrentlist': self.torrentmanager.gettorrentlistdata("initialise"),
				'stats': self.monitormanager.getsessionmeters()}



	#===============================================================================================
	# Refresh Torrents List on existing page, after performing a bulk action if required
	#===============================================================================================

	def updatelistpage(self, bulkaction):

		if (bulkaction == "Start") or (bulkaction == "Stop"):
			Logging.printinvocation(bulkaction + "ing all Torrents", "")
			self.torrentmanager.bulkprocessalltorrents(bulkaction)
		elif bulkaction == "RescanFileServer":
			Logging.printinvocation("Rescanning File-Server for TV Shows & Seasons", "")
			self.librarymanager.discovertvshows()
		elif bulkaction == "Refresh":
			Logging.printinvocation("Refreshing All Torrents List Page", "")
		else:
			Logging.printinvocation("Unknown Torrents List Update Action: " + bulkaction, "")
		self.torrentmanager.refreshtorrentlist("Manager")
		self.monitormanager.refreshsessionmeters(self.torrentmanager.getsessiondata())
		return {'torrents': self.torrentmanager.gettorrentlistdata("refresh"),
				'stats': self.monitormanager.getsessionmeters()}



	#===============================================================================================
	# Load a Torrent with Network & Configuration Data as new page
	#===============================================================================================

	def initialisetorrentpage(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Loading Specific Torrent Page", torrentid)
			self.torrentmanager.refreshtorrentdata(torrentid)
			return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "initialise"),
					'copystate': self.librarymanager.gettorrentcopystate(torrentid)}
		else:
			Logging.printinvocation("Requested view of Unknown Torrent", torrentid)


	#===============================================================================================
	# Refresh an existing Torrent page with Network Data, after performing an action if required
	#===============================================================================================

	def updatetorrentpage(self, torrentid, torrentaction):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			if (torrentaction == "Start") or (torrentaction == "Stop"):
				Logging.printinvocation(torrentaction + "ing Torrent", torrentid )
				self.torrentmanager.processonetorrent(torrentid, torrentaction)
			elif torrentaction == "Refresh":
				Logging.printinvocation("Refreshing Specific Torrent Page", torrentid)
			else:
				Logging.printinvocation("Unknown Torrent Update Action: " + torrentaction, torrentid)
			self.torrentmanager.refreshtorrentdata(torrentid)
			return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "refresh"),
					'copystate': self.librarymanager.gettorrentcopystate(torrentid)}
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
			self.torrentmanager.processonetorrent(torrentid, "Delete")
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
		newid = self.torrentmanager.addnewtorrenttoclient(newurl)
		Waste.time()
		#torrentmanager.refreshtorrentlist()
		return {'newtorrentid': newid}



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
		return {'copyactions': self.librarymanager.getcopierpagedata(self.torrentmanager.gettorrentidlist())}



	#===============================================================================================
	# Refresh Copier List page
	#===============================================================================================

	def updatecopierpage(self):

		Logging.printinvocation("Refreshing Copier Page", "")
		return {'copyactions': self.librarymanager.getcopierpageupdatedata()}



	#===============================================================================================
	# Display the monitor
	#===============================================================================================

	def displaymonitor(self):

		Logging.printinvocation("Loading Monitor History Page", "")
		return {'monitoroutput': self.monitormanager.gethistorygraphics()}



	#===============================================================================================
	# Generate a Monitor History Item
	#===============================================================================================

	def triggermonitor(self):

		Logging.printinvocation("Triggering Monitor", "")
		self.torrentmanager.refreshtorrentlist("Monitor")
		outcome = self.monitormanager.addtohistory(self.torrentmanager.getsessiondata())
		FileManager.savemonitor(outcome)
		return {'monitordata': outcome}



	#===============================================================================================
	# Process Copy Queue
	#===============================================================================================

	def triggercopier(self, latestcopyid, copyoutcome, notes):

		Logging.printinvocation("Triggering Copier", "")
		self.librarymanager.importcopieroutcome(latestcopyid, copyoutcome, notes)
		return self.librarymanager.processnextcopyaction()










	def determinewebmode(self):

		return True # FileManager.getwebhostconfig()
