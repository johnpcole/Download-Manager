from . import time_privatefunctions as TimeFunction

# ===========================================================================================================
# This class captures all times. It is not meant to be used directly by programs, but called via the
# DateTime class.
# ===========================================================================================================



class DefineTime:

	def __init__(self):
		
		# Times are stored as integers, capturing the number of seconds passed in the day
		# i.e. 00:00:00 = 0
		self.secondsintoday = -99999999999999999



# ===========================================================================================================
# Basic Value Setters
# ===========================================================================================================

# ---------------------------------------------------------
# Sets the time using another Time object
# ---------------------------------------------------------

	def setfromobject(self, timeobject):

		self.secondsintoday = timeobject.secondsintoday



# ---------------------------------------------------------
# Sets the time using a Hour-Minute-Second triplet of integers
# ---------------------------------------------------------

	def setfromtriplet(self, hour, minute, second):

		self.secondsintoday = TimeFunction.converttriplettoelapsedseconds(hour, minute, second)



# ---------------------------------------------------------
# Sets the time using a HHMMSS string
# ---------------------------------------------------------

	def setfromiso(self, hourminutesecondstring):
	
		hour, minute, second = TimeFunction.convertisototriplet(hourminutesecondstring)
		self.setfromtriplet(hour, minute, second)
	
	
	
# ---------------------------------------------------------
# Sets the time using a Seconds-into-Day integer
# ---------------------------------------------------------

	def setfromsecondsintoday(self, secondsintodayinteger):
	
		self.secondsintoday = secondsintodayinteger
	
	
	

# ===========================================================================================================
# Object Processing
# ===========================================================================================================

# ---------------------------------------------------------
# Adjusts the time by specified number of seconds (+ve or -ve)
# Returns an integer to indicate how many midnights have
# passed as a result of the adjustment
# ---------------------------------------------------------

	def adjustseconds(self, secondsdelta):

		self.secondsintoday = self.secondsintoday + secondsdelta
		sanitisedsecondsintoday, dayoffset = TimeFunction.sanitisetime(self.secondsintoday)
		self.secondsintoday = sanitisedsecondsintoday

		return dayoffset



# ---------------------------------------------------------
# Adjusts the time by specified number of minutes (+ve or -ve)
# Returns an integer to indicate how many midnights have
# passed as a result of the adjustment
# ---------------------------------------------------------

	def adjustminutes(self, minutesdelta):

		return self.adjustseconds(60 * minutesdelta)



# ---------------------------------------------------------
# Adjusts the time by specified number of hours (+ve or -ve)
# Returns an integer to indicate how many midnights have
# passed as a result of the adjustment
# ---------------------------------------------------------

	def adjusthours(self, hoursdelta):

		return self.adjustminutes(60 * hoursdelta)



# ===========================================================================================================
# Get Information
# ===========================================================================================================

# ---------------------------------------------------------
# Returns the time as a triplet of Hour-Minute-Second integers
# ---------------------------------------------------------

	def gettriplet(self):
	
		return TimeFunction.convertelapsedsecondstotriplet(self.secondsintoday)
	
	
	
# ---------------------------------------------------------
# Returns the time as a HHMMSS string
# ---------------------------------------------------------

	def getiso(self):

		hour, minute, second = self.gettriplet()
		return TimeFunction.converttriplettoiso(hour, minute, second)



	# ---------------------------------------------------------
	# Returns the time as a seconds-into-day integer
	# ---------------------------------------------------------

	def getsecondsintoday(self):

		return self.secondsintoday



	# ---------------------------------------------------------
	# Returns the time as a seconds-into-day integer
	# ---------------------------------------------------------

	def getreadabletime(self, timeformat, secondsflag):

		hour, minute, second = self.gettriplet()
		return TimeFunction.getreadabletime(hour, minute, second, timeformat, secondsflag)


