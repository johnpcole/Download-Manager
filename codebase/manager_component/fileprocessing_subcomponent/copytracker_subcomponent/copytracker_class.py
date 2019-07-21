from ....common_components.filesystem_framework import filesystem_module as FileSystem
from .copyaction_subcomponent import copyaction_module as CopyAction
from ....common_components.datetime_datatypes import datetime_module as DateTime
from ....common_components.logging_framework import logging_module as Logging


class DefineCopyTracker:

	def __init__(self):

		self.copyactions = {}

		self.copyactions["00000000000000000"] = CopyAction.createblankcopyaction()

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

	def startnextaction(self):

		inprogressflag = False
		nextactionid = "00000000000000000"

		for actionid in self.copyactions.keys():
			if self.copyactions[actionid].confirmstatus("In Progress"):
				inprogressflag = True
			elif self.copyactions[actionid].confirmstatus("Queued"):
				if nextactionid == "00000000000000000":
					nextactionid = actionid

		if inprogressflag == True:
			nextactionid = "00000000000000000"

		if nextactionid != "00000000000000000":
			self.copyactions[nextactionid].updatestatus("In Progress")

		outcome = {'copyid': nextactionid}
		outcome.update(self.copyactions[nextactionid].getinstruction())
		return outcome

# =========================================================================================

	def updateactionstatus(self, copyid, newstatus):

		foundflag = False
		if copyid in self.copyactions.keys():
			self.copyactions[copyid].updatestatus(newstatus)
			foundflag = True
		else:
			Logging.printout("Cannot find copy action to update: " + copyid)

		return foundflag

	# =========================================================================================

	def generateindex(self):

		currentdatetime = DateTime.getnow()
		indexstring = "0000" + str(len(self.copyactions) % 1000)
		outcome = currentdatetime.getiso() + indexstring[-3:]

		return outcome
























