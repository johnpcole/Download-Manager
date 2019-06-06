# ---------------------------------------------------------
# Converts a hour, minute and second triplet into
# a secondsintoday integer
# ---------------------------------------------------------

def converttriplettoelapsedseconds(hour, minute, second):

	if istimevalid(hour, minute, second) == True:
		outcome = ((minute + (hour * 60)) * 60) + second
	else:
		outcome = -9999999

	return outcome



# ---------------------------------------------------------
# Converts a secondsintoday integer into a
# hour, minute, second triplet
# ---------------------------------------------------------

def convertelapsedsecondstotriplet(secondsintoday):

	hour = int((secondsintoday / 60) / 60)
	remainder = secondsintoday - (hour * 60 * 60)
	minute = int(remainder / 60)
	second = remainder - (minute * 60)

	return hour, minute, second



# ---------------------------------------------------------
# Converts a hour, minute, second triplet of integers
# into an iso (HHMMSS) string
# ---------------------------------------------------------

def converttriplettoiso(hour, minute, second):

	if istimevalid(hour, minute, second) == True:
		hourstring = str(hour)
		if len(hourstring) < 2:
			hourstring = "0" + hourstring
		minutestring = str(minute)
		if len(minutestring) < 2:
			minutestring = "0" + minutestring
		secondstring = str(second)
		if len(secondstring) < 2:
			secondstring = "0" + secondstring
		outcome = hourstring + minutestring + secondstring
	else:
		outcome = "??????"

	return outcome



# ---------------------------------------------------------
# Converts an iso (HHMMSS) string into a
# hour, minute, second triplet of integers
# ---------------------------------------------------------

def convertisototriplet(timestring):

	try:
		hour = int(timestring[0:2])
		minute = int(timestring[2:4])
		second = int(timestring[4:6])
	except:
		hour = -99999999
		minute = -99999999
		second = -99999999

	return hour, minute, second



# ---------------------------------------------------------
# Returns if a time is valid
# ---------------------------------------------------------

def istimevalid(hour, minute, second):

	outcome = True
	if (hour < 0) or (hour > 23):
		outcome = False
	if (minute < 0) or (minute > 59):
		outcome = False
	if (second < 0) or (second > 59):
		outcome = False

	return outcome



# ---------------------------------------------------------
# Returns an updated time and a day offsetter
# If the time has gone earlier than 00:00:00 or later
# than 23:59:59
# ---------------------------------------------------------

def sanitisetime(secondsintoday):

	dayoffset = 0
	if secondsintoday < 0:
		newsecondsintoday = secondsintoday + 86400
		resanitisedsecondsintoday, additionaldayoffset = sanitisetime(newsecondsintoday)
		dayoffset = additionaldayoffset - 1
	elif secondsintoday > 86399:
		newsecondsintoday = secondsintoday - 86400
		resanitisedsecondsintoday, additionaldayoffset = sanitisetime(newsecondsintoday)
		dayoffset = additionaldayoffset + 1
	else:
		resanitisedsecondsintoday = secondsintoday

	return resanitisedsecondsintoday, dayoffset



# ---------------------------------------------------------
# Returns a human readable version of the time, as a string
# ---------------------------------------------------------

def getreadabletime(hours, minutes, seconds, timeformat, secondsflag):

	outcome = ""
	if timeformat == "12ap":
		if hours > 11:
			outcome = " pm"
		else:
			outcome = " am"

	nhours = hours
	if (timeformat == "12") or (timeformat == "12ap"):
		if hours > 12:
			nhours = hours - 12
		if nhours == 0:
			nhours = 12
		htext = str(nhours)
	else:
		htext = gettwodigitvalue(nhours)



	if secondsflag == True:
		outcome = ":" + gettwodigitvalue(seconds) + outcome

	return htext + ":" + gettwodigitvalue(minutes) + outcome



def gettwodigitvalue(rawval):

	outcome = str(rawval)
	if rawval < 10:
		outcome = "0" + outcome

	return outcome