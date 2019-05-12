from codebase.torrenting_component import torrenting_module as TorrentManager
from codebase.fileprocessing_component import fileprocessing_module as FileManager
from flask import Flask as Webserver
from flask import render_template as Webpage
from flask import jsonify as Jsondata
from flask import request as Webpost
from codebase.functions_component import functions_module as Functions

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

	Functions.printout("Refreshing Torrents List")
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
		Functions.printout(bulkaction + "ing all Torrents")
		torrentmanager.bulkprocessalltorrents(bulkaction)
	elif bulkaction == "RescanFileServer":
		Functions.printout("Rescanning File-Server for TV Shows & Seasons")
		librarymanager.discovertvshows()
	elif bulkaction != "Refresh":
		Functions.printout("Unknown Torrents List Update Action: " + bulkaction)
	torrentmanager.refreshtorrentlist()
	return Jsondata(torrents=torrentmanager.gettorrentlistdata("refresh"), stats = torrentmanager.getstats())



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printout("Refreshing Torrent " + torrentid)
		torrentmanager.refreshtorrentdata(torrentid)
		return Webpage('torrent.html', selectedtorrent = torrentmanager.gettorrentdata(torrentid, "initialise"))
	else:
		Functions.printout("Unknown Torrent Specified; Returning to Torrents List")
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
			Functions.printout(torrentaction + "ing Torrent " + torrentid)
			torrentmanager.processonetorrent(torrentid, torrentaction)
		elif torrentaction != "Refresh":
			Functions.printout("Unknown Torrent Update Action: " + torrentaction)
		Functions.printout("Refreshing Torrent " + torrentid)
		torrentmanager.refreshtorrentdata(torrentid)
		return Jsondata(selectedtorrent=torrentmanager.gettorrentdata(torrentid, "refresh"))
	else:
		Functions.printout("Updating unknown torrent " + torrentid)



#===============================================================================================
# Copies Files
#===============================================================================================

@website.route('/CopyTorrent', methods=['POST'])
def copytorrent():

	rawdata = Webpost.get_json()
	torrentid = rawdata['copyinstruction']
	if torrentid != "!!! CONTINUE EXISTING COPY PROCESS !!!":
		if torrentmanager.validatetorrentid(torrentid) == True:
			Functions.printout("Copying Torrent " + torrentid)
			librarymanager.queuefilecopy(torrentmanager.getcopyactions(torrentid))
		else:
			Functions.printout("Copying unknown torrent " + torrentid)
		refreshmode = False
	else:
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
		Functions.printout("Deleting Torrent " + torrentid)
		torrentmanager.processonetorrent(torrentid, "Delete")
	else:
		Functions.printout("Deleting unknown torrent " + torrentid)
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
		Functions.printout("Reconfiguring Torrent " + torrentid)
		torrentmanager.reconfiguretorrent(torrentid, rawdata['newconfiguration'])
		FileManager.saveconfigs(torrentmanager.getconfigs())
		return Jsondata(selectedtorrent = torrentmanager.gettorrentdata(torrentid, "reconfigure"))
	else:
		Functions.printout("Reconfiguring unknown torrent " + torrentid)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate edit fields
# ===============================================================================================

@website.route('/EditTorrent', methods=['POST'])
def edittorrentconfiguration():

	rawdata = Webpost.get_json()
	torrentid = rawdata['torrentid']
	if torrentmanager.validatetorrentid(torrentid) == True:
		Functions.printout("Edit Torrent " + torrentid)
		wastetime()
		torrentdata = torrentmanager.gettorrentdata(torrentid, "prepareedit")
		return Jsondata(selectedtorrent=torrentdata,
									listitems=librarymanager.getdropdownlists(torrentdata['tvshowname']))
	else:
		Functions.printout("Edit unknown torrent " + torrentid)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate the Season edit field
# ===============================================================================================

@website.route('/GetTVShowSeasons', methods=['POST'])
def updatetvshowseasonslist():

	Functions.printout("Getting TV Show Data")
	rawdata = Webpost.get_json()
	wastetime()
	return Jsondata(seasons=librarymanager.gettvshowseasons(rawdata['tvshow']))



# ===============================================================================================
# Performs a Torrent Addition, and returns the new Torrent Data (to be displayed on a new Page)
# ===============================================================================================

@website.route('/AddTorrent', methods=['POST'])
def addnewtorrent():

	Functions.printout("Adding New Torrent")
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

	Functions.printout("Getting Application Log")
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

