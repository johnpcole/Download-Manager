from .....common_components.datetime_datatypes import datetime_module as DateTime
from .graph_subcomponent import graph_module as Graph

class DefineGraphing:

	def __init__(self, smallera, largeera):

		# Define graphset size
		self.graphsetsize = 6

		# Defines the granularity of display of monitor data
		self.shorterasize = smallera
		self.longerasize = largeera

		# Screen metrics
		self.widegraphcolumnwidth = 3
		self.narrowgraphcolumnwidth = 2
		self.graphhorizontaloffset = 9
		self.graphverticaloffset = -28
		self.graphverticalspacing = 177
		self.widegraphwidth = 974 - 4
		self.narrowgraphwidth = 480 - 4
		self.graphheight = 125
		self.graphblockheight = 5

		self.wideshortoriginoffset = 42               # Hours from origin to now
		self.widelongoriginoffset = 12 + (10 * 24)    # Hours from origin to now
		self.narrowshortoriginoffset = 42             # Hours from origin to now
		self.narrowlongoriginoffset = 12 + (10 * 24)  # Hours from origin to now

	# =========================================================================================

	def drawgraphs(self, longhistorymode, historydataset):

		currentdatetime = DateTime.getnow()
		graphset = Graph.creategraphset(self.graphsetsize)

		for graphindex in [1, 2, 3, 4, 5, 6]:
		# Axes
			graphset.addto(graphindex, Graph.creategraphaxes(
										self.determineorigintimedate(currentdatetime, graphindex, longhistorymode),
														self.determinecorrecterasize(longhistorymode),
														self.determinecolumnwidth(graphindex),
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.determinegraphwidth(graphindex),
														self.graphheight))

		# Graph Headings
			graphset.addto(graphindex, Graph.createtitles(
														longhistorymode,
														self.graphhorizontaloffset,
														self.graphverticaloffset,
														self.graphverticalspacing,
														graphindex))


		for graphindex in [1, 4]:
		# VPN Bars for graphs 1 & 4
			graphset.addto(graphindex, Graph.createvpnbars(
										self.determineorigintimedate(currentdatetime, graphindex, longhistorymode),
														self.determinecorrecterasize(longhistorymode),
														self.determinecolumnwidth(graphindex),
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historydataset))

		# Upload Bars for graphs 2 & 5
			graphset.addto(graphindex + 1, Graph.createuploadedbars(
										self.determineorigintimedate(currentdatetime, graphindex + 1, longhistorymode),
														self.determinecorrecterasize(longhistorymode),
														self.determinecolumnwidth(graphindex + 1),
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historydataset))

		# Legends
			graphset.addto(graphindex, Graph.createstatuslegend(
														self.graphhorizontaloffset,
														self.determinegraphbottom(1)))

			if longhistorymode == True:
		# Status bars for graphs 1 & 4
				graphset.addto(graphindex, Graph.createstatusbars(
										self.determineorigintimedate(currentdatetime, graphindex, longhistorymode),
														self.determinecorrecterasize(longhistorymode),
														self.determinecolumnwidth(graphindex),
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historydataset))
			else:
		# Status blocks for graphs 1 & 4
				graphset.addto(graphindex, Graph.createstatusblocks(
										self.determineorigintimedate(currentdatetime, graphindex, longhistorymode),
														self.determinecorrecterasize(longhistorymode),
														self.determinecolumnwidth(graphindex),
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														historydataset,
														self.graphblockheight))


		# Temp bars for graphs 3 & 6
			graphset.addto(graphindex + 2, Graph.createtempbars(
										self.determineorigintimedate(currentdatetime, graphindex + 2, longhistorymode),
														self.determinecorrecterasize(longhistorymode),
														self.determinecolumnwidth(graphindex + 2),
														self.graphhorizontaloffset,
														self.determinegraphbottom(1),
														self.graphheight,
														historydataset))

		return graphset.printout()


	def determinegraphbottom(self, graphindex):

		return self.graphverticaloffset + (self.graphverticalspacing * graphindex)

	def determinecorrecterasize(self, longhistorymode):

		if longhistorymode == False:
			graph = self.shorterasize
		else:
			graph = self.longerasize

		return graph

	def determineorigintimedate(self, currenttimedate, graphindex, longhistorymode):

		graph = DateTime.createfromobject(currenttimedate)
		if graphindex > 3:
			if longhistorymode == True:
				graph.adjusthours(0 - self.narrowlongoriginoffset)
			else:
				graph.adjusthours(0 - self.narrowshortoriginoffset)
		else:
			if longhistorymode == True:
				graph.adjusthours(0 - self.widelongoriginoffset)
			else:
				graph.adjusthours(0 - self.wideshortoriginoffset)
		return graph

	def determinegraphwidth(self, index):

		if index < 4:
			outcome = self.widegraphwidth
		else:
			outcome = self.narrowgraphwidth
		return outcome

	def determinecolumnwidth(self, index):

		if index < 4:
			outcome = self.widegraphcolumnwidth
		else:
			outcome = self.narrowgraphcolumnwidth
		return outcome

