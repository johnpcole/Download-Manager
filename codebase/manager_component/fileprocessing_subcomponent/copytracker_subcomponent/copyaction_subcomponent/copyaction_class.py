from .....common_components.enumeration_datatype import enumeration_module as Enumeration


class DefineActionItem:

	def __init__(self, source, target, torrentid):

		self.source = source

		self.target = target

		self.status = Enumeration.createenum(["Queued", "In Progress", "Failed", "Succeeded", "Confirm"], "Queued")

		self.torrentid = torrentid


# =========================================================================================

	def updatestatus(self, newstatus):

		return self.status.set(newstatus)

# =========================================================================================

	def confirmstatus(self, statuscheck):

		return self.status.get(statuscheck)

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

	def getcopierpagedata(self):

		return {'source': self.source, 'target': self.target, 'torrentid': self.torrentid,
																'status': self.status.displaycurrent()}
