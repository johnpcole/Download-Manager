from .torrenting_subcomponent import torrenting_module as TorrentManager
from .monitoring_subcomponent import monitoring_module as MonitorManager
from .copiertracker_subcomponent import copiertracker_module as CopierManager
from .operatortracker_subcomponent import operatortracker_module as DelugeManager
from ..common_components.logging_framework import logging_module as Logging
from .datastore_subcomponent import datastore_module as ConfigFile
from .fileoptions_subcomponent import fileoptions_module as FileOptions


class DefineTorrentSet:

	def __init__(self, torrentsetname):

		Logging.printinvocation("Initialising Manager for " + torrentsetname, "")

		self.fileoptions = FileOptions.createfileoptions()
		self.managername = torrentsetname
		self.copiermanager = CopierManager.createtracker()
		self.torrentmanager = TorrentManager.createtorrentmanager()
		self.monitormanager = MonitorManager.createmonitor()
		self.monitormanager.restoresavedhistory(ConfigFile.getmonitor(MonitorManager.getloadlist()))
		self.delugemanager = DelugeManager.createtracker()

		#self.delugemanager.queuenewrefreshaction()

	#===============================================================================================
	# Load the Torrents List as new page
	#===============================================================================================

	def initialiselistpage(self):

		Logging.printinvocation("Loading All Torrents List Page", "")
		self.torrentmanager.refreshtorrentlist()
		self.monitormanager.refreshsessiondata(self.torrentmanager.getaggregates())
		return {'torrentlist': self.torrentmanager.gettorrentlistdata("initialise"),
				'stats': self.monitormanager.getdashboardmeters(True),  #self.delugemanager.hasrecentlybeenseen()),
				'copyqueuestate': self.copiermanager.getcopysetstate("ALL"),
				'refreshfolderstate': self.copiermanager.getcopysetstate("FOLDER REFRESH")}



	#===============================================================================================
	# Refresh Torrents List on existing page
	#===============================================================================================

	def updatelistpage(self):

		Logging.printinvocation("Refreshing All Torrents List Page", "")
		self.torrentmanager.refreshtorrentlist()
		self.monitormanager.refreshsessiondata(self.torrentmanager.getaggregates())
		return {'torrents': self.torrentmanager.gettorrentlistdata("refresh"),
				'stats': self.monitormanager.getdashboardmeters(True),  #self.delugemanager.hasrecentlybeenseen()),
				'copyqueuestate': self.copiermanager.getcopysetstate("ALL"),
				'refreshfolderstate': self.copiermanager.getcopysetstate("FOLDER REFRESH")}



	#===============================================================================================
	# Performing a bulk action if required
	#===============================================================================================

	def performbulkaction(self, bulkaction):

		if bulkaction == "Start":
			Logging.printinvocation("Starting all Torrents", "")
			self.delugemanager.queuenewresumeallaction()
		elif bulkaction == "Stop":
			Logging.printinvocation("Stopping all Torrents", "")
			self.delugemanager.queuenewpauseallaction()
		else:
			Logging.printinvocation("Unknown Torrents List Update Action: " + bulkaction, "")
		self.torrentmanager.refreshtorrentlist()
		self.monitormanager.refreshsessiondata(self.torrentmanager.getaggregates())
		return {'bulktorrentaction': 'done'}



	#===============================================================================================
	# Performing a bulk action if required
	#===============================================================================================

	def rescantvshows(self):

		Logging.printinvocation("Rescanning File-Server for TV Shows & Seasons", "")
		self.copiermanager.queuefolderrefresh()
		self.torrentmanager.refreshtorrentlist()
		return {'copyqueuestate': self.copiermanager.getcopysetstate("ALL"),
				'refreshfolderstate': self.copiermanager.getcopysetstate("FOLDER REFRESH")}





	#===============================================================================================
	# Load a Torrent with Network & Configuration Data as new page
	#===============================================================================================

	def initialisetorrentpage(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Loading Specific Torrent Page", torrentid)
			self.torrentmanager.refreshtorrentlist()
			return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "initialise"),
					'copyqueuestate': self.copiermanager.getcopysetstate(torrentid)}
		else:
			Logging.printinvocation("Requested view of Unknown Torrent", torrentid)
			return {'waitingforinitialisation': True}


	#===============================================================================================
	# Refresh an existing Torrent page with Network Data
	#===============================================================================================

	def updatetorrentpage(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Refreshing Specific Torrent Page", torrentid)
			self.torrentmanager.refreshtorrentlist()
			return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "refresh"),
					'copyqueuestate': self.copiermanager.getcopysetstate(torrentid)}
		else:
			Logging.printinvocation("Requested Refresh to Unknown Torrent", torrentid)


	#===============================================================================================
	# Refresh an existing Torrent page with Network Data, after performing an action if required
	#===============================================================================================

	def performtorrentaction(self, torrentid, torrentaction):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			if torrentaction == "Start":
				Logging.printinvocation("Starting Torrent", torrentid)
				self.delugemanager.queuenewresumetorrentaction(torrentid)
			elif torrentaction == "Stop":
				Logging.printinvocation("Stopping Torrent", torrentid)
				self.delugemanager.queuenewpausetorrentaction(torrentid)
			else:
				Logging.printinvocation("Unknown Torrent Update Action: " + torrentaction, torrentid)
			self.torrentmanager.refreshtorrentlist()
			return {'torrentaction': 'done'}
		else:
			Logging.printinvocation("Requested Update to Unknown Torrent", torrentid)




	#===============================================================================================
	# Copies Files
	#===============================================================================================

	def copytorrent(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Initiating Torrent Copy", torrentid)
			self.copiermanager.queuenewfilecopyactions(self.torrentmanager.getcopyactions(torrentid))
			return {'copydata': "Queued"}
		else:
			Logging.printinvocation("Requested Initiate Torrent Copy of Unknown Torrent", torrentid)



	#===============================================================================================
	# Delete Torrent
	#===============================================================================================

	def deletetorrent(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Deleting Torrent", torrentid)
			self.torrentmanager.markasdeteled(torrentid)
			self.delugemanager.queuenewdeletetorrentaction(torrentid)
			return {'deletedata': "Done"}
		else:
			Logging.printinvocation("Requested Deletion of Unknown Torrent", torrentid)



	# ===============================================================================================
	# Refresh an existing Torrent page with Configuration Data, after saving new instructions
	# ===============================================================================================

	def reconfiguretorrentconfiguration(self, torrentid, newconfiguration):

		#Waste.time()
		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Saving Reconfigured Torrent", torrentid)
			self.torrentmanager.reconfiguretorrent(torrentid, newconfiguration)
			return {'selectedtorrent': self.torrentmanager.gettorrentdata(torrentid, "reconfigure")}
		else:
			Logging.printinvocation("Requested Save Reconfiguration of Unknown Torrent", torrentid)



	# ===============================================================================================
	# Refresh an existing Torrent page with Configuration Data used to populate edit fields
	# ===============================================================================================

	def edittorrentconfiguration(self, torrentid):

		if self.torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Starting Torrent Reconfiguration", torrentid)
			#Waste.time()
			torrentdata = self.torrentmanager.gettorrentdata(torrentid, "prepareedit")
			return {'selectedtorrent': torrentdata,
					'listitems': self.fileoptions.getdropdownlists(torrentdata['tvshowname'])}
		else:
			Logging.printinvocation("Requested Unknown Torrent Reconfiguration", torrentid)



	# ===============================================================================================
	# Refresh an existing Torrent page with Configuration Data used to populate the Season edit field
	# ===============================================================================================

	def updatetvshowseasonslist(self, tvshow):

		Logging.printinvocation("Getting TV Show Data", "")
		#Waste.time()
		return {'seasons': self.fileoptions.gettvshowseasons(tvshow)}



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
		return {'loggingoutput': ConfigFile.getloggingdata(verboseloggingmode)}



	#===============================================================================================
	# Display the copier
	#===============================================================================================

	def displaycopier(self):

		Logging.printinvocation("Loading Copier Page", "")
		#self.delugemanager.queuenewrefreshaction()
		return {'copyactions': self.copiermanager.getcopierpageinitialdata(
																		self.torrentmanager.getvisibletorrentidlist())}



	#===============================================================================================
	# Refresh Copier List page
	#===============================================================================================

	def updatecopierpage(self):

		Logging.printinvocation("Refreshing Copier Page", "")
		#self.delugemanager.queuenewrefreshaction()
		return {'copyactions': self.copiermanager.getcopierpagerefreshdata()}



	#===============================================================================================
	# Get copy action detail
	#===============================================================================================

	def getcopieroutcomedetail(self, copyid):

		Logging.printinvocation("Retrieving copier outcome detail", "")
		return {'outcomedetail': self.copiermanager.getcopyactionoutcomedetail(copyid)}



	#===============================================================================================
	# Display the monitor
	#===============================================================================================

	def displaymonitordata(self, historyperiod):

		Logging.printinvocation("Loading Monitor History Data (" + historyperiod + ")", "")
		return {'monitoroutput': self.monitormanager.gethistorygraphics(historyperiod)}



	#===============================================================================================
	# Process Copy Intervention
	#===============================================================================================

	def processcopyintervention(self, copyid, intervention):

		Logging.printinvocation("Intervening Copier Action", "")
		self.copiermanager.intervene(copyid, intervention)

		return {'copyactions': self.copiermanager.getcopierpagerefreshdata()}



	#===============================================================================================
	# Process Copy Queue
	#===============================================================================================

	def triggercopier(self, latestcopyid, copyoutcome, notes):

		Logging.printinvocation("Synchronising with Download-Copier", "")
		self.copiermanager.updatecopieractionwithresult(latestcopyid, copyoutcome, notes)

		if self.copiermanager.shouldrefreshtvshowdata(latestcopyid) is True:
			self.fileoptions.importtvshows(notes)

		return self.copiermanager.startnextcopieraction()



	#===============================================================================================
	# Process Operator Queue
	#===============================================================================================

	# def triggeroperator(self, torrentdata, sessiondata, monitorhistory):
	#
	# 	Logging.printinvocation("Synchronising with Download-Operator", "")
	#
	# 	if torrentdata is not None:
	# 		self.torrentmanager.refreshtorrentlist(torrentdata)
	# 		if sessiondata is not None:
	# 			self.monitormanager.refreshsessiondata(sessiondata, self.torrentmanager.getaggregates())
	# 			self.delugemanager.lognewdatashare()
	#
	# 	if monitorhistory is True:
	# 		outcome = self.monitormanager.addtohistory()
	# 		ConfigFile.savemonitor(outcome)
	#
	# 	return self.delugemanager.getnextoperatoraction()!!!!!!!!!!!




	def determinewebmode(self):

		return True # ConfigFile.getwebhostconfig()
