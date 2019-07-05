from ....common_components.datetime_datatypes import datetime_module as DateTime
from .drawing_framework import drawing_module as Compose



class DefineGraph:

	def __init__(self, smallera, largeera):


		# Defines the granularity of display of monitor data
		self.shorterasize = smallera
		self.longerasize = largeera

		# Screen metrics
		self.graphcolumnwidth = 3
		self.graphhorizontaloffset = 5
		self.graphverticaloffset = -29
		self.graphverticalspacing = 177
		#self.graphupperverticaloffset = 148
		#self.graphlowerverticaloffset = 325
		#self.graphthreeverticaloffset = 502
		#self.graphfourverticaloffset = 679
		#self.graphfiveverticaloffset = 856
		self.graphwidth = 1020
		self.graphheight = 125
		self.graphblockheight = 5

		self.shortoriginoffset = 42             # Hours from origin to now
		self.longoriginoffset = 12 + (10 * 24)  # Hours from origin to now

# =========================================================================================

	def gethistorygraphics(self, shorthistory, longhistory):

		currentdatetime = DateTime.getnow()

		outcome = {"brightred": [], "red": [], "orange": [], "amber": [], "yellow": [], "green": [], "blue": [],
												"tempa": [], "tempb": [], "tempc": [], "tempd": [], "tempe": [],
												"axeslines": [], "biglabels": [], "littlelabels": [], "graphtitles": []}

		# Axes
		for graphindex in [1, 2, 3, 4, 5]:
			outcome = Compose.graphaxes(		self.determineorigintimedate(currentdatetime, graphindex),
												self.determinecorrecterasize(graphindex),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(graphindex),
												self.graphwidth,
												self.graphheight,
												outcome)

		# Upload & VPN Bars for top two graphs
		for graphindex in [1, 3]:
			outcome = Compose.vpnbars(			self.determineorigintimedate(currentdatetime, graphindex),
												self.determinecorrecterasize(graphindex),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(graphindex),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, graphindex),
												outcome)
			outcome = Compose.uploadedbars(		self.determineorigintimedate(currentdatetime, graphindex + 1),
												self.determinecorrecterasize(graphindex + 1),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(graphindex + 1),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, graphindex + 1),
												outcome)


		# Status blocks for top graph
		outcome = Compose.statusblocks(			self.determineorigintimedate(currentdatetime, 1),
												self.determinecorrecterasize(1),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(1),
												self.determinehistorytype(shorthistory, longhistory, 1),
												self.graphblockheight,
												outcome)

		# Status bars for third graph
		outcome = Compose.statusbars(			self.determineorigintimedate(currentdatetime, 3),
												self.determinecorrecterasize(3),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(3),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, 3),
												outcome)

		# Temp bars for bottom graph
		outcome = Compose.tempbars(				self.determineorigintimedate(currentdatetime, 5),
												self.determinecorrecterasize(5),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(5),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, 5),
												outcome)

		# Graph headings
		outcome = Compose.titles(				self.graphhorizontaloffset,
												self.graphverticaloffset,
												self.graphverticalspacing,
												outcome)

		return outcome


	def determinegraphbottom(self, graphindex):

		return self.graphverticaloffset + (self.graphverticalspacing * graphindex)

	def determinecorrecterasize(self, graphindex):
	
		if graphindex < 3:
			outcome = self.shorterasize
		else:
			outcome = self.longerasize
		
		return outcome

	def determineorigintimedate(self, currenttimedate, graphindex):

		outcome = DateTime.createfromobject(currenttimedate)
		if graphindex < 3:
			outcome.adjusthours(0 - self.shortoriginoffset)
		else:
			outcome.adjusthours(0 - self.longoriginoffset)
		return outcome

	def determinehistorytype(self, shorthistory, longhistory, graphindex):

		if graphindex < 3:
			history = shorthistory
		else:
			history = longhistory
		return history





