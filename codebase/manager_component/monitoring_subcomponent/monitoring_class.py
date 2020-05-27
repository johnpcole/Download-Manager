from .dashboardmeters_subcomponent import dashboardmeters_module as DashboardMeters
from .history_subcomponent import history_module as History



class DefineMonitor:

	def __init__(self):

		# An array of meter graph data, capturing important overall torrenting stats
		self.dashboardmeters = DashboardMeters.createdashboardmeters()

		# An array of historic monitor history
		self.monitorhistory = History.createhistory()

		# Determines whether the VPN is currently up or down
		self.networkstatus = 0

		self.uploadedtotal = 0

		# Torrent aggregate counts
		self.colourcounts = {'redcount': 0, 'orangecount': 0, 'ambercount': 0, 'yellowcount': 0, 'greencount': 0}



# =========================================================================================
#
# =========================================================================================

	def refreshsessiondata(self, sessiondata):

		self.dashboardmeters.updatesessiondata(sessiondata)

		for index in sessiondata.keys():
			if index == 'vpnstatus':
				self.networkstatus = sessiondata[index]
			elif index == 'uploadedtotal':
				self.uploadedtotal = sessiondata[index]

		#for index in torrentaggregates.keys():
		#	if index in self.colourcounts.keys():
		#		self.colourcounts[index] = torrentaggregates[index]


# =========================================================================================
# Generates an array of stat numerics, required to draw the meter graphs
# =========================================================================================

	def getdashboardmeters(self, isdatarecent):

		if isdatarecent == True:
			outcome = self.dashboardmeters.getmetergraphics()
			if self.networkstatus == 1:
				outcome['networkstatus'] = "vpn_up"
			else:
				outcome['networkstatus'] = "vpn_down"
		else:
			outcome = self.dashboardmeters.getdummymetergraphics()
			outcome['networkstatus'] = "vpn_up"

		return outcome

# =========================================================================================

	def addtohistory(self):

		return self.monitorhistory.addhistoryentry(self.colourcounts, self.networkstatus, self.uploadedtotal,
																				self.dashboardmeters.gettemperature())

# =========================================================================================

	def restoresavedhistory(self, saveddatalist):

		self.monitorhistory.restorehistory(saveddatalist)

# =========================================================================================

	def gethistorygraphics(self, historyperiod):

		return self.monitorhistory.gethistorygraphics(historyperiod)



