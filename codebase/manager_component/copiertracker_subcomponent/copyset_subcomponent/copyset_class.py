from ....common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineSet:

	def __init__(self, torrentid):

		self.torrentid = torrentid

		self.copystatus = Enumeration.createenum(["Nothing", "Incomplete", "Completed", "Attention"], "Nothing")

# =========================================================================================

	def updatestatus(self, copyactionobject):

		torrentid = copyactionobject.gettorrentid()
		if (self.torrentid == torrentid) or (self.torrentid == "< ALL ACTION ITEMS >"):
			newcopystatus = copyactionobject.getstatus()
			if (newcopystatus == "Queued") or (newcopystatus == "In Progress"):
				if (self.copystatus.get("Nothing") == True) or (self.copystatus.get("Completed") == True):
					self.copystatus.set("Incomplete")
			elif (newcopystatus == "Confirm") or (newcopystatus == "Failed"):
				self.copystatus.set("Attention")
			elif newcopystatus == "Succeeded":
				if self.copystatus.get("Nothing") == True:
					self.copystatus.set("Completed")



	def getstatus(self):

		outcome = self.copystatus.displaycurrent()
		return outcome.lower()


