from ...common_components.filesystem_framework import filesystem_module as FileSystem
from .copieraction_subcomponent import copieraction_module as CopierAction
from ...common_components.logging_framework import logging_module as Logging
from .copyset_subcomponent import copyset_module as CopySet
from . import copiertracker_privatefunctions as PrivateFunctions
from ...common_components.queue_framework import queue_module as Queue



class DefineCopierTracker:

	def __init__(self, copierhistorylocation, copieractionqueuelocation, filesystemqueuelocation):

		self.copieractions = {}

		self.nullaction = "00000000000000000"

		self.latestcopierresult = "00000000_000000_000"

		self.historylocation = copierhistorylocation

		self.copieractionqueue = Queue.createqueuewriter(copieractionqueuelocation, 24)

		self.copierdatastream = Queue.createqueuereader(filesystemqueuelocation)

		self.queuefolderrefresh()


# =========================================================================================

	def queuenewfilecopyactions(self, newcopyactions):

		if newcopyactions == []:
			print("No copy actions to add to the queue this time")
		else:

			for newaction in newcopyactions:
				copysource = FileSystem.createpathfromlist(newaction['source'])
				copytarget = FileSystem.createpathfromlist(newaction['target'])
				newactionobject = CopierAction.createcopyaction(copysource, copytarget,
												newaction['torrentid'], newaction['torrentname'], self.historylocation)
				self.writetoqueue(newactionobject)


# =========================================================================================

	def queuefolderrefresh(self):

		newactionobject = CopierAction.createscrapeaction(self.historylocation)
		self.writetoqueue(newactionobject)


# =========================================================================================

	def writetoqueue(self, newactionobject):
		newid = newactionobject.getcopyid()
		self.copieractions[newid] = newactionobject
		newinstruction = newactionobject.getcopieractioninstruction()
		self.copieractionqueue.createqueueditem(newinstruction)


# =========================================================================================

	def getlatestcopierresults(self):

		nextresult = self.copierdatastream.readfromqueue
		if nextresult is not None:
			copyid = nextresult['copyid']
			newstatus = nextresult['outcome']
			Logging.printout("Request " + copyid + " returned from copier with result <" + newstatus + ">")
			if copyid in self.copieractions.keys():
				self.copieractions[copyid].updatestatusandresultdetail(newstatus, nextresult['notes'])
				self.latestcopierresult = copyid
			else:
				Logging.printrawline("Cannot find copy action to update: " + copyid)

# =========================================================================================

	def intervene(self, copyid, intervention):

		if copyid in self.copieractions.keys():
			self.copieractions[copyid].intervention(intervention)
			if self.copieractions[copyid].getstatus == "Queued":
				self.copieractionqueue.createqueueditem(self.copieractions[copyid].getcopieractioninstruction())
		else:
			Logging.printrawline("Cannot find copy action to intervene with: " + copyid)

# =========================================================================================

	def getrefreshedtvshowdata(self):

		outcome = None
		if self.copieractions[self.latestcopierresult].isvalidscrapedata() is True:
			outcome = self.copieractions[self.latestcopierresult].getactiondetail()
		return outcome

	# =========================================================================================


	# def isqueuealldone(self):
	#
	# 	queuetest = True
	# 	for actionid in self.copieractions.keys():
	# 		if self.copieractions[actionid].getstatus == "Queued":
	# 			queuetest = False
	#
	# 	return queuetest

	#
	# def findnextqueuedaction(self):
	#
	# 	inprogressflag = False
	# 	nextactionid = self.nullaction
	#
	# 	sortedlist = sorted(self.copieractions.keys())
	#
	# 	for actionid in sortedlist:
	# 		if self.copieractions[actionid].getstatus() == "In Progress":
	# 			inprogressflag = True
	# 		elif self.copieractions[actionid].getstatus() == "Queued":
	# 			if nextactionid == self.nullaction:
	# 				nextactionid = actionid
	#
	# 	if inprogressflag == True:
	# 		nextactionid = self.nullaction
	# 		Logging.printrawline("Looking for a new item in queue, but there is already an In Progress item")
	#
	# 	return nextactionid



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

		#print("==============================================")
		for actionid in self.copieractions.keys():
			tracker.updatestatus(self.copieractions[actionid])
		#print("==============================================")

		return tracker.getstatus()


	def getcopyactionoutcomedetail(self, copyid):

		copyaction = self.copieractions[copyid]

		return copyaction.getcopieractiondetail()



