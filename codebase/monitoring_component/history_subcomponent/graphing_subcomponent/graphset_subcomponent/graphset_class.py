from ..graph_subcomponent import graph_module as Graph



class DefineGraphSet:

	def __init__(self, size):

		self.size = size

		self.graphset = {}

		for i in range(1, self.size + 1):
			self.graphset[i] = Graph.creategraph()

# =========================================================================================

	def addto(self, setnum, newgraphobject):

		self.graphset[setnum].mergein(newgraphobject)

# =========================================================================================

	def get(self):

		graphoutput = {}
		for i in range(1, self.size + 1):
			graphoutput[i] = self.graphset[i].get()

		return graphoutput

