from .thermometer_subcomponent import thermometer_module as PiThermometer
from .sessiondatameters_subcomponent import sessiondatameters_module as SessionDataMeters
from .historyitem_subcomponent import historyitem_module as HistoryItem
from ..common_components.datetime_datatypes import datetime_module as DateTime
from ..common_components.datetime_datatypes import eras_module as EraFunctions


class DefineMonitor:

	def __init__(self):

		# An array of meter graph data, capturing important overall torrenting stats
		self.sessionmeters = SessionDataMeters.createsessiondatameters()

		# An array of historic monitor history
		self.monitorhistory = []

		# Defines the granularity of display of monitor data
		self.erasize = 4 # Ten minute intervals

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

		return {"History_Size": len(self.monitorhistory), "Latest_Entry": self.getlatesthistoryitemforsaving()}



	def gethistorygraphics(self):

		nowtimedate = DateTime.getnow()
		nowtimedate.adjusthours(-42)
		boxoutcome = []
		for historyitem in self.monitorhistory:
			boxoutcome.extend(historyitem.getgraphicdata(3, 123, 3, 5, nowtimedate, self.erasize))

		markersoutcome = []
		currentmarker = EraFunctions.geteraasobject(nowtimedate, self.erasize)
		markerposition = EraFunctions.geteradifference(nowtimedate, currentmarker, self.erasize)
		indexer = 0
		while indexer < 100: #markerposition < 260:
			indexer = indexer + 1
			print("Current Marker", currentmarker.getiso(), "   Marker Position", markerposition)
			instruction = 'x1="' + str(markerposition) + '" y1=150" x2="' + str(markerposition) + '" y2="160"'
			markersoutcome.append(instruction)
			currentmarker.adjusthours(3)
			markerposition = EraFunctions.geteradifference(nowtimedate, currentmarker, self.erasize)


		return {"boxes": boxoutcome, "markers": markersoutcome}



