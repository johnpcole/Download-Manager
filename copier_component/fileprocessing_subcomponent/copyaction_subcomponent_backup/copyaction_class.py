class DefineActionItem:

	def __init__(self, source, target, sizeorattempts, description):

		self.source = source

		self.target = target

		self.sizeorattempts = sizeorattempts

		self.description = description

		self.status = "queued"

# =========================================================================================

	def getinfo(self):

		if ((self.source)[-8:] == "CONNECT]") and (self.status == "copying"):
			realstatus = "connecting"
		else:
			realstatus = self.status
		outcome = {'description': self.description, 'status': realstatus, 'progress': self.sizeorattempts}

		return outcome

# =========================================================================================

	def getstatus(self):

		return self.status

# =========================================================================================

	def getsource(self):

		return self.source

# =========================================================================================

	def gettarget(self):

		return self.target

# =========================================================================================

	def startaction(self):

		outcome = False
		if self.status == "queued":
			outcome = True
			self.status = "copying"
			if (self.source)[-8:] == "CONNECT]":
				self.sizeorattempts = 1

		return outcome

# =========================================================================================

	def updateaction(self, osreturnvalue):

		if osreturnvalue == 0:
			self.status = "copied"
		else:
			if (self.source)[-8:] == "CONNECT]":
				self.sizeorattempts = self.sizeorattempts + 1
				if self.sizeorattempts > 9:
					self.sizeorattempts = 9
					self.status = "failed"
			else:
				self.status = "failed"

		if self.status == "failed":
			for j in range(0, 100000):
				pass


# =========================================================================================

	def getactiontype(self):

		if self.source == "[CONNECT]":
			actionoutcome = "Connect"
		elif self.source == "[DISCONNECT]":
			actionoutcome = "Disconnect"
		else:
			actionoutcome = "Copy File"

		return actionoutcome

