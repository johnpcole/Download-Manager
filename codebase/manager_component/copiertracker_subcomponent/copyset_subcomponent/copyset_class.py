from ....common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineSet:

	def __init__(self, torrentid):

		self.torrentid = torrentid

		self.copystatus = Enumeration.createenum(["Nothing", "Incomplete", "Completed", "Attention"], "Nothing")

# =========================================================================================

	def updatestatus(self, copyactionobject):

		if self.torrentid == "< REFRESH FOLDERS >":
			if copyactionobject.getactiontype() == "Scrape TV Shows":
				newcopystatus = copyactionobject.getstatus()
				if (newcopystatus == "Queued") or (newcopystatus == "In Progress"):
					self.copystatus.set("Incomplete")
		else:
			if (self.torrentid == copyactionobject.gettorrentid()) or (self.torrentid == "< ALL ACTION ITEMS >"):
				newcopystatus = copyactionobject.getstatus()
				if (newcopystatus == "Queued") or (newcopystatus == "In Progress"):
					if (self.copystatus.get("Nothing") is True) or (self.copystatus.get("Completed") is True):
						self.copystatus.set("Incomplete")
				elif (newcopystatus == "Confirm") or (newcopystatus == "Failed"):
					self.copystatus.set("Attention")
				elif newcopystatus == "Succeeded":
					if self.copystatus.get("Nothing") is True:
						self.copystatus.set("Completed")

		#print("tracker-id: ", self.torrentid, "   lookup-type: ", copyactionobject.getactiontype(),
		#		"   lookup-id: ", copyactionobject.gettorrentid(), "   lookup-state: ", copyactionobject.getstatus(),
		#		"   new-tracker-status: ", self.copystatus.displaycurrent())




	def getstatus(self):

		outcome = self.copystatus.displaycurrent()
		return outcome.lower()


