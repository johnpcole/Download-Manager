from ...common_components.queue_framework import queue_module as Queue




class DefineOperatorTracker:

	def __init__(self):

		self.actionsqueue = Queue.createqueue("./data/operator_queue", "Queuer")

		self.delugedatastream = Queue.createqueue("./data/session_data", "Reader")

		self.latestdelugedata = {'torrents': {}, 'sessiondata': {}, 'lastpolled': "19991231235959"}

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




# =========================================================================================



	def updatedelugedata(self):

		latestdelugedata = self.delugedatastream.readqueuelatest()
		if latestdelugedata is not None:
			if 'torrents' in latestdelugedata.keys():
				if 'sessiondata' in latestdelugedata.keys():
					self.latestdelugedata = latestdelugedata.copy()

# =========================================================================================

	def getlatesttorrentdata(self):

		return self.latestdelugedata['torrents']

# =========================================================================================

	def getlatestsessiondata(self):

		return self.latestdelugedata['sessiondata']

