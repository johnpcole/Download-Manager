from .operatoraction_subcomponent import operatoraction_module as OperatorAction
from ...common_components.datetime_datatypes import datetime_module as DateTime




class DefineOperatorTracker:

	def __init__(self):

		self.operatoractions = {}

		self.nullaction = "Null"

		self.actioncounter = 0

		self.queuenewrefreshaction()


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

		self.queuenewrefreshaction()

# =========================================================================================

	def getnextoperatoraction(self):

		nextactionid = self.findnextqueuedaction()

		if nextactionid != self.nullaction:
			outcome = self.operatoractions[nextactionid].getinstruction(nextactionid)
			del self.operatoractions[nextactionid]
		else:
			outcome = {'index': '-----------------', 'action': self.nullaction, 'context': "Null"}

		print("=================================================================")
		print("=================================================================")
		print("Next action for operator:", outcome)
		print("=================================================================")
		print("=================================================================")
		return outcome

# =========================================================================================


	def generateindex(self):

		currentdatetime = DateTime.getnow()
		self.actioncounter = self.actioncounter + 1
		if self.actioncounter > 999:
			self.actioncounter = 0
		indexstring = "0000" + str(self.actioncounter)
		outcome = currentdatetime.getiso() + indexstring[-3:]

		return outcome

# =========================================================================================

	def findnextqueuedaction(self):

		outcome = self.nullaction

		if len(self.operatoractions) > 0:

			actionids = []
			print("=============================================================================")
			print("=============================================================================")
			for actionid in self.operatoractions.keys():
				temp = self.operatoractions[actionid]
				print("Queued action: ", temp.getinstruction(actionid))
				actionids.append(actionid)

			actionids.sort()

			print("=============================================================================")
			outcome = actionids[0]
			print("Selected instruction:", outcome)
			print("=============================================================================")
			print("=============================================================================")

		else:
			print("=============================================================================")
			print("=============================================================================")
			print("No Queued Actions Left to find next")
			print("=============================================================================")
			print("=============================================================================")

		return outcome




	def queueaction(self, action, context):

		duplicatefound = False
		for existingactionid in self.operatoractions.keys():
			existingaction = self.operatoractions[existingactionid]
			if existingaction.isduplicate(action, context) == True:
				duplicatefound = True

		if duplicatefound == False:
			newindex = self.generateindex()
			print("=============================================================================")
			print("=============================================================================")
			print("Adding unique operator action: ", newindex, action, context)
			print("=============================================================================")
			print("=============================================================================")
			self.operatoractions[newindex] = OperatorAction.createaoperatoraction(action, context)
		else:
			print("=============================================================================")
			print("=============================================================================")
			print("Ignoring duplicate operator action: ", action, context)
			print("=============================================================================")
			print("=============================================================================")



