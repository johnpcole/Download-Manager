from codebase.torrenting_component import torrenting_module as TorrentManager
from codebase.fileprocessing_component import fileprocessing_module as FileManager
from flask import Flask as Webserver
from flask import render_template as Webpage
from flask import jsonify as Jsondata
from flask import request as Webpost
from codebase.common_components.dataconversion_framework import dataconversion_module as Functions

Functions.printinvocation("Starting Download-Manager Application", "")

librarymanager = FileManager.createmanager(FileManager.getlibraryconnectionconfig())
torrentmanager = TorrentManager.createmanager(FileManager.gettorrentconnectionconfig())
torrentmanager.setconfigs(FileManager.loadconfigs())
webmode = FileManager.getwebhostconfig()

website = Webserver(__name__)



#===============================================================================================
# Load the Torrents List as new page
#===============================================================================================

@website.route('/')
def initialiselistpage():

	Functions.printinvocation("Loading All Torrents List Page", "")
	torrentmanager.refreshtorrentlist("Download-Manager")
	return Webpage('index.html', torrentlist=torrentmanager.gettorrentlistdata("initialise"), stats=torrentmanager.getstats())



#===============================================================================================
# Refresh Torrents List on existing page, after performing a bulk action if required
#===============================================================================================

@website.route('/UpdateTorrentsList', methods=['POST'])
def updatelistpage():

	rawdata = Webpost.get_json()
	bulkaction = rawdata["bulkaction"]
	if (bulkaction == "Start") or (bulkaction == "Stop"):
		Functions.printinvocation(bulkaction + "ing all Torrents", "")
		torrentmanager.bulkprocessalltorrents(bulkaction)
	elif bulkaction == "RescanFileServer":
		Functions.printinvocation("Rescanning File-Server for TV Shows & Seasons", "")
		librarymanager.discovertvshows()
	elif bulkaction == "Refresh":
		Functions.printinvocation("Refreshing All Torrents List Page", "")
	else:
		Functions.printinvocation("Unknown Torrents List Update Action: " + bulkaction, "")
	torrentmanager.refreshtorrentlist("Download-Manager")
	return Jsondata(torrents=torrentmanager.gettorrentlistdata("refresh"), stats=torrentmanager.getstats())



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printinvocation("Loading Specific Torrent Page", torrentid)
		torrentmanager.refreshtorrentdata(torrentid)
		return Webpage('torrent.html', selectedtorrent=torrentmanager.gettorrentdata(torrentid, "initialise"))
	else:
		Functions.printinvocation("Returning to Torrents List; Unknown Torrent Specified", torrentid)
		torrentmanager.refreshtorrentlist("Download-Manager")
		return Webpage('index.html', torrentlist=torrentmanager.gettorrentlistdata("initialise"))



#===============================================================================================
# Refresh an existing Torrent page with Network Data, after performing an action if required
#===============================================================================================

@website.route('/UpdateTorrent', methods=['POST'])
def updatetorrentpage():

	rawdata = Webpost.get_json()
	torrentid = rawdata['torrentid']
	if torrentmanager.validatetorrentid(torrentid) == True:
		torrentaction = rawdata['torrentaction']
		if (torrentaction == "Start") or (torrentaction == "Stop"):
			Functions.printinvocation(torrentaction + "ing Torrent", torrentid )
			torrentmanager.processonetorrent(torrentid, torrentaction)
		elif torrentaction == "Refresh":
			Functions.printinvocation("Refreshing Specific Torrent Page", torrentid)
		else:
			Functions.printinvocation("Unknown Torrent Update Action: " + torrentaction, torrentid)
		torrentmanager.refreshtorrentdata(torrentid)
		return Jsondata(selectedtorrent=torrentmanager.gettorrentdata(torrentid, "refresh"))
	else:
		Functions.printinvocation("Requested Update to Unknown Torrent", torrentid)



#===============================================================================================
# Copies Files
#===============================================================================================

