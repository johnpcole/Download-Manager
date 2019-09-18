from ...common_components.enumeration_datatype import enumeration_module as Enumeration



class DefineInstruction:

	def __init__(self):

		self.copyid = "00000000000000000"

		self.actiontype = Enumeration.createenum(["Null", "File Copy", "Scrape TV Shows"], "Null")

		self.status = Enumeration.createenum(["All Done", "Succeeded", "In Progress", "Failed", "Confirm"], "All Done")

		self.resultsnotes = {}

# =========================================================================================

	def updateresults(self, newstatus, newnotes):

		self.status.set(newstatus)

		self.resultsnotes = newnotes

	def settonew(self, copyid, actiontype):

		self.copyid = copyid

		self.actiontype.set(actiontype)

		self.status.set("In Progress")

		self.resultsnotes = {}

	def setalldone(self):

		self.copyid = "00000000000000000"

		self.actiontype.set("Null")

		self.status.set("All Done")

		self.resultsnotes = {}


	def isalldone(self):

		return self.actiontype.get("Null")


	def getstatus(self):

		return {'copyid': self.copyid, 'outcome': self.status.displaycurrent(), 'notes': self.resultsnotes}

