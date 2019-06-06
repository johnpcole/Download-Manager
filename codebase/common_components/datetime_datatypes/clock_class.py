class DefineClock:

	# ==========================================================================================
	# Object Setup
	# ==========================================================================================

	def __init__(self, hours, minutes, seconds):

		minutesoverflow = int(seconds / 60)

		actualseconds = seconds - (minutesoverflow * 60)

		combinedminutes = minutes + minutesoverflow

		hoursoverflow = int(combinedminutes / 60)

		actualminutes = combinedminutes - (hoursoverflow * 60)

		combinedhours = hours + hoursoverflow

		daysoverflow = int(combinedhours / 24)

		actualhours = combinedhours - (daysoverflow * 24)

		self.hours = actualhours

		self.minutes = actualminutes

		self.seconds = actualseconds

	# =========================================================================================

	def getvalue(self):

		totalminutes = self.minutes + (self.hours * 60)
		return (totalminutes * 60) + self.seconds

	# =========================================================================================

	def getsecondlessvalue(self):

		totalminutes = self.minutes + (self.hours * 60)
		return (totalminutes * 60)

	# =========================================================================================

	def gettext(self):

		return "%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds)

	# =========================================================================================

	def getsecondlesstext(self):

		return "%02d:%02d" % (self.hours, self.minutes)

	# =========================================================================================

	def gethour(self):

		return self.hours

	# =========================================================================================

	def getminute(self):

		return self.minutes

	# =========================================================================================

	def getsecond(self):

		return self.seconds

	# =========================================================================================

	def getmodularisedvalue(self, timebox):

		rawvalue = self.getvalue()
		modval = timebox.getvalue()
		multiple = int(rawvalue) / modval
		return (multiple * modval)

