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
																	newaction['torrentid'], newaction['torrentname'])

# =========================================================================================

	def queuefolderrefresh(self):

		self.copyactions[self.refreshfolders] = CopyAction.createblankcopyaction()

# =========================================================================================

	def startnextaction(self):

		nextactionid = self.findnextqueuedaction()

		Logging.printout(self.getactiondescription(nextactionid))

		outcome = {'copyid': nextactionid, 'overwrite': False}

		if nextactionid != self.noaction:
			self.copyactions[nextactionid].updatestatus("In Progress")
			outcome.update(self.copyactions[nextactionid].getinstruction())
		else:
			outcome.update({'source': "", 'target': ""})

		return outcome

# =========================================================================================

	def updatecopyaction(self, copyid, newstatus):

		Logging.printout(self.getresultdescription(copyid, newstatus))

		refreshdata = False
		if copyid == self.noaction:
			refreshdata = False
		elif copyid == self.refreshfolders:
			self.copyactions[copyid].updatestatus(newstatus)
			refreshdata = True
		else:
			if copyid in self.copyactions.keys():
				self.copyactions[copyid].updatestatus(newstatus)
			else:
				Logging.printrawline("Cannot find copy action to update: " + copyid)

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
			if self.copyactions[actionid].getstatus == "Queued":
				queuetest = False

		return queuetest


	def findnextqueuedaction(self):

		inprogressflag = False
		nextactionid = self.noaction

		for actionid in self.copyactions.keys():
			if self.copyactions[actionid].getstatus() == "In Progress":
				inprogressflag = True
			elif self.copyactions[actionid].getstatus() == "Queued":
				if nextactionid == self.noaction:
					nextactionid = actionid

		if inprogressflag == True:
			nextactionid = self.noaction
			Logging.printrawline("Looking for a new item in queue, but there is already an In Progress item")

		return nextactionid



	def getactiondescription(self, copyid):

		if copyid == self.noaction:
			outcome = "No Requests in queue"

		elif copyid == self.refreshfolders:
			outcome = "Request to scrape TV Show folders"

		else:
			outcome = "Request " + copyid + " to Copy File:</br>"
			action = self.copyactions[copyid]
			outcome = outcome + action.getdescription()

		return outcome


	def getresultdescription(self, copyid, result):

		if copyid == self.noaction:
			outcome = "Empty Request Queue Processed"

		elif copyid == self.refreshfolders:
			outcome = "Scraped TV Show folders - " + result

		else:
			outcome = "Request " + copyid + " to Copy File - " + result

		return outcome


	def getcopierpagedata(self, torrentidlist):

		outcome = []
		for actionid in self.copyactions.keys():
			if actionid != self.refreshfolders:
				datetime = actionid[:4] + "-" + actionid[4:6] + "-" + actionid[6:8] + " "
				datetime = datetime + actionid[8:10] + ":" + actionid[10:12] + ":" + actionid[12:14]
				datetime = datetime + " [" + actionid[14:] + "]"
				newitem = {'copyid': actionid, 'datetimestamp': datetime}
				newitem.update(self.copyactions[actionid].getactioncopierpagedata())
				if newitem['torrentid'] in torrentidlist:
					newitem['stillavailable'] = "Yes"
				else:
					newitem['stillavailable'] = "No"
				outcome.append(newitem)

		return outcome



	def getcopierpageupdatedata(self):

		outcome = []
		for actionid in self.copyactions.keys():
			if actionid != self.refreshfolders:
				if self.copyactions[actionid].getcachestate() == True:
					newitem = {'copyid': actionid}
					newitem.update(self.copyactions[actionid].getactioncopierpageupdatedata())
					outcome.append(newitem)

		return outcome



	def gettorrentcopystate(self, torrentid):

		outcome = "Nothing"
		for actionid in self.copyactions.keys():
			if self.copyactions[actionid] == torrentid:
				copystatus = self.copyactions[actionid].getstatus()
				if (copystatus == "Queued") or (copystatus == "In Progress"):
					if outcome == "Nothing":
						outcome = "Incomplete"
				elif (copystatus == "Confirm") or (copystatus == "Failed"):
					outcome = "Attention"
				elif copystatus == "Succeeded":
					if outcome == "Nothing":
						outcome = "Completed"
		return outcome


