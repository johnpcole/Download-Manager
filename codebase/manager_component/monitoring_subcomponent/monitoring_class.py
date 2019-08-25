from .sessiondatameters_subcomponent import sessiondatameters_module as SessionDataMeters
from .history_subcomponent import history_module as History


class DefineMonitor:

	def __init__(self):

		# An array of meter graph data, capturing important overall torrenting stats
		self.sessionmeters = SessionDataMeters.createsessiondatameters()

		# An array of historic monitor history
		self.monitorhistory = History.createhistory()

		# Determines whether the VPN is currently up or down
		self.networkstatus = 0

		# Torrent aggregate counts
		self.torrentaggregates = {'downloadcount': 0, 'activedownloads': 0, 'uploadcount': 0, 'activeuploads': 0,
									'redcount': 0, 'orangecount': 0, 'ambercount': 0, 'yellowcount': 0, 'greencount': 0}


# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshmonitordata(self, sessiondata, torrentaggregates):

		self.sessionmeters.updatesessiondata(sessiondata)

		if 'vpnstatus' in sessiondata.keys():
			self.networkstatus = sessiondata['vpnstatus']

		self.torrentaggregates = torrentaggregates

# =========================================================================================
# Generates an array of stat numerics, required to draw the meter graphs
# =========================================================================================

	def getsessionmeters(self):

		outcome = self.sessionmeters.getstats()
		if self.networkstatus == 1:
			outcome['networkstatus'] = "vpn_up"
		else:
			outcome['networkstatus'] = "vpn_down"
		return outcome

# =========================================================================================

	#def addtohistory(self):

		#return self.monitorhistory.addhistoryentry(monitordata, Network.getvpnstatus(), PiThermometer.getoveralltemperature())

# =========================================================================================

	def restoresavedhistory(self, saveddatalist):

		self.monitorhistory.restorehistory(saveddatalist)

# =========================================================================================

	def gethistorygraphics(self):

		return self.monitorhistory.gethistorygraphics()



