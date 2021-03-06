from codebase.common_components.logging_framework import logging_module as Logging
from codebase.common_components.webserver_framework import webserver_module as WebServer
from codebase.manager_component import manager_module as TorrentSet


Logging.printinvocation("Starting Download-Manager Application", "")

torrentset = TorrentSet.createmanager("Public Daemon")
website = WebServer.createwebsite(__name__)



#===============================================================================================
# Load the Torrents List as new page
#===============================================================================================

@website.route('/')
def initialiselistpage():

	result = torrentset.initialiselistpage()
	if 'torrentlist' in result.keys():
		return WebServer.makehtml('index.html', **result)
	else:
		return WebServer.makehtml('index_holding.html', **result)



#===============================================================================================
# Refresh Torrents List on existing page
#===============================================================================================

@website.route('/UpdateTorrentsList', methods=['POST'])
def updatelistpage():

	inputdata = WebServer.getrequestdata()
	result = torrentset.updatelistpage()
	return WebServer.makejson(**result)



#===============================================================================================
# Perform a bulk start or stop
#===============================================================================================

@website.route('/PerformBulkTorrentAction', methods=['POST'])
def performbulkaction():

	inputdata = WebServer.getrequestdata()
	result = torrentset.performbulkaction(inputdata["bulkaction"])
	return WebServer.makejson(**result)



#===============================================================================================
# Perform a bulk action if required
#===============================================================================================

@website.route('/PerformTVShowRescan', methods=['POST'])
def rescantvshows():

	inputdata = WebServer.getrequestdata()
	result = torrentset.rescantvshows()
	return WebServer.makejson(**result)



#===============================================================================================
# Load a Torrent with Network & Configuration Data as new page
#===============================================================================================

@website.route('/Torrent=<torrentid>')
def initialisetorrentpage(torrentid):

	result = torrentset.initialisetorrentpage(torrentid)
	if 'selectedtorrent' in result.keys():
		return WebServer.makehtml('torrent.html', **result)
	else:
		return WebServer.makehtml('holding.html', **result)



#===============================================================================================
# Refresh an existing Torrent page with Network Data
#===============================================================================================

@website.route('/UpdateTorrent', methods=['POST'])
def updatetorrentpage():

	inputdata = WebServer.getrequestdata()
	result = torrentset.updatetorrentpage(inputdata['torrentid'])
	return WebServer.makejson(**result)




#===============================================================================================
# Performing an action if required
#===============================================================================================

@website.route('/PerformTorrentAction', methods=['POST'])
def performtorrentaction():

	inputdata = WebServer.getrequestdata()
	result = torrentset.performtorrentaction(inputdata['torrentid'], inputdata['torrentaction'])
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

	result = torrentset.displaymonitordata("Initial Page Load with no data")
	return WebServer.makehtml('monitor.html', **result)



#===============================================================================================
# Display the monitor
#===============================================================================================

@website.route('/MonitorData', methods=['POST'])
def displaymonitordata():

	inputdata = WebServer.getrequestdata()
	result = torrentset.displaymonitordata(inputdata['timespan'])
	return WebServer.makejson(**result)



#===============================================================================================
# Display the copier
#===============================================================================================

@website.route('/Copier')
def displaycopier():

	result = torrentset.displaycopier()
	return WebServer.makehtml('copier.html', **result)



#===============================================================================================
# Refresh Torrents List on existing page, after performing a bulk action if required
#===============================================================================================

@website.route('/UpdateCopierList', methods=['POST'])
def updatecopierpage():

	inputdata = WebServer.getrequestdata()
	result = torrentset.updatecopierpage()
	return WebServer.makejson(**result)



#===============================================================================================
# Gets specific copy action information
#===============================================================================================

@website.route('/GetCopyActionDetail', methods=['POST'])
def getcopieroutcome():

	inputdata = WebServer.getrequestdata()
	result = torrentset.getcopieroutcomedetail(inputdata['copyid'])
	return WebServer.makejson(**result)



#===============================================================================================
# Gets specific copy action information
#===============================================================================================

@website.route('/PerformCopyIntervention', methods=['POST'])
def performcopyintervention():

	inputdata = WebServer.getrequestdata()
	result = torrentset.processcopyintervention(inputdata['copyid'], inputdata['intervention'])
	return WebServer.makejson(**result)



#===============================================================================================
# Generate a Copier Interaction
#===============================================================================================

@website.route('/TriggerDownloadCopier', methods=['POST'])
def triggercopier():

	inputdata = WebServer.getrequestdata()
	result = torrentset.triggercopier(inputdata['copyid'], inputdata['outcome'], inputdata['notes'])
	return WebServer.makejson(**result)



#===============================================================================================
# Generate a Copier Interaction
#===============================================================================================

@website.route('/TriggerDownloadOperator', methods=['POST'])
def triggeroperator():

	inputdata = WebServer.getrequestdata()
	#print("===========================================================")
	#print("INPUT KEYS: ", inputdata.keys())
	#print("===========================================================")
	if ("torrents" in inputdata.keys()) and ("sessiondata" in inputdata.keys()
																			and ("monitorhistory" in inputdata.keys())):
		result = torrentset.triggeroperator(inputdata['torrents'], inputdata['sessiondata'],
																							inputdata['monitorhistory'])
	else:
		result = torrentset.triggeroperator(None, None, None)
	return WebServer.makejson(**result)



#===============================================================================================
# Start the web server
#===============================================================================================


if __name__ == "__main__":
	Logging.printinvocation("Starting Web Server as standalone application", "")
	if torrentset.determinewebmode() == True:
		website.run(debug=False, host='0.0.0.0')
	else:
		website.run(debug=True)
else:
	Logging.printinvocation("Starting Web Server as embedded application", "")



