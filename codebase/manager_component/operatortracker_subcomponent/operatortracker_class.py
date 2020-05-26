#from .operatoraction_subcomponent import operatoraction_module as OperatorAction
#from ...common_components.datetime_datatypes import datetime_module as DateTime
#from ...common_components.logging_framework import logging_module as Logging
from ...common_components.queue_framework import queue_module as Queue



class DefineOperatorTracker:

	def __init__(self):

		self.actionsqueue = Queue.createqueue("./data/operator_queue", "Queuer")


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



	def queueaction(self, action, context):

		newactions = []
		newactions.append({'recordtype': 'queuedaction', 'actiontype': action, 'context': context})
		self.actionsqueue.createqueueditem(newactions)


