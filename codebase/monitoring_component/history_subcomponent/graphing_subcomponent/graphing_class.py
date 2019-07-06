from ....common_components.datetime_datatypes import datetime_module as DateTime
from .graph_subcomponent import graph_module as Graph

class DefineGraphing:

	def __init__(self, smallera, largeera):

		# Define graphset  size
		self.graphsetsize = 5

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

	def drawgraphs(self, shorthistory, longhistory):

		currentdatetime = DateTime.getnow()
		graphset = Graph.creategraphset(self.graphsetsize)

		for graphindex in [1, 2, 3, 4, 5]:
		# Axes
			graphset.addto(graphindex, Graph.creategraphaxes(
														self.determineorigintimedate(currentdatetime, graphindex),
														self.determinecorrecterasize(graphindex),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphwidth,
														self.graphheight))

		# Graph Headings
			graphset.addto(graphindex, Graph.createtitles(
														self.graphhorizontaloffset,
														self.graphverticaloffset,
														self.graphverticalspacing,
														graphindex))


		for graphindex in [1, 3]:
			historytype = self.determinehistorytype(shorthistory, longhistory, graphindex)
		# VPN Bars for graphs 1 & 3
			graphset.addto(graphindex, Graph.createvpnbars(
														self.determineorigintimedate(currentdatetime, graphindex),
														self.determinecorrecterasize(graphindex),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historytype))

		# Upload Bars for graphs 2 & 4
			graphset.addto(graphindex + 1, Graph.createuploadedbars(
														self.determineorigintimedate(currentdatetime, graphindex + 1),
														self.determinecorrecterasize(graphindex + 1),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historytype))

		# Legends
			graphset.addto(graphindex, Graph.createstatuslegend(
														self.graphhorizontaloffset,
														self.determinegraphbottom(1)))


		# Status blocks for top graph
		graphset.addto(1, Graph.createstatusblocks(		self.determineorigintimedate(currentdatetime, 1),
														self.determinecorrecterasize(1),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.determinehistorytype(shorthistory, longhistory, 1),
														self.graphblockheight))

		# Status bars for third graph
		graphset.addto(3, Graph.createstatusbars(		self.determineorigintimedate(currentdatetime, 3),
														self.determinecorrecterasize(3),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														self.determinehistorytype(shorthistory, longhistory, 3)))

		# Temp bars for fifth graph
		graphset.addto(5, Graph.createtempbars(			self.determineorigintimedate(currentdatetime, 5),
														self.determinecorrecterasize(5),
														self.graphcolumnwidth,
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														self.determinehistorytype(shorthistory, longhistory, 5)))

		return graphset.printout()


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

