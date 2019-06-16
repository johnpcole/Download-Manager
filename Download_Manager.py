from codebase.torrenting_component import torrenting_module as TorrentManager
from codebase.fileprocessing_component import fileprocessing_module as FileManager
from codebase.monitoring_component import monitoring_module as MonitorManager
from codebase.common_components.logging_framework import logging_module as Logging
from codebase.common_components.webserver_framework import webserver_module as WebServer



Logging.printinvocation("Starting Download-Manager Application", "")

librarymanager = FileManager.createmanager(FileManager.getlibraryconnectionconfig())
torrentmanager = TorrentManager.createmanager(FileManager.gettorrentconnectionconfig())
torrentmanager.setconfigs(FileManager.loadconfigs())
monitormanager = MonitorManager.createmonitor()
webmode = FileManager.getwebhostconfig()

website = WebServer.createwebsite()



#===============================================================================================
# Load the Torrents List as new page
#===============================================================================================

@website.route('/')
def initialiselistpage():

	Logging.printinvocation("Loading All Torrents List Page", "")
	torrentmanager.refreshtorrentlist("Download-Manager")
	monitormanager.refreshsessionmeters(torrentmanager.getsessiondata())
	return WebServer.makehtml('index.html', torrentlist=torrentmanager.gettorrentlistdata("initialise"), stats=monitormanager.getsessionmeters())



#===============================================================================================
# Refresh Torrents List on existing page, after performing a bulk action if required
#===============================================================================================

@website.route('/UpdateTorrentsList', methods=['POST'])
def updatelistpage():

	rawdata = WebServer.getrequestdata()
	bulkaction = rawdata["bulkaction"]
	if (bulkaction == "Start") or (bulkaction == "Stop"):
		Logging.printinvocation(bulkaction + "ing all Torrents", "")
		torrentmanager.bulkprocessalltorrents(bulkaction)
	elif bulkaction == "RescanFileServer":
		Logging.printinvocation("Rescanning File-Server for TV Shows & Seasons", "")
		librarymanager.discovertvshows()
	elif bulkaction == "Refresh":
		Logging.printinvocation("Refreshing All Torrents List Page", "")
	else:
		Logging.printinvocation("Unknown Torrents List Update Action: " + bulkaction, "")
	torrentmanager.refreshtorrentlist("Download-Manager")
	monitormanager.refreshsessionmeters(torrentmanager.getsessiondata())
	return WebServer.makejson(torrents=torrentmanager.gettorrentlistdata("refresh"), stats=monitormanager.getsessionmeters())



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	if torrentmanager.validatetorrentid(torrentid) == True:
		Logging.printinvocation("Loading Specific Torrent Page", torrentid)
		torrentmanager.refreshtorrentdata(torrentid)
		return WebServer.makehtml('torrent.html', selectedtorrent=torrentmanager.gettorrentdata(torrentid, "initialise"))
	else:
		Logging.printinvocation("Returning to Torrents List; Unknown Torrent Specified", torrentid)
		torrentmanager.refreshtorrentlist("Download-Manager")
		return WebServer.makehtml('index.html', torrentlist=torrentmanager.gettorrentlistdata("initialise"))



#===============================================================================================
# Refresh an existing Torrent page with Network Data, after performing an action if required
#===============================================================================================

@website.route('/UpdateTorrent', methods=['POST'])
def updatetorrentpage():

	rawdata = WebServer.getrequestdata()
	torrentid = rawdata['torrentid']
	if torrentmanager.validatetorrentid(torrentid) == True:
		torrentaction = rawdata['torrentaction']
		if (torrentaction == "Start") or (torrentaction == "Stop"):
			Logging.printinvocation(torrentaction + "ing Torrent", torrentid )
			torrentmanager.processonetorrent(torrentid, torrentaction)
		elif torrentaction == "Refresh":
			Logging.printinvocation("Refreshing Specific Torrent Page", torrentid)
		else:
			Logging.printinvocation("Unknown Torrent Update Action: " + torrentaction, torrentid)
		torrentmanager.refreshtorrentdata(torrentid)
		return WebServer.makejson(selectedtorrent=torrentmanager.gettorrentdata(torrentid, "refresh"))
	else:
		Logging.printinvocation("Requested Update to Unknown Torrent", torrentid)



#===============================================================================================
# Copies Files
#===============================================================================================

@website.route('/CopyTorrent', methods=['POST'])
def copytorrent():

	rawdata = WebServer.getrequestdata()
	torrentid = rawdata['copyinstruction']
	if torrentid != "!!! CONTINUE EXISTING COPY PROCESS !!!":
		if torrentmanager.validatetorrentid(torrentid) == True:
			Logging.printinvocation("Initiating Torrent Copy", torrentid)
			librarymanager.queuefilecopy(torrentmanager.getcopyactions(torrentid))
		else:
			Logging.printinvocation("Requested Initiate Torrent Copy of Unknown Torrent", torrentid)
		refreshmode = False
	else:
		Logging.printinvocation("Continuing Torrent Copy", "")
		wastetime()
		refreshmode = librarymanager.processfilecopylist()
	return WebServer.makejson(copydata=librarymanager.getcopyprocessinfo(), refreshmode=refreshmode)



