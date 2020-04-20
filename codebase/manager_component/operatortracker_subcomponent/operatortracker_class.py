#from .operatoraction_subcomponent import operatoraction_module as OperatorAction
from ...common_components.datetime_datatypes import datetime_module as DateTime
#from ...common_components.logging_framework import logging_module as Logging
from ... import database_definitions as Database



class DefineOperatorTracker:

	def __init__(self):

		self.actionsqueue = Database.createoperatoractionsdatabase()

		self.actionresults = Database.createoperatorresultsdatabase()

		self.outstandingactions = []

		#self.operatoractions = {}

		#self.nullaction = "Null"

		#self.actioncounter = 0

		#self.queuenewrefreshaction()

		self.lastseen = DateTime.getnow()


# =========================================================================================

	def refreshoutstandingactions(self):

		outstandingactions = []
		actiondata = self.actionsqueue.extractdatabaserows([{'recordtype': 'queuedaction'}])
		resultdata = self.actionresults.extractdatabaserows([{'recordtype': 'processedaction'}])

		for action in actiondata:
			matchfound = False
			for result in resultdata:
				if result['actionid'] == action['actionid']:
					matchfound = True
			if matchfound is False:
				outstandingactions.append(action)

		self.outstandingactions = outstandingactions



# =========================================================================================

	def queuenewaddtorrentaction(self, newurl):
		self.queueaction("Add", newurl)

	def queuenewpausetorrentaction(self, torrentid):
		self.queueaction("Stop", torrentid)

	def queuenewpauseallaction(self):
		self.queueaction("Stop", "ALL")

	def queuenewresumetorrentaction(self, torrentid):
		self.queueaction("Start", torrentid)

	def queuenewresumeallaction(self):
		self.queueaction("Start", "ALL")

	def queuenewdeletetorrentaction(self, torrentid):
		self.queueaction("Delete", torrentid)

	#def queuenewrefreshaction(self):
	#	self.queueaction("Refresh", "None")



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



	def queueaction(self, action, context):

		self.refreshoutstandingactions()

		duplicatefound = False
		for existingaction in self.outstandingactions:
			if (existingaction['actiontype'] == action) and (existingaction['context'] == context):
				duplicatefound = True

		if duplicatefound == False:
			newactions = []
			newactions.append({'actionid': self.generateindex(), 'actiontype': action, 'context': context})

			self.actionsqueue.insertdatabaserows(newactions)



	# def lognewdatashare(self):
	#
	# 	self.lastseen.settonow()
	#
	#
	#
	# def hasrecentlybeenseen(self):
	#
	# 	timedifference = DateTime.timedifferenceasduration(self.lastseen, DateTime.getnow())
	# 	if abs(timedifference.getsecondsvalue()) > 10:
	# 		outcome = False
	# 	else:
	# 		outcome = True
	#
	# 	return outcome




