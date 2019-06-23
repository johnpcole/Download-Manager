from .historyitem_subcomponent import historyitem_module as HistoryItem
from ...common_components.datetime_datatypes import datetime_module as DateTime
from . import history_privatefunctions as Functions



class DefineHistory:

	def __init__(self):

		# An array of historic monitor history
		self.monitorhistory = []

		# Defines the granularity of display of monitor data
		self.erasize = 4 # Ten minute intervals

		# Screen metrics
		self.graphcolumnwidth = 3
		self.graphhorizontaloffset = 5
		self.graphupperverticaloffset = 123
		self.graphlowerverticaloffset = 123 + 160

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
		origintimedate.adjusthours(-42)
		outcome[""] = Functions.getgraphaxes(origintimedate, self.erasize, self.graphcolumnwidth, horizontaloffset, firstverticaloffset, secondverticaloffset):

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

		if currentdatetime.gettimevalue() < 600:
			print("Before clean up: ", len(self.monitorhistory))
			threshold = DateTime.createfromobject(currentdatetime)
			threshold.adjustdays(-5)
			newhistorylist = []
			for historyitem in self.monitorhistory:
				if DateTime.isfirstlaterthansecond(historyitem.getdatetime(), threshold) == True:
					newhistorylist.append(historyitem)

			self.monitorhistory = newhistorylist.copy()
			print("After clean up: ", len(self.monitorhistory))




