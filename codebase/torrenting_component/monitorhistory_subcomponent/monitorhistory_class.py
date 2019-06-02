


class DefineHistory:

	def __init__(self):

		self.history = {}

# =========================================================================================

	def addhistoryentry(self, newvalue):
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
