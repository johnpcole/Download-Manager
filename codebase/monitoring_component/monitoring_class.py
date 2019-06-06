from .thermometer_subcomponent import thermometer_module as PiThermometer
from .sessiondatameters_subcomponent import sessiondatameters_module as SessionDataMeters
from .historyitem_subcomponent import historyitem_module as HistoryItem
from ..common_components.datetime_datatypes import datetime_module as DateTime



class DefineMonitor:

	def __init__(self):

		# An array of meter graph data, capturing important overall torrenting stats
		self.sessionmeters = SessionDataMeters.createsessiondatameters()

		# An array of historic monitor history
		self.monitorhistory = []


# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshsessionmeters(self, sessiondata):

		self.sessionmeters.updatesessiondata(sessiondata, PiThermometer.gettemperature())

# =========================================================================================
# Generates an array of stat numerics, required to draw the meter graphs
# =========================================================================================

	def getsessionmeters(self):

		return self.sessionmeters.getstats()

# =========================================================================================

	def addhistoryentry(self, monitordata):

		self.monitorhistory.append(HistoryItem.createhistoryitem(DateTime.getnow(), monitordata))

# =========================================================================================

	def gethistory(self, startpointdatetime, endpointdatetime):

		outcome = []
		print("==================")
		for historyitem in self.monitorhistory:
			currentdatetime = historyitem.getdatetime()
			print("Looking up: " + currentdatetime.getiso() + "   " + startpointdatetime.getiso() + "   " + endpointdatetime.getiso())
			if DateTime.isfirstlaterthansecond(currentdatetime, startpointdatetime):
				print("PASSED FIRST TEST")
				if DateTime.isfirstlaterthansecond(endpointdatetime, currentdatetime):
					print("PASSED SECOND TEST")
					outcome.append(historyitem)

		return outcome

# =========================================================================================

	def getlatestdayshistory(self):

		endpointdatetime = DateTime.getnow()
		startpointdatetime = DateTime.createfromobject(endpointdatetime)
		startpointdatetime.adjustdays(-1)
		return self.gethistory(startpointdatetime, endpointdatetime)


