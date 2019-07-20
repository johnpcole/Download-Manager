from . import clock_class as ClockClass
import datetime as PythonDateTime



def createastime(hours, minutes, seconds):
	
	return ClockClass.DefineClock(hours, minutes, seconds)



def createasinteger(timevalue):

	return ClockClass.DefineClock(0, 0, timevalue)



def createasclock(existingtime):
	return ClockClass.DefineClock(0, 0, existingtime.getvalue())



def getnow():

	currentdatetime = str(PythonDateTime.datetime.now())
	return ClockClass.DefineClock(int(currentdatetime[11:13]), int(currentdatetime[14:16]), int(currentdatetime[17:19]))



def getsecondlessnow():

	currentdatetime = str(PythonDateTime.datetime.now())
	return ClockClass.DefineClock(int(currentdatetime[11:13]), int(currentdatetime[14:16]), 0)



def timediff(earliertime, latertime):

	earlier = earliertime.getvalue()
	later = latertime.getvalue()
	sanitisedlater = getfuturetimevalue(later, earlier)
	return ClockClass.DefineClock(0, 0, sanitisedlater - earlier)



def timeadd(timeone, timetwo):

	return ClockClass.DefineClock(0, 0, timeone.getvalue() + timetwo.getvalue())



def isequal(timeone, timetwo):

	if timeone.getvalue() == timetwo.getvalue():
		return True
	else:
		return False



def convert24hourtohuman(hour):

	rawhour = hour % 12
	if rawhour == 0:
		return str(12)
	else:
		return str(rawhour)



def getfuturetimevalue(latertimevalue, earliertimevalue):

	if latertimevalue <= earliertimevalue:
		return (latertimevalue + (24 * 3600))
	else:
		return latertimevalue
