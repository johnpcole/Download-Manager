from .....common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineActionItem:

	def __init__(self, source, target, torrentid, torrentname):

		self.source = source

		self.target = target

		self.status = Enumeration.createenum(["Queued", "In Progress", "Failed", "Succeeded", "Confirm", "Discarded"],
																											"Queued")

		self.torrentid = torrentid

		self.torrentname = torrentname

		self.cacheupdateflag = False

# =========================================================================================

	def getcachestate(self):

		return self.cacheupdateflag

# =========================================================================================

	def updatestatus(self, newstatus):

		self.cacheupdateflag = True
		return self.status.set(newstatus)

# =========================================================================================

	def getstatus(self):

		return self.status.displaycurrent()

# =========================================================================================

	def gettorrentid(self):

		return self.torrentid

# =========================================================================================

	def getinstruction(self):

		return {'source': self.source, 'target': self.target}

# =========================================================================================

	def getdescription(self):

		space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
		arrows = space + space + "&darr;"
		indent = space + space + space + space + space
		lineofarrows = arrows + arrows + arrows + arrows + arrows
		outcome = "</br>" + indent + self.source + "</br>" + indent + lineofarrows + "</br>" + indent + self.target
		return outcome

# =========================================================================================

	def getactioncopierpagedata(self):

		statuslabel = self.status.displaycurrent()
		if statuslabel == "In Progress":
			statuslabel = "InProgress"
		target = self.target
		target = target.replace("/", " / ")
		self.cacheupdateflag = False
		return {'source': self.source, 'target': target[1:], 'torrentid': self.torrentid,
														'torrentname': self.torrentname, 'status': statuslabel.lower()}


# =========================================================================================

	def getactioncopierpageupdatedata(self):

		statuslabel = self.status.displaycurrent()
		if statuslabel == "In Progress":
			statuslabel = "InProgress"
		self.cacheupdateflag = False
		return {'status': statuslabel.lower()}

# =========================================================================================
