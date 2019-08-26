from .operatoraction_subcomponent import operatoraction_module as OperatorAction
from ...common_components.datetime_datatypes import datetime_module as DateTime




class DefineOperatorTracker:

	def __init__(self):

		self.operatoractions = {}

		self.queuenewrefreshaction()

		self.nullaction = "Null"

# =========================================================================================

	def queuenewaddtorrentaction(self, newurl):
		self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction("Add", newurl)
		self.cleanrefreshactionsout()

	def queuenewpausetorrentaction(self, torrentid):
		self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction("Stop", torrentid)
		self.cleanrefreshactionsout()

	def queuenewpauseallaction(self):
		self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction("Stop", "ALL")
		self.cleanrefreshactionsout()

	def queuenewresumetorrentaction(self, torrentid):
		self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction("Start", torrentid)
		self.cleanrefreshactionsout()

	def queuenewresumeallaction(self):
		self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction("Start", "ALL")
		self.cleanrefreshactionsout()

	def queuenewdeletetorrentaction(self, torrentid):
		self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction("Delete", torrentid)
		self.cleanrefreshactionsout()

	def queuenewrefreshaction(self):
		self.operatoractions[self.generateindex()] = OperatorAction.createaoperatoraction("Refresh", "None")


	def cleanrefreshactionsout(self):
		for actionindex in self.operatoractions.keys():
			if self.operatoractions[actionindex].isrefresh() == True:
				del self.operatoractions[actionindex]

# =========================================================================================

	def getnextoperatoraction(self):

		nextactionid = self.findnextqueuedaction()

		if nextactionid != self.nullaction:
			outcome = self.operatoractions[nextactionid].getinstruction()
			del self.operatoractions[nextactionid]
		else:
			outcome = {'action': self.nullaction, 'context': "Null"}

		print(outcome)
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




