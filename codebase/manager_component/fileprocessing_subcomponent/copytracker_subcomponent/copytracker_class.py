from ....common_components.filesystem_framework import filesystem_module as FileSystem
from .copyaction_subcomponent import copyaction_module as CopyAction
from ....common_components.datetime_datatypes import datetime_module as DateTime
from ....common_components.logging_framework import logging_module as Logging


class DefineCopyTracker:

	def __init__(self):

		self.copyactions = {}

		self.noaction = "00000000000000000"

		self.refreshfolders = "-----------------"

		self.copyactions[self.refreshfolders] = CopyAction.createblankcopyaction()

# =========================================================================================

	def queuenewactions(self, newcopyactions):

		if newcopyactions == []:
			print("No copy actions to add to the queue this time")
		else:

			for newaction in newcopyactions:
				copysource = FileSystem.createpathfromlist(newaction['source'])
				copytarget = FileSystem.createpathfromlist(newaction['target'])
				self.copyactions[self.generateindex()] = CopyAction.createcopyaction(copysource, copytarget,
																					newaction['torrentid'])

# =========================================================================================

	def queuefolderrefresh(self):

		self.copyactions[self.refreshfolders] = CopyAction.createblankcopyaction()

# =========================================================================================

	def startnextaction(self):

		inprogressflag = False
		nextactionid = self.noaction

		for actionid in self.copyactions.keys():
			if self.copyactions[actionid].confirmstatus("In Progress"):
				inprogressflag = True
			elif self.copyactions[actionid].confirmstatus("Queued"):
				if nextactionid == self.noaction:
					nextactionid = actionid

		if inprogressflag == True:
			nextactionid = self.noaction
			Logging.printout("Looking for a new item in queue, but there is already an In Progress item")

		if nextactionid != self.noaction:
			self.copyactions[nextactionid].updatestatus("In Progress")

		outcome = {'copyid': nextactionid, 'overwrite': False}
		outcome.update(self.copyactions[nextactionid].getinstruction())
		return outcome

# =========================================================================================

	def importcopieroutcome(self, copyid, newstatus):

		refreshdata = False
		if copyid == self.noaction:
			if self.isqueuealldone() == False:
				Logging.printout("Copier thinks is was finished, but there are more queued items")
		elif copyid == self.refreshfolders:
			self.copyactions[copyid].updatestatus(newstatus)
			refreshdata = True
		else:
			if copyid in self.copyactions.keys():
				self.copyactions[copyid].updatestatus(newstatus)
			else:
				Logging.printout("Cannot find copy action to update: " + copyid)

		return refreshdata

	# =========================================================================================

	def generateindex(self):

		currentdatetime = DateTime.getnow()
		indexstring = "0000" + str(len(self.copyactions) % 1000)
		outcome = currentdatetime.getiso() + indexstring[-3:]

		return outcome



	def isqueuealldone(self):

		queuetest = True
		for actionid in self.copyactions.keys():
			if self.copyactions[actionid].confirmstatus("Queued") == True:
				queuetest = False

		return queuetest



















