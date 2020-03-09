from .....common_components.dataconversion_framework import dataconversion_module as Functions


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
		# is a rounded number that may give false results)
		self.iscompleted = False


		self.eta = "!UNKNOWN!"

		self.activepeers = 0

		self.activeseeders = 0

		self.trackerstatus = "None"



# =========================================================================================

	def setsize(self, newvalue):
		self.size = Functions.sanitisesize(newvalue)

# =========================================================================================

	def setstatus(self, newvalue):
		self.status = newvalue.lower()


# =========================================================================================

	def setprogress(self, newvalue):
		self.progress = str(int(newvalue)) + "%"


# =========================================================================================

	def setfinished(self, newvalue):
		self.iscompleted = newvalue


# =========================================================================================

	def seteta(self, newvalue):
		self.eta = Functions.sanitisetime(newvalue)


# =========================================================================================

	def setactivepeers(self, newvalue):
		self.activepeers = newvalue


# =========================================================================================

	def setactiveseeders(self, newvalue):
		self.activeseeders = newvalue


# =========================================================================================

	def settrackerstatus(self, newvalue):
		self.trackerstatus = newvalue


# =========================================================================================

	def getfulltorrentstatus(self):

		if self.status == "queued":
			if self.iscompleted is True:
				outcome = "seeding_queued"
			else:
				outcome = "downloading_queued"
		elif self.status == "paused":
			if self.iscompleted is True:
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

	def getconnectionstatusdata(self):

		outcome = {'activedownloads': 0, 'activeuploads': 0, 'downloadcount': 0, 'uploadcount': 0,
									'redcount': 0, 'orangecount': 0, 'ambercount': 0, 'yellowcount': 0, 'greencount': 0}

		torrentstatus = self.getfulltorrentstatus()
		if torrentstatus[-6:] == "active":
			outcome[self.gettrackerstatus() + 'count'] = 1
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

		if self.iscompleted is True:
			outcome = "Completed"
		else:
			outcome = "In Progress"
		return outcome

# =========================================================================================

	def gettrackerstatus(self):
		if self.trackerstatus.find(" Announce OK") != -1:
			outcome = 'green'
		elif self.trackerstatus.find(" Error: ") != -1:
			if self.trackerstatus.find(" Error: timed out") != -1:
				outcome = 'amber'
			elif self.trackerstatus.find(" Error: Invalid argument") != -1:
				outcome = 'orange'
			else:
				outcome = 'red'
		else:
			outcome = 'yellow'

		return outcome