@website.route('/CopyTorrent', methods=['POST'])
def copytorrent():

	rawdata = Webpost.get_json()
	torrentid = rawdata['copyinstruction']
	if torrentid != "!!! CONTINUE EXISTING COPY PROCESS !!!":
		if torrentmanager.validatetorrentid(torrentid) == True:
			Functions.printinvocation("Initiating Torrent Copy", torrentid)
			librarymanager.queuefilecopy(torrentmanager.getcopyactions(torrentid))
		else:
			Functions.printinvocation("Requested Initiate Torrent Copy of Unknown Torrent", torrentid)
		refreshmode = False
	else:
		Functions.printinvocation("Continuing Torrent Copy", "")
		wastetime()
		refreshmode = librarymanager.processfilecopylist()
	return Jsondata(copydata=librarymanager.getcopyprocessinfo(), refreshmode=refreshmode)



#===============================================================================================
# Delete Torrent
#===============================================================================================

@website.route('/DeleteTorrent', methods=['POST'])
def deletetorrent():

	rawdata = Webpost.get_json()
	torrentid = rawdata['deleteinstruction']
	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printinvocation("Deleting Torrent", torrentid)
		torrentmanager.processonetorrent(torrentid, "Delete")
	else:
		Functions.printinvocation("Requested Deletion of Unknown Torrent", torrentid)
	return Jsondata(deletedata="Done")



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data, after saving new instructions
# ===============================================================================================

@website.route('/ReconfigureTorrent', methods=['POST'])
def reconfiguretorrentconfiguration():

	rawdata = Webpost.get_json()
	torrentid = rawdata['torrentid']
	wastetime()
	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printinvocation("Saving Reconfigured Torrent", torrentid)
		torrentmanager.reconfiguretorrent(torrentid, rawdata['newconfiguration'])
		FileManager.saveconfigs(torrentmanager.getconfigs())
		return Jsondata(selectedtorrent=torrentmanager.gettorrentdata(torrentid, "reconfigure"))
	else:
		Functions.printinvocation("Requested Save Reconfiguration of Unknown Torrent", torrentid)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate edit fields
# ===============================================================================================

@website.route('/EditTorrent', methods=['POST'])
def edittorrentconfiguration():

	rawdata = Webpost.get_json()
	torrentid = rawdata['torrentid']
	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printinvocation("Starting Torrent Reconfiguration", torrentid)
		wastetime()
		torrentdata = torrentmanager.gettorrentdata(torrentid, "prepareedit")
		return Jsondata(selectedtorrent=torrentdata,
									listitems=librarymanager.getdropdownlists(torrentdata['tvshowname']))
	else:
		Functions.printinvocation("Requested Unknown Torrent Reconfiguration", torrentid)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate the Season edit field
# ===============================================================================================

@website.route('/GetTVShowSeasons', methods=['POST'])
def updatetvshowseasonslist():

	Functions.printinvocation("Getting TV Show Data", "")
	rawdata = Webpost.get_json()
	wastetime()
	return Jsondata(seasons=librarymanager.gettvshowseasons(rawdata['tvshow']))



# ===============================================================================================
# Performs a Torrent Addition, and returns the new Torrent Data (to be displayed on a new Page)
# ===============================================================================================

@website.route('/AddTorrent', methods=['POST'])
def addnewtorrent():

	Functions.printinvocation("Adding New Torrent", "")
	rawdata = Webpost.get_json()
	newid = torrentmanager.addnewtorrenttoclient(rawdata['newurl'])
	wastetime()
	#torrentmanager.refreshtorrentlist()
	return Jsondata(newtorrentid=newid)



#===============================================================================================
# Display the logging file contents
#===============================================================================================

@website.route('/Logs')
def displaylogs():

	Functions.printinvocation("Loading Application Log Page", "")
	return Webpage('logs.html', loggingoutput=FileManager.getloggingdata(False))


@website.route('/VerboseLogs')
def displayverboselogs():

	Functions.printinvocation("Loading Application Verbose Log Page", "")
	return Webpage('logs.html', loggingoutput=FileManager.getloggingdata(True))




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

