from ....common_components.filesystem_framework import filesystem_module as FileSystem
from .copyaction_subcomponent import copyaction_module as CopyAction



class DefineCopyTracker:

	def __init__(self):

		self.copyactions = []

# =========================================================================================

	def queuenewactions(self, newcopyactions):

		if newcopyactions == []:
			print("No copy actions to add to the queue this time")
		else:

			for newaction in newcopyactions:
				copysource = FileSystem.createpathfromlist(newaction['source'])
				copytarget = FileSystem.createpathfromlist(newaction['target'])
				queuesize = len(self.copyactions) + 1
				self.copyactions.append(CopyAction.createcopyaction(copysource, copytarget, queuesize,
																								newaction['torrentid']))


# =========================================================================================

	def getnextaction(self):

		inprogressflag = False
		nextaction = None

		for action in self.copyactions:
			if action.confirmstatus("In Progress"):
				inprogressflag = True
			elif action.confirmstatus("Queued"):
				if nextaction is None:
					nextaction = action

		if inprogressflag == True:
			nextaction = None

		if nextaction is not None:
			nextaction.updatestatus("In Progress")

		return nextaction

# =========================================================================================

	def updateactionstatus(self, torrentid, newstatus):

		foundflag = False
		for action in self.copyactions:
			if action.getid() == torrentid:
				action.updatestatus(newstatus)
				foundflag = True

		return foundflag






























