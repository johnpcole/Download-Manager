from ....common_components.datetime_datatypes import datetime_module as DateTime
from .drawing_framework import drawing_module as Compose
from  ....common_components.webserver_framework  import webserver_module as Test


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
		self.graphwidth = 1020
		self.graphheight = 125
		self.graphblockheight = 5

		self.shortoriginoffset = 42             # Hours from origin to now
		self.longoriginoffset = 12 + (10 * 24)  # Hours from origin to now

# =========================================================================================

	def getgraph(self, shorthistory, longhistory):

		currentdatetime = DateTime.getnow()

		graph = self.startblankcanvass(5)

		# Axes
		for graphindex in [1, 2, 3, 4, 5]:
			graph[graphindex] = Compose.graphaxes(
												self.determineorigintimedate(currentdatetime, graphindex),
												self.determinecorrecterasize(graphindex),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(1),
												self.graphwidth,
												self.graphheight,
												graph[graphindex])

		# Upload & VPN Bars for top two graphs
		for graphindex in [1, 3]:
			graph[graphindex] = Compose.vpnbars(
												self.determineorigintimedate(currentdatetime, graphindex),
												self.determinecorrecterasize(graphindex),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(1),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, graphindex),
												graph[graphindex])
												
			graph[graphindex + 1] = Compose.uploadedbars(
												self.determineorigintimedate(currentdatetime, graphindex + 1),
												self.determinecorrecterasize(graphindex + 1),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(1),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, graphindex + 1),
												graph[graphindex + 1])

		# Status blocks for top graph
		graph[1] = Compose.statusblocks(		self.determineorigintimedate(currentdatetime, 1),
												self.determinecorrecterasize(1),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(1),
												self.determinehistorytype(shorthistory, longhistory, 1),
												self.graphblockheight,
												graph[1])

		# Status bars for third graph
		graph[3] = Compose.statusbars(		self.determineorigintimedate(currentdatetime, 3),
												self.determinecorrecterasize(3),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(1),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, 3),
												graph[3])

		# Temp bars for bottom graph
		graph[5] = Compose.tempbars(			self.determineorigintimedate(currentdatetime, 5),
												self.determinecorrecterasize(5),
												self.graphcolumnwidth,
												self.graphhorizontaloffset,
												self.determinegraphbottom(1),
												self.graphheight,
												self.determinehistorytype(shorthistory, longhistory, 5),
												graph[5])

		# Graph headings
		graph = Compose.titles(				self.graphhorizontaloffset,
												self.graphverticaloffset,
												self.graphverticalspacing,
												graph)

		return graph


	def determinegraphbottom(self, graphindex):

		return self.graphverticaloffset + (self.graphverticalspacing * graphindex)

	def determinecorrecterasize(self, graphindex):
	
		if graphindex < 3:
			graph = self.shorterasize
		else:
			graph = self.longerasize
		
		return graph

	def determineorigintimedate(self, currenttimedate, graphindex):

		graph = DateTime.createfromobject(currenttimedate)
		if graphindex < 3:
			graph.adjusthours(0 - self.shortoriginoffset)
		else:
			graph.adjusthours(0 - self.longoriginoffset)
		return graph

	def determinehistorytype(self, shorthistory, longhistory, graphindex):

		if graphindex < 3:
			history = shorthistory
		else:
			history = longhistory
		return history


	def startblankcanvass(self, setsize):

		newdictionaryset  = {}
		newdictionary = {"brightred": [], "red": [], "orange": [], "amber": [], "yellow": [], "green": [], "blue": [],
												"tempa": [], "tempb": [], "tempc": [], "tempd": [], "tempe": [],
												"axeslines": [], "biglabels": [], "littlelabels": [], "graphtitles": []}

		for x in range(1, setsize + 1):
			newdictionaryset[x] = newdictionary

		return newdictionaryset




