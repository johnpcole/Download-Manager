from .historyitem_subcomponent import historyitem_module as HistoryItem
from ....common_components.datetime_datatypes import datetime_module as DateTime
from ....common_components.datetime_datatypes import eras_module as EraFunctions
from .graphing_subcomponent import graphing_module as Graphing


class DefineHistory:

	def __init__(self):

		# An array of historic monitor history
		self.monitorhistory = []

		# Defines the granularity of display of monitor data
		self.erasize = 4        # Ten minute intervals
		self.longerasize = 5    # Hour intervals

		# Graphing module
		self.graphs = Graphing.creategraphing(self.erasize, self.longerasize)

# =========================================================================================

	def addhistoryentry(self, colourcounts, networkstatus, uploadedtotal, temperature):

		currentdatetime = DateTime.getnow()
		newhistoryitem = HistoryItem.createhistoryitem(currentdatetime, colourcounts, networkstatus, uploadedtotal,
																										temperature)
		self.monitorhistory.append(newhistoryitem)
		self.clearuphistory(currentdatetime)
		#print("NEW MONITOR HISTORY ITEM: ", newhistoryitem.getsavedata())
		return newhistoryitem.getsavedata()



	def restorehistory(self, saveddatalist):

		for dataitem in saveddatalist:
			self.monitorhistory.append(HistoryItem.createfromfile(dataitem))



	def gethistorygraphics(self, historyperiod):

		if historyperiod == "Latest":
			output = self.graphs.drawgraphs(False, self.monitorhistory)
		elif historyperiod == "Recent":
			output = self.graphs.drawgraphs(True, self.getlonghistory())
		else:
			output = self.graphs.drawdummygraphs()

		return output



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



