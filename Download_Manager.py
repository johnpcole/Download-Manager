from codebase.fileprocessing_component import fileprocessing_module as FileManager
from codebase.common_components.logging_framework import logging_module as Logging
from codebase.common_components.webserver_framework import webserver_module as WebServer
from codebase import manager_module as Manager


Logging.printinvocation("Starting Download-Manager Application", "")

manager = Manager.createmanager("Public Daemon")

webmode = manager.determinewebmode()

website = WebServer.createwebsite()



#===============================================================================================
# Load the Torrents List as new page
#===============================================================================================

@website.route('/')
def initialiselistpage():

	result = manager.initialiselistpage()
	return WebServer.makehtml(	'index.html',
								torrentlist=result['torrentlist'],
								stats=result['stats'])



#===============================================================================================
# Refresh Torrents List on existing page, after performing a bulk action if required
#===============================================================================================

@website.route('/UpdateTorrentsList', methods=['POST'])
def updatelistpage():

	inputdata = WebServer.getrequestdata()
	result = manager.updatelistpage(inputdata["bulkaction"])
	return WebServer.makejson(	torrents=result['torrents'],
								stats=result['stats'])



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	result = manager.initialisetorrentpage(torrentid)
	return WebServer.makehtml(	'torrent.html',
								selectedtorrent=result['selectedtorrent'])



#===============================================================================================
# Refresh an existing Torrent page with Network Data, after performing an action if required
#===============================================================================================

@website.route('/UpdateTorrent', methods=['POST'])
def updatetorrentpage():

	inputdata = WebServer.getrequestdata()
	result = manager.updatetorrentpage(inputdata['torrentid'], inputdata['torrentaction'])
	return WebServer.makejson(	selectedtorrent=result['selectedtorrent'])






#===============================================================================================
# Generate a Monitor History Item
#===============================================================================================

@website.route('/TriggerDelugeMonitor')
def triggermonitor():

	result = manager.triggermonitor()
	return WebServer.makejson(	message=result['message'])






if webmode == True:
	website.run(debug=False, host='0.0.0.0')
else:
	website.run(debug=True)

