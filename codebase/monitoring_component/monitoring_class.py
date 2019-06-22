from .thermometer_subcomponent import thermometer_module as PiThermometer
from .sessiondatameters_subcomponent import sessiondatameters_module as SessionDataMeters
from .historyitem_subcomponent import historyitem_module as HistoryItem
from ..common_components.datetime_datatypes import datetime_module as DateTime
from . import monitoring_privatefunctions as Functions
from .network_subcomponent import network_module as Network



class DefineMonitor:

	def __init__(self):

		# An array of meter graph data, capturing important overall torrenting stats
		self.sessionmeters = SessionDataMeters.createsessiondatameters()

		# An array of historic monitor history
		self.monitorhistory = []

		self.networkstatus = 0

		# Defines the granularity of display of monitor data
		self.erasize = 4 # Ten minute intervals
		self.boxwidth = 3
		self.horizontaloffset = 3
		self.verticaloffset = 123
# =========================================================================================
# Connects to the torrent daemon, and updates the local list of torrents
# =========================================================================================

	def refreshsessionmeters(self, sessiondata):

		self.sessionmeters.updatesessiondata(sessiondata, PiThermometer.gettemperature())
		self.networkstatus = Network.getvpnstatus()

# =========================================================================================
# Generates an array of stat numerics, required to draw the meter graphs
# =========================================================================================

	def getsessionmeters(self):

		outcome = self.sessionmeters.getstats()
		outcome['networkstatus'] = str(self.networkstatus)
		return outcome

# =========================================================================================

	def addhistoryentry(self, monitordata):

		currentdatetime = DateTime.getnow()
		self.monitorhistory.append(HistoryItem.createhistoryitem(currentdatetime, monitordata, Network.getvpnstatus()))
		if currentdatetime.gettimevalue() < 600:
			print("Before clean up: ", len(self.monitorhistory))
			self.clearuphistory(currentdatetime)
			print("After clean up: ", len(self.monitorhistory))

# =========================================================================================

#	def gethistory(self, startpointdatetime, endpointdatetime):
#
#		outcome = []
#		for historyitem in self.monitorhistory:
#			currentdatetime = historyitem.getdatetime()
#			if DateTime.isfirstlaterthansecond(currentdatetime, startpointdatetime):
#				if DateTime.isfirstlaterthansecond(endpointdatetime, currentdatetime):
#					outcome.append(historyitem.getalldata())
#
#		return outcome

# =========================================================================================

#	def getlatestdayshistory(self):
#
#		endpointdatetime = DateTime.getnow()
#		startpointdatetime = DateTime.createfromobject(endpointdatetime)
#		startpointdatetime.adjustdays(-1)
#		return self.gethistory(startpointdatetime, endpointdatetime)

# =========================================================================================

	def getlatesthistoryitemforsaving(self):

		if len(self.monitorhistory) > 0:
			latesthistoryitem = self.monitorhistory[-1]
			outcome = latesthistoryitem.getsavedata()

		else:
			outcome = "0|0|0|0|0|0|0|True"

		return outcome



	def restorehistory(self, saveddatalist):

		for dataitem in saveddatalist:
			self.monitorhistory.append(HistoryItem.createfromfile(dataitem))



#	def getmonitorstate(self):
#
#		return {"History_Size": len(self.monitorhistory), "Latest_Entry": self.getlatesthistoryitemforsaving()}



	def gethistorygraphics(self):

		outcome = {}
		origintimedate = DateTime.getnow()
		origintimedate.adjusthours(-42)
		boxoutcome = []
		baroutcome = []
		uploadtally = 0
		for historyitem in self.monitorhistory:
			boxoutcome.extend(historyitem.getstatusgraphicdata(self.horizontaloffset, self.verticaloffset, self.boxwidth, 5, origintimedate, self.erasize))
			baroutcome.extend(historyitem.getuploadgraphicdata(self.horizontaloffset, self.verticaloffset, self.boxwidth, uploadtally, origintimedate, self.erasize))
			uploadtally = historyitem.getuploaded()

		outcome["boxes"] = boxoutcome
		outcome["bars"] = baroutcome
		outcome.update(Functions.getxaxis(origintimedate, self.erasize, self.boxwidth, self.horizontaloffset, self.verticaloffset))

		return outcome




	def clearuphistory(self, currentdatetime):

		threshold = DateTime.createfromobject(currentdatetime)
		threshold.adjustdays(-5)
		newhistorylist = []
		for historyitem in self.monitorhistory:
			if DateTime.isfirstlaterthansecond(historyitem.getdatetime(), threshold) == True:
				newhistorylist.append(historyitem)

		self.monitorhistory = newhistorylist.copy()




