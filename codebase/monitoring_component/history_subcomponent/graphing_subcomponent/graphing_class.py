from ....common_components.datetime_datatypes import datetime_module as DateTime
from .drawing_framework import drawing_module as Compose
from .graph_subcomponent import graph_module as Graph

class DefineGraphing:

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

		graphset = {1: Graph.creategraph(), 2: Graph.creategraph(), 3: Graph.creategraph(),
								4: Graph.creategraph(), 5: Graph.creategraph()}

		# Axes
		for graphindex in [1, 2, 3, 4, 5]:
			graphset[graphindex].mergein(Compose.graphaxes(
														self.determineorigintimedate(currentdatetime, graphindex),
														self.determinecorrecterasize(graphindex),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphwidth,
														self.graphheight))

		# Upload & VPN Bars for top two graphs
		for graphindex in [1, 3]:
			historytype = self.determinehistorytype(shorthistory, longhistory, graphindex)
			graphset[graphindex].mergein(Compose.vpnbars(
														self.determineorigintimedate(currentdatetime, graphindex),
														self.determinecorrecterasize(graphindex),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historytype))
												
			graphset[graphindex + 1].mergein(Compose.uploadedbars(
														self.determineorigintimedate(currentdatetime, graphindex + 1),
														self.determinecorrecterasize(graphindex + 1),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historytype))

		# Status blocks for top graph
		graphset[1].mergein(Compose.statusblocks(		self.determineorigintimedate(currentdatetime, 1),
														self.determinecorrecterasize(1),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.determinehistorytype(shorthistory, longhistory, 1),
														self.graphblockheight))

		# Status bars for third graph
		graphset[3].mergein(Compose.statusbars(			self.determineorigintimedate(currentdatetime, 3),
														self.determinecorrecterasize(3),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														self.determinehistorytype(shorthistory, longhistory, 3)))

		# Temp bars for bottom graph
		graphset[5].mergein(Compose.tempbars(			self.determineorigintimedate(currentdatetime, 5),
														self.determinecorrecterasize(5),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														self.determinehistorytype(shorthistory, longhistory, 5)))

		# Graph headings
#		graph = Compose.titles(				self.graphhorizontaloffset,
#												self.graphverticaloffset,
#												self.graphverticalspacing,
#												graph)

		graphoutput = {1: graphset[1].get(), 2: graphset[2].get(), 3: graphset[3].get(),
																			4: graphset[4].get(), 5: graphset[5].get()}
		return graphoutput


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

