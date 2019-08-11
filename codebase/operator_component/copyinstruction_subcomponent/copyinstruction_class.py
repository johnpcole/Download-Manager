
class DefineInstruction:

	def __init__(self):

		self.copyid = "00000000000000000"

		self.actiontype = "Null"

		self.status = "All Done"

		self.resultsnotes = ""

# =========================================================================================

	def updatestatus(self, newstatus):

		self.status = newstatus


	def updatenotes(self, newnotes):

		self.resultsnotes = newnotes

		self.status = "Succeeded"

	def settonew(self, copyid, actiontype):

		self.copyid = copyid

		self.actiontype = actiontype

		self.status = "In Progress"

		self.resultsnotes = {}

	def setalldone(self):

		self.copyid = "00000000000000000"

		self.actiontype = "Null"

		self.status = "All Done"

		self.resultsnotes = {}


	def isalldone(self):

		if self.actiontype == "Null":
			outcome = True
		else:
			outcome = False
		return outcome


	def getstatus(self):

		return {'copyid': self.copyid, 'outcome': self.status, 'notes': self.resultsnotes}

