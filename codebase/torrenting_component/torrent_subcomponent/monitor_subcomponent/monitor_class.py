

# This class creates an object which is used to capture tracker information about an individual torrent
# The object contains remotely read Deluge Daemon data and presents it in a Download-Manager friendly format


class DefineMonitor:

	def __init__(self):

		self.trackerstatus = "unknown"

		self.totaluploaded = 0

# =========================================================================================

	def updatetrackerstatus(self, newvalue):
		if newvalue[:5] == "Error":
			self.trackerstatus = "Red"
		else:
			self.trackerstatus = "Green"
		return self.trackerstatus

# =========================================================================================

	def updatetotaluploaded(self, newvalue):
		oldvalue = self.totaluploaded
		outcome = newvalue - oldvalue
		if outcome < 0:
			outcome = 0
		self.totaluploaded = newvalue
		return outcome


# =========================================================================================

	def updatemonitordata(self, datalist):

		outcome = {}
		outcome["trackerstatus"] = "unknown"
		outcome["uploaddelta"] = 0

		for dataitem in datalist:

			if dataitem == "trackerstatus":
				outcome["trackerstatus"] = self.updatetrackerstatus(datalist[dataitem])
			elif dataitem == "uploadedtotal":
				outcome["uploadeddelta"] = self.updatetotaluploaded(datalist[dataitem])
			else:
				outcome = "Unknown Data Label: " + dataitem
				assert 0 == 1, outcome

		return outcome

# =========================================================================================
