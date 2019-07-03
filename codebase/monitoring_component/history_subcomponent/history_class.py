from .historyitem_subcomponent import historyitem_module as HistoryItem
from ...common_components.datetime_datatypes import datetime_module as DateTime
from . import history_privatefunctions as Functions
from ...common_components.datetime_datatypes import eras_module as EraFunctions



class DefineHistory:

	def __init__(self):

		# An array of historic monitor history
		self.monitorhistory = []

		# Defines the granularity of display of monitor data
		self.erasize = 4        # Ten minute intervals
		self.longerasize = 5    # Hour intervals

		# Screen metrics
		self.graphcolumnwidth = 3
		self.graphhorizontaloffset = 5
		self.graphupperverticaloffset = 150   #    17 for heading
		self.graphlowerverticaloffset = 320   #   187 for heading
		self.graphthreeverticaloffset = 490   #   ??? for heading
		self.graphfourverticaloffset = 660   #   ??? for heading
		self.graphwidth = 1020
		self.graphheight = 125
		self.graphblockheight = 5

# =========================================================================================

	def addhistoryentry(self, monitordata, networkstatus):

		currentdatetime = DateTime.getnow()
		newhistoryitem = HistoryItem.createhistoryitem(currentdatetime, monitordata, networkstatus)
		self.monitorhistory.append(newhistoryitem)
		self.clearuphistory(currentdatetime)
		return newhistoryitem.getsavedata()



	def restorehistory(self, saveddatalist):

		for dataitem in saveddatalist:
			self.monitorhistory.append(HistoryItem.createfromfile(dataitem))



	def gethistorygraphics(self):

		outcome = {}
		origintimedate = DateTime.getnow()
		longorigintimedate = DateTime.createfromobject(origintimedate)
		origintimedate.adjusthours(-42)
		longorigintimedate.adjustdays(-10)
		longorigintimedate.adjusthours(-12)
#		outcome.update(Functions.getgraphaxes(origintimedate, self.erasize, self.graphcolumnwidth,
#												self.graphhorizontaloffset, self.graphupperverticaloffset,
#												self.graphlowerverticaloffset, self.graphwidth, self.graphheight))
#		outcome.update(Functions.getgraphblocks(origintimedate, self.erasize, self.graphcolumnwidth,
#												self.graphhorizontaloffset, self.graphupperverticaloffset,
#												self.graphlowerverticaloffset, self.graphheight,
#												self.monitorhistory, self.graphblockheight))

		outcome.update(Functions.getlonggraphaxes(longorigintimedate, self.longerasize, self.graphcolumnwidth,
												self.graphhorizontaloffset, self.graphupperverticaloffset,
												self.graphlowerverticaloffset, self.graphwidth, self.graphheight))
		outcome.update(Functions.getlonggraphblocks(longorigintimedate, self.longerasize, self.graphcolumnwidth,
												self.graphhorizontaloffset, self.graphupperverticaloffset,
												self.graphlowerverticaloffset, self.graphheight,
												self.getlonghistory()))

		return outcome




	def clearuphistory(self, currentdatetime):

		if currentdatetime.gettimevalue() < 600:
			print("Before clean up: ", len(self.monitorhistory))
			threshold = DateTime.createfromobject(currentdatetime)
			threshold.adjustdays(-11)
			newhistorylist = []
			for historyitem in self.monitorhistory:
				if DateTime.isfirstlaterthansecond(historyitem.getdatetime(), threshold) == True:
					newhistorylist.append(historyitem)

			self.monitorhistory = newhistorylist.copy()
			print("After clean up: ", len(self.monitorhistory))




	def getlonghistory(self):

		outcome = []
		currentlonghistoryitem = HistoryItem.createblank(DateTime.createfromiso("20100101000000"))
		for historyitem in self.monitorhistory:
			newhour = historyitem.getdatetime()
			if EraFunctions.compareeras(newhour, currentlonghistoryitem.getdatetime(), 5) == True:
				currentlonghistoryitem.cumulate(historyitem)
			else:
				outcome.append(currentlonghistoryitem)
				currentlonghistoryitem = HistoryItem.createblank(EraFunctions.geteraasobject(newhour, 5))
		if EraFunctions.compareeras(currentlonghistoryitem.getdatetime(), DateTime.getnow(), 5) == False:
			outcome.append(currentlonghistoryitem)
		return outcome



