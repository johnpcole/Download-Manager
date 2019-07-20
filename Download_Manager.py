from common_components.logging_framework import logging_module as Logging
from common_components.webserver_framework import webserver_module as WebServer
from manager_component import manager_module as TorrentSet


Logging.printinvocation("Starting Download-Manager Application", "")

torrentset = TorrentSet.createmanager("Public Daemon")
website = WebServer.createwebsite(__name__)



#===============================================================================================
# Load the Torrents List as new page
#===============================================================================================

@website.route('/')
def initialiselistpage():

	result = torrentset.initialiselistpage()
	return WebServer.makehtml('index.html', **result)



#===============================================================================================
# Refresh Torrents List on existing page, after performing a bulk action if required
#===============================================================================================

@website.route('/UpdateTorrentsList', methods=['POST'])
def updatelistpage():

	inputdata = WebServer.getrequestdata()
	result = torrentset.updatelistpage(inputdata["bulkaction"])
	return WebServer.makejson(**result)



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	result = torrentset.initialisetorrentpage(torrentid)
	return WebServer.makehtml('torrent.html', **result)



#===============================================================================================
# Refresh an existing Torrent page with Network Data, after performing an action if required
#===============================================================================================

@website.route('/UpdateTorrent', methods=['POST'])
def updatetorrentpage():

	inputdata = WebServer.getrequestdata()
	result = torrentset.updatetorrentpage(inputdata['torrentid'], inputdata['torrentaction'])
	return WebServer.makejson(**result)



#===============================================================================================
# Copies Files
#===============================================================================================

@website.route('/CopyTorrent', methods=['POST'])
def copytorrent():

	inputdata = WebServer.getrequestdata()
	result = torrentset.copytorrent(inputdata['copyinstruction'])
	return WebServer.makejson(**result)



#===============================================================================================
# Delete Torrent
#===============================================================================================

@website.route('/DeleteTorrent', methods=['POST'])
def deletetorrent():

	inputdata = WebServer.getrequestdata()
	result = torrentset.deletetorrent(inputdata['deleteinstruction'])
	return WebServer.makejson(**result)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data, after saving new instructions
# ===============================================================================================

@website.route('/ReconfigureTorrent', methods=['POST'])
def reconfiguretorrentconfiguration():

	inputdata = WebServer.getrequestdata()
	result = torrentset.reconfiguretorrentconfiguration(inputdata['torrentid'], inputdata['newconfiguration'])
	return WebServer.makejson(**result)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate edit fields
# ===============================================================================================

@website.route('/EditTorrent', methods=['POST'])
def edittorrentconfiguration():

	inputdata = WebServer.getrequestdata()
	result = torrentset.edittorrentconfiguration(inputdata['torrentid'])
	return WebServer.makejson(**result)



# ===============================================================================================
# Refresh an existing Torrent page with Configuration Data used to populate the Season edit field
# ===============================================================================================

@website.route('/GetTVShowSeasons', methods=['POST'])
def updatetvshowseasonslist():

	inputdata = WebServer.getrequestdata()
	result = torrentset.updatetvshowseasonslist(inputdata['tvshow'])
	return WebServer.makejson(**result)



# ===============================================================================================
# Performs a Torrent Addition, and returns the new Torrent Data (to be displayed on a new Page)
# ===============================================================================================

@website.route('/AddTorrent', methods=['POST'])
def addnewtorrent():

	inputdata = WebServer.getrequestdata()
	result = torrentset.addnewtorrent(inputdata['newurl'])
	return WebServer.makejson(**result)



#===============================================================================================
# Display the logging file contents
#===============================================================================================

@website.route('/Logs')
def displaylogs():

	result = torrentset.displaylogs(True)
	return WebServer.makehtml('logs.html', **result)



#===============================================================================================
# Display the monitor
#===============================================================================================

@website.route('/Monitor')
def displaymonitor():

	result = torrentset.displaymonitor()
	return WebServer.makehtml('monitor.html', **result)






#===============================================================================================
# Generate a Monitor History Item
#===============================================================================================

@website.route('/TriggerDelugeMonitor')
def triggermonitor():

	result = torrentset.triggermonitor()
	return WebServer.makejson(**result)




#===============================================================================================
# Start the web server
#===============================================================================================


if __name__ == "__main__":
	Logging.printinvocation("Starting Web Server (as standalone application)", "")
	if torrentset.determinewebmode() == True:
		website.run(debug=False, host='0.0.0.0')
	else:
		website.run(debug=True)
else:
	Logging.printinvocation("Starting Web Server (as embedded application)", "")


