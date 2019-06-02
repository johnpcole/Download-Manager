from . import time_class as TimeClass



# ---------------------------------------------------------
# Creates the time using another Time object
# ---------------------------------------------------------

def createfromobject(timeobject):

	newtime = TimeClass.DefineTime()
	newtime.setfromobject(timeobject)
	return newtime



# ---------------------------------------------------------
# Creates the time using a Hour-Minute-Second triplet of integers
# ---------------------------------------------------------

def createfromtriplet(hour, minute, second):

	newtime = TimeClass.DefineTime()
	newtime.setfromtriplet(hour, minute, second)
	return newtime



# ---------------------------------------------------------
# Creates the time using a HHMMSS string
# ---------------------------------------------------------

def createfromiso(hourminutesecondstring):

	newtime = TimeClass.DefineTime()
	newtime.setfromiso(hourminutesecondstring)
	return newtime



# ---------------------------------------------------------
# Creates the time using a Seconds-into-Day integer
# ---------------------------------------------------------

def createfromsecondsintoday(secondsintodayinteger):

	newtime = TimeClass.DefineTime()
	newtime.setfromsecondsintoday(secondsintodayinteger)
	return newtime



# ---------------------------------------------------------
# Returns the difference, in seconds, between two times
# ---------------------------------------------------------

def secondsdifference(first, second):

		return (first.getsecondsintoday() - second.getsecondsintoday())


