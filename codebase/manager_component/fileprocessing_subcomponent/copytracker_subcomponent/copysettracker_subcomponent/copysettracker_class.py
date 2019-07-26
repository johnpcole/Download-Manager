from .....common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineSetTracker:

	def __init__(self, torrentid, ignoreid):

		self.torrentid = torrentid

		self.ignoreid = ignoreid

		self.status = Enumeration.createenum(["Nothing", "Incomplete", "Completed", "Attention"], "Nothing")

# =========================================================================================

	def updatestatus(self, copyactionobject):

		torrentid = copyactionobject.gettorrentid()
		if torrentid != self.ignoreid:
			if (self.torrentid == torrentid) or (self.torrentid == ""):
				newcopystatus = copyactionobject.getstatus()
				if (newcopystatus == "Queued") or (newcopystatus == "In Progress"):
					if (self.status.getstatus("Nothing") == True) or (self.status.getstatus("Completed") == True):
						self.status.set("Incomplete")
				elif (newcopystatus == "Confirm") or (newcopystatus == "Failed"):
					self.status.set("Attention")
				elif newcopystatus == "Succeeded":
					if self.status.getstatus("Nothing") == True:
						self.status.set("Completed")



	def getstatus(self):

		return self.status.lower()


