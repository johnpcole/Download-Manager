from . import date_privatefunctions as DateFunction

# ===========================================================================================================
# This class captures all dates. It is not meant to be used directly by programs, but called via the
# DateTime class.
# ===========================================================================================================

class DefineDate:

	def __init__(self):
		
		# Dates are stored as integers, capturing the number of days into the millennium
		# i.e. 1st Jan 2000 = 1
		self.daysintomillennium = -999
		



# ===========================================================================================================
# Basic Value Setters
# ===========================================================================================================

# ---------------------------------------------------------
# Sets the date using another Date object
# ---------------------------------------------------------

	def setfromobject(self, dateobject):

		self.daysintomillennium = dateobject.daysintomillennium



# ---------------------------------------------------------
# Sets the date using a Day-Month-Year triplet of integers
# ---------------------------------------------------------

	def setfromtriplet(self, day, month, year):

		self.daysintomillennium = DateFunction.converttriplettoelapseddays(day, month, year)



# ---------------------------------------------------------
# Sets the date using a YYYYMMDD string
# ---------------------------------------------------------

	def setfromiso(self, yearmonthdaystring):
	
		day, month, year = DateFunction.convertisototriplet(yearmonthdaystring)
		self.setfromtriplet(day, month, year)
	
	
	
# ---------------------------------------------------------
# Sets the date using a Days-into-Millennium integer
# ---------------------------------------------------------

	def setfromdaysintomillennium(self, daysintomillenniuminteger):
	
		self.daysintomillennium = daysintomillenniuminteger
	
	
	
# ===========================================================================================================
# Object Processing
# ===========================================================================================================
	
# ---------------------------------------------------------
# Adjusts the date by specified number of days (+ve or -ve)
# ---------------------------------------------------------

	def adjustdays(self, daysdelta):
	
		self.daysintomillennium = self.daysintomillennium + daysdelta

		
		
# ---------------------------------------------------------
# Adjusts the date by DateDuration (object)
# ---------------------------------------------------------

	def adjustdate(self, durationdelta):

		# Get the adjustment value and unit from the DateDuration object
		# This should only be in Days or Months
		adjustment, stepsize = durationdelta.getsanitised()
		
		# If Days (which includes Weeks and Lunars)
		if stepsize == "Days":
			self.adjustdays(adjustment)
		
		# If Months (which includes Years)
		elif stepsize == "Months":
			self.adjustmonths(adjustment)
		
		# Print an error
		else:
			print("Cannot Adjust (", stepsize, ")")

		
		
# ---------------------------------------------------------
# Adjusts the date by specified number of months (+ve or -ve)
# ---------------------------------------------------------

	def adjustmonths(self, monthsdelta):
	
		originalday, originalmonth, originalyear = self.gettriplet()
		if monthsdelta > 0:
			self.increasemonths(monthsdelta, originalday, originalmonth, originalyear)
		elif monthsdelta < 0:
			self.decreasemonths(abs(monthsdelta), originalday)



# ---------------------------------------------------------
# Increases the date by specified number of months
# WHICH MUST BE A POSITIVE NUMBER
# ---------------------------------------------------------

	def increasemonths(self, monthsincrease, originalday, originalmonth, originalyear):

		# Determine the index of the new month
		newmonthcount = originalmonth + monthsincrease
		
		# Determine the number of years which must be added to the date
		yearstoadd = int((newmonthcount - 1) / 12)
		
		# The new month value is the remainder
		newmonth = newmonthcount - (yearstoadd * 12)
		
		# New year value
		newyear = originalyear + yearstoadd
		
		# The maximum number of days in the new month
		maxdaysinnewmonth = DateFunction.getdaysinmonth(newmonth, DateFunction.isleapyear(newyear))
		
		# If the original day of the month is later than the last day
		# of the new month, reduce the day value
		newday = min(originalday, maxdaysinnewmonth)
		
		# Reset the date to have the new day-month-year values
		self.setfromtriplet(newday, newmonth, newyear)



# ---------------------------------------------------------
# Decreases the date by specified number of months
# WHICH MUST BE A POSITIVE NUMBER
# ---------------------------------------------------------

	def decreasemonths(self, monthsdecrease, originalday):
		
		# Turn the subtraction into an addition by winding the year back
		# in excess of the amount required
		yearstosubtract = int(monthsdecrease / 12) + 1
		
		# Reduce the date by the excess number of years
		self.adjustyears(0 - yearstosubtract)
		
		# Determine how many months need to be added in order
		# to replicate the original subtraction
		newmonthstoadd = (yearstosubtract * 12) - monthsdecrease
		
		# Increase the date by the required number of months
		self.adjustmonths(newmonthstoadd)
		
		# Capture this new date
		newday, newmonth, newyear = self.gettriplet()
		
		# Because two adjustments have been made above, inappropriate rounding may
		# have resulted if the new month is February. Correct...
		if (newmonth == 2) and (originalday > 28):
			self.setfromtriplet(DateFunction.getdaysinmonth(2, DateFunction.isleapyear(newyear)), newmonth, newyear)



# ---------------------------------------------------------
# Adjusts the date by specified number of years (+ve or -ve)
# ---------------------------------------------------------

	def adjustyears(self, yearsdelta):
	
		# Get the date as a triplet of integers
		originalday, originalmonth, originalyear = self.gettriplet()
		
		# Determine the new year value
		newyear = originalyear + yearsdelta
		
		# If the old date was a 29th Feb, ensure the
		# new date is 28th or 29th as appropriate
		if (originalmonth == 2) and (originalday == 29):
			newday = DateFunction.getdaysinmonth(2, DateFunction.isleapyear(newyear))
		
		# Otherwise the day value is unchanged
		else:
			newday = originalday
		
		# Reset the date to have the new day-month-year values
		self.setfromtriplet(newday, originalmonth, newyear)
			
			

# ===========================================================================================================
# Get Information
# ===========================================================================================================

# ---------------------------------------------------------
# Returns the date as a triplet of Day-Month-Year integers
# ---------------------------------------------------------

	def gettriplet(self):
	
		return DateFunction.convertelapseddaystotriplet(self.daysintomillennium)
	
	
	
# ---------------------------------------------------------
# Returns the date as a YYYYYMMDD string
# ---------------------------------------------------------

	def getiso(self):

		day, month, year = self.gettriplet()
		return DateFunction.converttriplettoiso(day, month, year)



# ---------------------------------------------------------
# Returns the date as a daysintomillennium integer
# ---------------------------------------------------------

	def getdaysintomillennium(self):

		return self.daysintomillennium



# ---------------------------------------------------------
# Returns the date as a readable string
# ---------------------------------------------------------

	def getreadabledate(self, dayflag, dateflag, monthflag, yearflag, separator):

		day, month, year = self.gettriplet()
		return DateFunction.getreadabledate(day, month, year, dayflag, dateflag, monthflag, yearflag, separator)



