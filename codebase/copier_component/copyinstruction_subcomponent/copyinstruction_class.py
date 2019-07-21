
class DefineInstruction:

	def __init__(self):

		self.copyid = "00000000000000000"

		self.status = "All Done"

		self.notes = ""

# =========================================================================================

	def updatestatus(self, newstatus):

		self.status = newstatus


	def updatenotes(self, newnotes):

		self.notes = newnotes

		self.status = "Succeeded"

	def settonew(self, copyid):

		self.copyid = copyid

		self.status = "In Progress"

		self.notes = {}

	def setalldone(self):

		self.copyid = "00000000000000000"

		self.status = "All Done"

		self.notes = {}

	def setrefreshfolders(self):

		self.copyid = "-----------------"

		self.status = "In Progress"

		self.notes = {}


	def isalldone(self):

		if self.copyid == "00000000000000000":
			outcome = True
		else:
			outcome = False
		return outcome

	def getstatus(self):

		return {'copyid': self.copyid, 'outcome': self.status, 'notes': self.notes}

