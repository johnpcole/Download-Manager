from .thermometer_subcomponent import thermometer_module as PiThermometer
from .sessiondatameters_subcomponent import sessiondatameters_module as SessionDataMeters
from .network_subcomponent import network_module as Network
from .history_subcomponent import history_module as History


class DefineMonitor:

	def __init__(self):

		# An array of meter graph data, capturing important overall torrenting stats
		self.sessionmeters = SessionDataMeters.createsessiondatameters()

		# An array of historic monitor history
		self.monitorhistory = History.createhistory()

		# Determines whether the VPN is currently up or down
		self.networkstatus = 0



# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshsessionmeters(self, sessiondata):

		self.sessionmeters.updatesessiondata(sessiondata, PiThermometer.getoveralltemperature())
		self.networkstatus = Network.getvpnstatus()

# =========================================================================================
# Generates an array of stat numerics, required to draw the meter graphs
# =========================================================================================

	def getsessionmeters(self):

		outcome = self.sessionmeters.getstats()
		if self.networkstatus == 1:
			outcome['networkstatus'] = "indexbanner_good"
		else:
			outcome['networkstatus'] = "indexbanner_bad"
		return outcome

# =========================================================================================

	def addtohistory(self, monitordata):

		return self.monitorhistory.addhistoryentry(monitordata, Network.getvpnstatus(), PiThermometer.getoveralltemperature())

# =========================================================================================

	def restoresavedhistory(self, saveddatalist):

		self.monitorhistory.restorehistory(saveddatalist)

# =========================================================================================

	def gethistorygraphics(self):

		return self.monitorhistory.gethistorygraphics()



