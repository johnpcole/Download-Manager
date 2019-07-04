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
		self.graphupperverticaloffset = 148
		self.graphlowerverticaloffset = 325
		self.graphthreeverticaloffset = 502
		self.graphfourverticaloffset = 679
		self.graphfiveverticaloffset = 856
		self.graphwidth = 1020
		self.graphheight = 125
		self.graphblockheight = 5

# =========================================================================================

	def addhistoryentry(self, monitordata, networkstatus, temperature):

		currentdatetime = DateTime.getnow()
		newhistoryitem = HistoryItem.createhistoryitem(currentdatetime, monitordata, networkstatus, temperature)
		self.monitorhistory.append(newhistoryitem)
		self.clearuphistory(currentdatetime)
		return newhistoryitem.getsavedata()



	def restorehistory(self, saveddatalist):

		for dataitem in saveddatalist:
			self.monitorhistory.append(HistoryItem.createfromfile(dataitem))



	def gethistorygraphics(self):

		origintimedate = DateTime.getnow()
		longorigintimedate = DateTime.createfromobject(origintimedate)
		origintimedate.adjusthours(-42)
		longorigintimedate.adjustdays(-10)
		longorigintimedate.adjusthours(-12)

		outcome = {"brightred": [], "red": [], "orange": [], "amber": [], "yellow": [], "green": [], "blue": [],
																"axeslines": [], "biglabels": [], "littlelabels": []}

		for graphtop in [self.graphupperverticaloffset, self.graphlowerverticaloffset]:
			outcome = Functions.getgraphaxes(origintimedate, self.erasize, self.graphcolumnwidth,
													self.graphhorizontaloffset, graphtop, self.graphwidth,
													self.graphheight, outcome)

		for graphtop in [self.graphthreeverticaloffset, self.graphfourverticaloffset, self.graphfiveverticaloffset]:
			outcome = Functions.getgraphaxes(longorigintimedate, self.longerasize, self.graphcolumnwidth,
													self.graphhorizontaloffset, graphtop, self.graphwidth,
													self.graphheight, outcome)

		outcome = Functions.getgraphblocks(origintimedate, self.erasize, self.graphcolumnwidth,
											self.graphhorizontaloffset, self.graphupperverticaloffset,
											self.graphlowerverticaloffset, self.graphheight,
											self.monitorhistory, self.graphblockheight, outcome)

		outcome = Functions.getlonggraphblocks(longorigintimedate, self.longerasize, self.graphcolumnwidth,
											self.graphhorizontaloffset, self.graphthreeverticaloffset,
											self.graphfourverticaloffset, self.graphheight,
											self.getlonghistory(), outcome)

		outcome = Functions.gettempgraphblocks(longorigintimedate, self.longerasize, self.graphcolumnwidth,
											self.graphhorizontaloffset, self.graphfiveverticaloffset,
											self.graphheight, self.getlonghistory(), outcome)

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
				currentlonghistoryitem.cumulate(historyitem)
		if EraFunctions.compareeras(currentlonghistoryitem.getdatetime(), DateTime.getnow(), 5) == False:
			outcome.append(currentlonghistoryitem)
		return outcome



