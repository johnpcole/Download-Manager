from . import date_class as DateClass



# ---------------------------------------------------------
# Creates the date using another Date object
# ---------------------------------------------------------

def createfromobject(dateobject):
	newdate = DateClass.DefineDate()
	newdate.setfromobject(dateobject)
	return newdate



# ---------------------------------------------------------
# Creates the date using a Day-Month-Year triplet of integers
# ---------------------------------------------------------

def createfromtriplet(day, month, year):
	newdate = DateClass.DefineDate()
	newdate.setfromtriplet(day, month, year)
	return newdate



# ---------------------------------------------------------
# Creates the date using a YYYYMMDD string
# ---------------------------------------------------------

def createfromiso(yearmonthdaystring):
	newdate = DateClass.DefineDate()
	newdate.setfromiso(yearmonthdaystring)
	return newdate



# ---------------------------------------------------------
# Creates the date using a Days-into-Millennium integer
# ---------------------------------------------------------

def createfromdaysintomillennium(daysintomillenniuminteger):
	newdate = DateClass.DefineDate()
	newdate.setfromdaysintomillennium(daysintomillenniuminteger)
	return newdate



# ---------------------------------------------------------
# Returns the difference, in days, between this date and
# the date (object) passed in
# ---------------------------------------------------------

def daysdifference(first, second):

	return (first.getdaysintomillennium() - second.getdaysintomillennium())



