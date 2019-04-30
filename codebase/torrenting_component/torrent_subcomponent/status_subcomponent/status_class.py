from ....functions_component import functions_module as Functions


# This class creates an object which is used to capture status information about an individual torrent
# The object contains remotely read Deluge Daemon data and presents it in a Download-Manager friendly format


class DefineStatus:

	def __init__(self):

		# The size of the torrent, captured as a string containing the value and units (string)
		self.size = "!UNKNOWN!"

		# The Download-Manager status, which can be set to seeding_queued, downloading_queued, seeding_paused,
		# downloading_paused, downloading_active, seeding_active or the Deluge status (string)
		self.status = "!UNKNOWN!"

		# The percentage of the torrent downloaded, captured as a string containing the value and percent
		# symbol (string)
		self.progress = -99999

		# Defines whether the torrent has completed downloading or not (without relying on the percentage, which
		# is a rounded number that may give false results); Can be set to In Progress or Completed (string)
		self.finished = "In Progress"


		self.eta = "!UNKNOWN!"

		self.activepeers = 0

		self.activeseeders = 0


	def setsize(self, newvalue):
		self.size = Functions.sanitisesize(newvalue)


	def setstatus(self, newvalue):
		self.status = newvalue.lower()


	def setprogress(self, newvalue):
		self.progress = str(int(newvalue)) + "%"


	def setfinished(self, newvalue):
		if newvalue == True:
			self.finished = "Completed"
		else:
			self.finished = "In Progress"


	def seteta(self, newvalue):
		self.eta = Functions.sanitisetime(newvalue)


	def setactivepeers(self, newvalue):
		self.activepeers = newvalue


	def setactiveseeders(self, newvalue):
		self.activeseeders = newvalue


# =========================================================================================

	def getfulltorrentstatus(self):

		if self.status == "queued":
			if self.finished == "Completed":
				outcome = "seeding_queued"
			else:
				outcome = "downloading_queued"
		elif self.status == "paused":
			if self.finished == "Completed":
				outcome = "seeding_paused"
			else:
				outcome = "downloading_paused"
		elif self.status == "downloading":
			outcome = "downloading_active"
		elif self.status == "seeding":
			outcome = "seeding_active"
		else:
			outcome = self.status
		return outcome

# =========================================================================================

	def getprogresssizeeta(self):

		if self.progress == "100%":
			outcome = ""
		else:
			outcome = self.progress

		if outcome != "":
			outcome = outcome + " of "
		outcome = outcome + self.size

		if self.getfulltorrentstatus() == "downloading_active":
			outcome = outcome + " (~" + self.eta + ")"

		return outcome

# =========================================================================================

	def getconnectiondata(self):

		outcome = {}
		outcome['activedownloads'] = 0
		outcome['activeuploads'] = 0
		outcome['downloadcount'] = 0
		outcome['activedownloads'] = 0

		torrentstatus = self.getfulltorrentstatus()
		if torrentstatus[-6:] == "active":
			outcome['uploadcount'] = 1
			if self.activepeers > 0:
				outcome['activeuploads'] = 1
			if torrentstatus == "downloading_active":
				outcome['downloadcount'] = 1
				if self.activeseeders > 0:
					outcome['activedownloads'] = 1

		return outcome

# =========================================================================================

	def getprogress(self):

		return self.progress

# =========================================================================================

	def getfinished(self):

		return self.finished