#===============================================================================================
# Delete Torrent
#===============================================================================================

@website.route('/DeleteTorrent', methods=['POST'])
def deletetorrent():

	rawdata = WebServer.getrequestdata()
	torrentid = rawdata['deleteinstruction']
	if torrentmanager.validatetorrentid(torrentid) == True:
		Logging.printinvocation("Deleting Torrent", torrentid)
		torrentmanager.processonetorrent(torrentid, "Delete")
	else:
		Logging.printinvocation("Requested Deletion of Unknown Torrent", torrentid)
	return WebServer.makejson(deletedata="Done")



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data, after saving new instructions
# ===============================================================================================

@website.route('/ReconfigureTorrent', methods=['POST'])
def reconfiguretorrentconfiguration():

	rawdata = WebServer.getrequestdata()
	torrentid = rawdata['torrentid']
	wastetime()
	if torrentmanager.validatetorrentid(torrentid) == True:
		Logging.printinvocation("Saving Reconfigured Torrent", torrentid)
		torrentmanager.reconfiguretorrent(torrentid, rawdata['newconfiguration'])
		FileManager.saveconfigs(torrentmanager.getconfigs())
		return WebServer.makejson(selectedtorrent=torrentmanager.gettorrentdata(torrentid, "reconfigure"))
	else:
		Logging.printinvocation("Requested Save Reconfiguration of Unknown Torrent", torrentid)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate edit fields
# ===============================================================================================

@website.route('/EditTorrent', methods=['POST'])
def edittorrentconfiguration():

	rawdata = WebServer.getrequestdata()
	torrentid = rawdata['torrentid']
	if torrentmanager.validatetorrentid(torrentid) == True:
		Logging.printinvocation("Starting Torrent Reconfiguration", torrentid)
		wastetime()
		torrentdata = torrentmanager.gettorrentdata(torrentid, "prepareedit")
		return WebServer.makejson(selectedtorrent=torrentdata,
									listitems=librarymanager.getdropdownlists(torrentdata['tvshowname']))
	else:
		Logging.printinvocation("Requested Unknown Torrent Reconfiguration", torrentid)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate the Season edit field
# ===============================================================================================

@website.route('/GetTVShowSeasons', methods=['POST'])
def updatetvshowseasonslist():

	Logging.printinvocation("Getting TV Show Data", "")
	rawdata = WebServer.getrequestdata()
	wastetime()
	return WebServer.makejson(seasons=librarymanager.gettvshowseasons(rawdata['tvshow']))



# ===============================================================================================
# Performs a Torrent Addition, and returns the new Torrent Data (to be displayed on a new Page)
# ===============================================================================================

@website.route('/AddTorrent', methods=['POST'])
def addnewtorrent():

	Logging.printinvocation("Adding New Torrent", "")
	rawdata = WebServer.getrequestdata()
	newid = torrentmanager.addnewtorrenttoclient(rawdata['newurl'])
	wastetime()
	#torrentmanager.refreshtorrentlist()
	return WebServer.makejson(newtorrentid=newid)



#===============================================================================================
# Display the logging file contents
#===============================================================================================

@website.route('/Logs')
def displaylogs():

	Logging.printinvocation("Loading Application Log Page", "")
	return WebServer.makehtml('logs.html', loggingoutput=FileManager.getloggingdata(False))


@website.route('/VerboseLogs')
def displayverboselogs():

	Logging.printinvocation("Loading Application Verbose Log Page", "")
	return WebServer.makehtml('logs.html', loggingoutput=FileManager.getloggingdata(True))



#===============================================================================================
# Display the monitor
#===============================================================================================

@website.route('/Monitor')
def displaymonitor():

	return WebServer.makehtml('monitor.html', monitoroutput=monitormanager.gethistorygraphics())



#===============================================================================================
# Generate a Monitor History Item
#===============================================================================================

@website.route('/TriggerDelugeMonitor')
def triggermonitor():

	Logging.printinvocation("Triggering Monitor", "")
	torrentmanager.refreshtorrentlist("Deluge-Monitor")
	monitormanager.addhistoryentry(torrentmanager.getsessiondata())
	FileManager.savemonitor(monitormanager.getlatesthistoryitemforsaving())
	return WebServer.makejson(tester=monitormanager.getmonitorstate())





#-----------------------------------------------


def wastetime():
	if webmode == False:
		for i in range(0, 100):
			print(str(i), "%")
			for j in range(0, 10000):
				pass

#-----------------------------------------------



if webmode == True:
	website.run(debug=False, host='0.0.0.0')
else:
	website.run(debug=True)

