from ...common_components.filesystem_framework import filesystem_module as FileSystem
from .copieraction_subcomponent import copieraction_module as CopierAction
from ...common_components.datetime_datatypes import datetime_module as DateTime
from ...common_components.logging_framework import logging_module as Logging
from .copyset_subcomponent import copyset_module as CopySet
from . import copiertracker_privatefunctions as PrivateFunctions



class DefineCopierTracker:

	def __init__(self):

		self.copieractions = {}

		self.nullaction = "00000000000000000"

		self.queuefolderrefresh()

# =========================================================================================

	def queuenewfilecopyactions(self, newcopyactions):

		if newcopyactions == []:
			print("No copy actions to add to the queue this time")
		else:

			for newaction in newcopyactions:
				copysource = FileSystem.createpathfromlist(newaction['source'])
				copytarget = FileSystem.createpathfromlist(newaction['target'])
				self.copieractions[self.generateindex()] = CopierAction.createcopyaction(copysource, copytarget,
																	newaction['torrentid'], newaction['torrentname'])

# =========================================================================================

	def queuefolderrefresh(self):

		self.copieractions[self.generateindex()] = CopierAction.createscrapeaction()

# =========================================================================================

	def startnextcopieraction(self):

		nextactionid = self.findnextqueuedaction()

		if nextactionid == self.nullaction:
			Logging.printout("Null Request to Copier")
		else:
			Logging.printout(PrivateFunctions.getcopieractiondescription(nextactionid, self.copieractions[nextactionid]))

		if nextactionid != self.nullaction:
			self.copieractions[nextactionid].updatestatusandresultdetail("In Progress", "")
			outcome = self.copieractions[nextactionid].getcopieractioninstruction(nextactionid)
		else:
			outcome = {'copyid': self.nullaction, 'action': "Null"}

		return outcome

# =========================================================================================

	def updatecopieractionwithresult(self, copyid, newstatus, newresultdetail):

		if copyid == self.nullaction:
			Logging.printout("Null Request returned from copier")
		else:
			Logging.printout("Request " + copyid + " returned from copier with result <" + newstatus + ">")

		if copyid != self.nullaction:
			if copyid in self.copieractions.keys():
				self.copieractions[copyid].updatestatusandresultdetail(newstatus, newresultdetail)
			else:
				Logging.printrawline("Cannot find copy action to update: " + copyid)

# =========================================================================================

	def intervene(self, copyid, intervention):

		if copyid in self.copieractions.keys():
			self.copieractions[copyid].intervention(intervention)
		else:
			Logging.printrawline("Cannot find copy action to intervene with: " + copyid)

# =========================================================================================

	def shouldrefreshtvshowdata(self, copyid):

		outcome = False
		if copyid in self.copieractions.keys():
			if self.copieractions[copyid].isvalidscrapedata() == True:
				outcome = True
		return outcome

	# =========================================================================================

	def generateindex(self):

		currentdatetime = DateTime.getnow()
		indexstring = "0000" + str(len(self.copieractions) % 1000)
		outcome = currentdatetime.getiso() + indexstring[-3:]

		return outcome



	def isqueuealldone(self):

		queuetest = True
		for actionid in self.copieractions.keys():
			if self.copieractions[actionid].getstatus == "Queued":
				queuetest = False

		return queuetest


	def findnextqueuedaction(self):

		inprogressflag = False
		nextactionid = self.nullaction

		sortedlist = sorted(self.copieractions.keys())

		for actionid in sortedlist:
			if self.copieractions[actionid].getstatus() == "In Progress":
				inprogressflag = True
			elif self.copieractions[actionid].getstatus() == "Queued":
				if nextactionid == self.nullaction:
					nextactionid = actionid

		if inprogressflag == True:
			nextactionid = self.nullaction
			Logging.printrawline("Looking for a new item in queue, but there is already an In Progress item")

		return nextactionid



	def getcopierpageinitialdata(self, torrentidlist):

		keylist = []
		for actionid in self.copieractions.keys():
			keylist.append(actionid)

		keylist.sort(reverse=True)

		outcome = []
		for actionid in keylist:
			if self.copieractions[actionid].getstatus() != "Abandoned":
				outcome.append(self.copieractions[actionid].getcopierpageloaddata(torrentidlist, actionid))

		return outcome



	def getcopierpagerefreshdata(self):

		outcome = []
		for actionid in self.copieractions.keys():
			if self.copieractions[actionid].getcachestate() == True:
				outcome.append(self.copieractions[actionid].getcopierpageupdatedata(actionid))

		return outcome



	def getcopysetstate(self, torrentid):

		if torrentid == "ALL":
			tracker = CopySet.createglobalactiontracker()
		elif torrentid == "FOLDER REFRESH":
			tracker = CopySet.createrefreshtracker()
		else:
			tracker = CopySet.createtorrentcopytracker(torrentid)

		for actionid in self.copieractions.keys():
			tracker.updatestatus(self.copieractions[actionid])

		return tracker.getstatus()


	def getcopyactionoutcomedetail(self, copyid):

		copyaction = self.copieractions[copyid]

		return copyaction.getcopieractiondetail()



