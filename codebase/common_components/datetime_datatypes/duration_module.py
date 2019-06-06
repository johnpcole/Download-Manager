from . import duration_class as DurationClass



# ---------------------------------------------------------
# Creates a duration using an existing duration object
# ---------------------------------------------------------

def createfromobject(durationobject):

	newduration = DurationClass.DefineDuration()
	newduration.setfromobject(durationobject)
	return newduration



# ---------------------------------------------------------
# Creates a duration using a value-unit combination
# ---------------------------------------------------------

def createfromvalues(initialvalue, initialunit):

	newduration = DurationClass.DefineDuration()
	newduration.setfromvalues(initialvalue, initialunit)
	return newduration



# ---------------------------------------------------------
# Returns true if the duration is within a spefied period
# of time (which is also a duration)
# ---------------------------------------------------------

def iswithinlimit(testduration, thresholdduration):

	if abs(testduration.getsecondsvalue()) > abs(thresholdduration.getsecondsvalue()):
		outcome = False
	else:
		outcome = True

	return outcome



# ---------------------------------------------------------
# Returns the sum of two durations
# ---------------------------------------------------------

def add(first, second):

	newduration = createfromvalues(first.getsecondsvalue() + second.getsecondsvalue(), "Seconds")

	return newduration



# ---------------------------------------------------------
# Returns the difference between two durations
# ---------------------------------------------------------

def subtract(first, second):

	newduration = createfromvalues(first.getsecondsvalue() - second.getsecondsvalue(), "Seconds")

	return newduration



# ---------------------------------------------------------
# Returns true if two durations are identical
# ---------------------------------------------------------

def areidentical(first, second):

	if first.getsecondsvalue() == second.getsecondsvalue():
		outcome = True
	else:
		outcome = False

	return outcome