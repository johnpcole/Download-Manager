from ....common_components.datetime_datatypes import datetime_module as DateTime
from .drawing_framework import drawing_module as Compose
from .graphset_subcomponent import graphset_module as GraphSet

class DefineGraphing:

	def __init__(self, smallera, largeera):


		# Defines the granularity of display of monitor data
		self.shorterasize = smallera
		self.longerasize = largeera

		# Screen metrics
		self.graphcolumnwidth = 3
		self.graphhorizontaloffset = 9
		self.graphverticaloffset = -28
		self.graphverticalspacing = 177
		self.graphwidth = 1020
		self.graphheight = 125
		self.graphblockheight = 5

		self.shortoriginoffset = 42             # Hours from origin to now
		self.longoriginoffset = 12 + (10 * 24)  # Hours from origin to now

# =========================================================================================

	def getgraph(self, shorthistory, longhistory):

		currentdatetime = DateTime.getnow()

		graphset = GraphSet.creategraphset(5)

		# Axes
		for graphindex in [1, 2, 3, 4, 5]:
			graphset.addto(graphindex, Compose.graphaxes(
														self.determineorigintimedate(currentdatetime, graphindex),
														self.determinecorrecterasize(graphindex),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphwidth,
														self.graphheight))

		# Graph Headings
			graphset.addto(graphindex, Compose.titles(	self.graphhorizontaloffset,
														self.graphverticaloffset,
														self.graphverticalspacing,
														graphindex))


		# Upload & VPN Bars for top two graphs
		for graphindex in [1, 3]:
			historytype = self.determinehistorytype(shorthistory, longhistory, graphindex)
			graphset.addto(graphindex, Compose.vpnbars(	self.determineorigintimedate(currentdatetime, graphindex),
														self.determinecorrecterasize(graphindex),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historytype))
												
			graphset.addto(graphindex + 1, Compose.uploadedbars(
														self.determineorigintimedate(currentdatetime, graphindex + 1),
														self.determinecorrecterasize(graphindex + 1),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historytype))

		# Status blocks for top graph
		graphset.addto(1, Compose.statusblocks(			self.determineorigintimedate(currentdatetime, 1),
														self.determinecorrecterasize(1),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.determinehistorytype(shorthistory, longhistory, 1),
														self.graphblockheight))

		# Status bars for third graph
		graphset.addto(3, Compose.statusbars(			self.determineorigintimedate(currentdatetime, 3),
														self.determinecorrecterasize(3),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														self.determinehistorytype(shorthistory, longhistory, 3)))

		# Temp bars for bottom graph
		graphset.addto(5, Compose.tempbars(				self.determineorigintimedate(currentdatetime, 5),
														self.determinecorrecterasize(5),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														self.determinehistorytype(shorthistory, longhistory, 5)))

		return graphset.get()


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

