import datetime as PythonDateTime



# ---------------------------------------------------------
# Splits a datetime iso string into separate date &
# time iso strings
# ---------------------------------------------------------

def separatedatetimeisocomponents(datetimestring):

	if len(datetimestring) == 14:
		datestring = datetimestring[:8]
		timestring = datetimestring[8:]
	else:
		datestring = "99999999"
		timestring = "999999"

	return datestring, timestring



# ---------------------------------------------------------
# Gets the current time and puts into iso format
# ---------------------------------------------------------

def getcurrentdatetime():

	currentdatetime = str(PythonDateTime.datetime.now())
	#print("Current DateTime: ", currentdatetime)
	currentdate = currentdatetime[:4] + currentdatetime[5:7] + currentdatetime[8:10]
	#print("Current Date: ", currentdate)
	currenttime = currentdatetime[11:13] + currentdatetime[14:16] + currentdatetime[17:19]
	#print("Current Time: ", currenttime)

	return currentdate, currenttime



# ---------------------------------------------------------
# Gets the current fraction of second
# ---------------------------------------------------------

def getcurrentsubsecondfraction():

	currentdatetime = str(PythonDateTime.datetime.now())

	try:
		currentfraction = int(currentdatetime[20:22])
	except:
		currentfraction = 0

	return currentfraction



# ---------------------------------------------------------
# Gets the current fraction of second
# ---------------------------------------------------------

def getcurrentsecondfraction():
	currentdatetime = str(PythonDateTime.datetime.now())
	currentseconds = 100 * int(currentdatetime[17:19])

	try:
		currentfraction = int(currentdatetime[20:22])
	except:
		currentfraction = 0

	return currentseconds + currentfraction

