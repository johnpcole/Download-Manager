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
		for historyitem in self.monitorhistory:
			currentdatetime = historyitem.getdatetime()
			if DateTime.isfirstlaterthansecond(currentdatetime, startpointdatetime):
				if DateTime.isfirstlaterthansecond(endpointdatetime, currentdatetime):
					outcome.append(historyitem.getalldata())

		return outcome

# =========================================================================================

	def getlatestdayshistory(self):

		endpointdatetime = DateTime.getnow()
		startpointdatetime = DateTime.createfromobject(endpointdatetime)
		startpointdatetime.adjustdays(-1)
		return self.gethistory(startpointdatetime, endpointdatetime)

# =========================================================================================

	def getlatesthistoryitemforsaving(self):

		if len(self.monitorhistory) > 0:
			latesthistoryitem = self.monitorhistory[-1]
			outcome = latesthistoryitem.getsavedata()

		else:
			outcome = "||||||"

		return outcome




	def getmonitorstate(self):

		return len(self.monitorhistory)



	def gethistorygraphics(self):

		outcome = []
		horizontalposition = 3 + (4 * 200)
		for historyitem in self.monitorhistory:
			horizontalposition = horizontalposition + 4
			outcome.extend(historyitem.getgraphicdata(horizontalposition, 123, 3, 5))
		print(outcome)
		return outcome



