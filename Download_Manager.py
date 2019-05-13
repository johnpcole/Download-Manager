from codebase.torrenting_component import torrenting_module as TorrentManager
from codebase.fileprocessing_component import fileprocessing_module as FileManager
from flask import Flask as Webserver
from flask import render_template as Webpage
from flask import jsonify as Jsondata
from flask import request as Webpost
from codebase.functions_component import functions_module as Functions

Functions.printout("> Starting Download-Manager Application")

librarymanager = FileManager.createmanager(FileManager.getlibraryconnectionconfig())
torrentmanager = TorrentManager.createmanager(FileManager.gettorrentconnectionconfig())
torrentmanager.refreshtorrentlist()
torrentmanager.setconfigs(FileManager.loadconfigs())
webmode = FileManager.getwebhostconfig()

website = Webserver(__name__)



#===============================================================================================
# Load the Torrents List as new page
#===============================================================================================

@website.route('/')
def initialiselistpage():

	Functions.printout("> Loading All Torrents List Page")
	torrentmanager.refreshtorrentlist()
	return Webpage('index.html', torrentlist = torrentmanager.gettorrentlistdata("initialise"), stats = torrentmanager.getstats())



#===============================================================================================
# Refresh Torrents List on existing page, after performing a bulk action if required
#===============================================================================================

@website.route('/UpdateTorrentsList', methods=['POST'])
def updatelistpage():

	rawdata = Webpost.get_json()
	bulkaction = rawdata["bulkaction"]
	if (bulkaction == "Start") or (bulkaction == "Stop"):
		Functions.printout("> " + bulkaction + "ing all Torrents")
		torrentmanager.bulkprocessalltorrents(bulkaction)
	elif bulkaction == "RescanFileServer":
		Functions.printout("> Rescanning File-Server for TV Shows & Seasons")
		librarymanager.discovertvshows()
	elif bulkaction == "Refresh":
		Functions.printout("> Refreshing All Torrents List Page")
	else:
		Functions.printout("> Unknown Torrents List Update Action: " + bulkaction)
	torrentmanager.refreshtorrentlist()
	return Jsondata(torrents=torrentmanager.gettorrentlistdata("refresh"), stats = torrentmanager.getstats())



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printout("> Loading Specific Torrent Page <small>(" + torrentid + ")</small>")
		torrentmanager.refreshtorrentdata(torrentid)
		return Webpage('torrent.html', selectedtorrent = torrentmanager.gettorrentdata(torrentid, "initialise"))
	else:
		Functions.printout("> Returning to Torrents List; Unknown Torrent Specified <small>(" + torrentid + ")</small>")
		torrentmanager.refreshtorrentlist()
		return Webpage('index.html', torrentlist = torrentmanager.gettorrentlistdata("initialise"))



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
			Functions.printout("> " + torrentaction + "ing Torrent <small>(" + torrentid + ")</small>")
			torrentmanager.processonetorrent(torrentid, torrentaction)
		elif torrentaction == "Refresh":
			Functions.printout("> Refreshing Specific Torrent Page <small>(" + torrentid + ")</small>")
		else:
			Functions.printout("> Unknown Torrent Update Action: " + torrentaction)
		torrentmanager.refreshtorrentdata(torrentid)
		return Jsondata(selectedtorrent=torrentmanager.gettorrentdata(torrentid, "refresh"))
	else:
		Functions.printout("> Requested " + torrentaction + " Update to Unknown Torrent <small>(" + torrentid + ")</small>")



#===============================================================================================
# Copies Files
#===============================================================================================

@website.route('/CopyTorrent', methods=['POST'])
def copytorrent():

	rawdata = Webpost.get_json()
	torrentid = rawdata['copyinstruction']
	if torrentid != "!!! CONTINUE EXISTING COPY PROCESS !!!":
		if torrentmanager.validatetorrentid(torrentid) == True:
			Functions.printout("> Initiating Torrent Copy <small>(" + torrentid + ")</small>")
			librarymanager.queuefilecopy(torrentmanager.getcopyactions(torrentid))
		else:
			Functions.printout("> Requested Initiate Torrent Copy of Unknown Torrent <small>(" + torrentid + ")</small>")
		refreshmode = False
	else:
		Functions.printout("> Continuing Torrent Copy")
		wastetime()
		refreshmode = librarymanager.processfilecopylist()
	return Jsondata(copydata = librarymanager.getcopyprocessinfo(), refreshmode = refreshmode)



#===============================================================================================
# Delete Torrent
#===============================================================================================

@website.route('/DeleteTorrent', methods=['POST'])
def deletetorrent():

	rawdata = Webpost.get_json()
	torrentid = rawdata['deleteinstruction']
	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printout("> Deleting Torrent <small>(" + torrentid + ")</small>")
		torrentmanager.processonetorrent(torrentid, "Delete")
	else:
		Functions.printout("> Requested Deletion of Unknown Torrent <small>(" + torrentid + ")</small>")
	return Jsondata(deletedata = "Done")



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data, after saving new instructions
# ===============================================================================================

@website.route('/ReconfigureTorrent', methods=['POST'])
def reconfiguretorrentconfiguration():

	rawdata = Webpost.get_json()
	torrentid = rawdata['torrentid']
	wastetime()
	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printout("> Saving Reconfigured Torrent <small>(" + torrentid + ")</small>")
		torrentmanager.reconfiguretorrent(torrentid, rawdata['newconfiguration'])
		FileManager.saveconfigs(torrentmanager.getconfigs())
		return Jsondata(selectedtorrent = torrentmanager.gettorrentdata(torrentid, "reconfigure"))
	else:
		Functions.printout("> Requested Save Reconfiguration of Unknown Torrent <small>(" + torrentid + ")</small>")



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate edit fields
# ===============================================================================================

@website.route('/EditTorrent', methods=['POST'])
def edittorrentconfiguration():

	rawdata = Webpost.get_json()
	torrentid = rawdata['torrentid']
	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printout("> Starting Torrent Reconfiguration <small>(" + torrentid + ")</small>")
		wastetime()
		torrentdata = torrentmanager.gettorrentdata(torrentid, "prepareedit")
		return Jsondata(selectedtorrent=torrentdata,
									listitems=librarymanager.getdropdownlists(torrentdata['tvshowname']))
	else:
		Functions.printout("> Requested Unknown Torrent Reconfiguration <small>(" + torrentid + ")</small>")



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate the Season edit field
# ===============================================================================================

@website.route('/GetTVShowSeasons', methods=['POST'])
def updatetvshowseasonslist():

	Functions.printout("> Getting TV Show Data")
	rawdata = Webpost.get_json()
	wastetime()
	return Jsondata(seasons=librarymanager.gettvshowseasons(rawdata['tvshow']))



# ===============================================================================================
# Performs a Torrent Addition, and returns the new Torrent Data (to be displayed on a new Page)
# ===============================================================================================

@website.route('/AddTorrent', methods=['POST'])
def addnewtorrent():

	Functions.printout("> Adding New Torrent")
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

	Functions.printout("> Loading Application Log Page")
	return Webpage('logs.html', loggingoutput = FileManager.getloggingdata())





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

