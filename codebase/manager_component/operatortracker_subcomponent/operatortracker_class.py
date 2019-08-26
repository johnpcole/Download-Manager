from .operatoraction_subcomponent import operatoraction_module as OperatorAction
from ...common_components.datetime_datatypes import datetime_module as DateTime




class DefineOperatorTracker:

	def __init__(self):

		self.operatoractions = {}

		self.queuenewrefreshaction()

		self.nullaction = "Null"

# =========================================================================================

	def queuenewaddtorrentaction(self, newurl):
		self.queueaction("Add", newurl)
		self.cleanrefreshactionsout()

	def queuenewpausetorrentaction(self, torrentid):
		self.queueaction("Stop", torrentid)
		self.cleanrefreshactionsout()

	def queuenewpauseallaction(self):
		self.queueaction("Stop", "ALL")
		self.cleanrefreshactionsout()

	def queuenewresumetorrentaction(self, torrentid):
		self.queueaction("Start", torrentid)
		self.cleanrefreshactionsout()

	def queuenewresumeallaction(self):
		self.queueaction("Start", "ALL")
		self.cleanrefreshactionsout()

	def queuenewdeletetorrentaction(self, torrentid):
		self.queueaction("Delete", torrentid)
		self.cleanrefreshactionsout()

	def queuenewrefreshaction(self):
		self.queueaction("Refresh", "None")


	def cleanrefreshactionsout(self):
		foundindexes = []
		for actionindex in self.operatoractions.keys():
			if self.operatoractions[actionindex].isrefresh() == True:
				foundindexes.append(actionindex)
		if len(foundindexes) > 0:
			for actionindex in foundindexes:
				del self.operatoractions[actionindex]


# =========================================================================================

	def getnextoperatoraction(self):

		nextactionid = self.findnextqueuedaction()

		if nextactionid != self.nullaction:
			outcome = self.operatoractions[nextactionid].getinstruction()
			del self.operatoractions[nextactionid]
		else:
			outcome = {'action': self.nullaction, 'context': "Null"}

		print("Number of operations left: ",len(self.operatoractions), " This operation: ", outcome)
		return outcome

# =========================================================================================


	def generateindex(self):

		currentdatetime = DateTime.getnow()
		indexstring = "0000" + str(len(self.operatoractions) % 1000)
		outcome = currentdatetime.getiso() + indexstring[-3:]

		return outcome

# =========================================================================================

	def findnextqueuedaction(self):

		outcome = self.nullaction

		if len(self.operatoractions) > 0:

			actionids = []
			for actionid in self.operatoractions.keys():
				actionids.append(actionid)

			actionids.sort()

			outcome = actionids[0]

		return outcome




	def queueaction(self, action, context):

		duplicatefound = False
		for actionid in self.operatoractions.keys():
			if self.operatoractions[actionid].isduplicate() == True:
				duplicatefound = True

		if duplicatefound == False:
			self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction(action, context)
		else:
			print("Ignoring duplicate operator action: ", action, context)



