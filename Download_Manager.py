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

	outputdata = manager.initialiselistpage()
	return WebServer.makehtml('index.html', outputdata)



#===============================================================================================
# Refresh Torrents List on existing page, after performing a bulk action if required
#===============================================================================================

@website.route('/UpdateTorrentsList', methods=['POST'])
def updatelistpage():

	inputdata = WebServer.getrequestdata()
	outputdata = manager.updatelistpage(inputdata["bulkcation"])
	return WebServer.makejson(outputdata)



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	outputdata = manager.initialisetorrentpage(torrentid)
	return WebServer.makehtml('torrent.html', outputdata)





if webmode == True:
	website.run(debug=False, host='0.0.0.0')
else:
	website.run(debug=True)

