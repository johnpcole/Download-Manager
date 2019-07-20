from . import datetime_class as DateTimeClass
from . import duration_module as Duration
from .date_subcomponent import date_module as Date
from .time_subcomponent import time_module as Time


# ---------------------------------------------------------
# Creates a datetime using an existing datetime object
# ---------------------------------------------------------

def createfromobject(datetimeobject):

	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.setfromobject(datetimeobject)
	return newdatetime



# ---------------------------------------------------------
# Creates a datetime using a
# Day-Month-Year-Hour-Minute-Second sextuplet of integers
# ---------------------------------------------------------

def createfromsextuplet(day, month, year, hour, minute, second):

	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.setfromsextuplet(day, month, year, hour, minute, second)
	return newdatetime



# ---------------------------------------------------------
# Creates a date using a
# Day-Month-Year triplet of integers
# ---------------------------------------------------------

def createdatefromtriplet(day, month, year):

	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.setfromsextuplet(day, month, year, 0, 0, 0)
	return newdatetime



# ---------------------------------------------------------
# Creates a time using a
# Hour-Minute-Second triplet of integers
# ---------------------------------------------------------

def createtimefromtriple(hour, minute, second):

	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.setfromsextuplet(1, 1, 2100, hour, minute, second)
	return newdatetime



# ---------------------------------------------------------
# Creates a date using a YYYYMMDD string
# ---------------------------------------------------------

def createdatefromiso(isostring):

	return createfromiso(isostring + "000000")



# ---------------------------------------------------------
# Creates a date using a HHMMSS string
# ---------------------------------------------------------

def createtimefromiso(isostring):

	return createfromiso("21000101" + isostring)



# ---------------------------------------------------------
# Creates a datetime using a YYYYMMDDHHMMSS string
# ---------------------------------------------------------

def createfromiso(isostring):

	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.setfromiso(isostring)
	return newdatetime



# ---------------------------------------------------------
# Creates a date using a daysintomillennium integer
# ---------------------------------------------------------

def createdatefromvalue(daysintomillenniuminteger):

	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.setdatefromvalue(daysintomillenniuminteger)
	newdatetime.settimefromiso("000000")
	return newdatetime



# ---------------------------------------------------------
# Creates a time using a secondsintoday integer
# ---------------------------------------------------------

def createtimefromvalue(secondsintodayinteger):

	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.settimefromvalue(secondsintodayinteger)
	newdatetime.setdatefromiso("21000101")
	return newdatetime



# ---------------------------------------------------------
# Returns the difference, in seconds, between this datetime
# and the datetime (object) passed in
# ---------------------------------------------------------

def secondsdifference(first, second):

	datedifference = Duration.createfromvalues(
											Date.daysdifference(first.getdatecomponent(), second.getdatecomponent()),
																										"Days")

	timedifference = Duration.createfromvalues(
											Time.secondsdifference(first.gettimecomponent(), second.gettimecomponent()),
																										"Seconds")

	return Duration.add(datedifference, timedifference)



# ---------------------------------------------------------
# Returns whether the first is later than the second
# ---------------------------------------------------------

def isfirstlaterthansecond(first, second):

	differenceduration = secondsdifference(first, second)

	if differenceduration.getsecondsvalue() > 0:
		outcome = True
	else:
		outcome = False

	return outcome



# ---------------------------------------------------------
# Returns whether the first is identical to the second
# ---------------------------------------------------------

def areidentical(first, second):

	differenceduration = secondsdifference(first, second)

	if differenceduration.getsecondsvalue() == 0:
		outcome = True
	else:
		outcome = False

	return outcome



# ---------------------------------------------------------
# Get Now
# ---------------------------------------------------------

def getnow():
	
	newdatetime = DateTimeClass.DefineDateTime()
	newdatetime.settonow()
	return newdatetime



def getnowfraction(secondsmodeflag):
	newdatetime = DateTimeClass.DefineDateTime()
	return newdatetime.getdummynowfraction(secondsmodeflag)
