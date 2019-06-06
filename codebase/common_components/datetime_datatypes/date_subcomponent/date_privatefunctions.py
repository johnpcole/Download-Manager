# ---------------------------------------------------------
# Converts a day, month and year triplet into
# a daysinmillennium integer
# ---------------------------------------------------------

def converttriplettoelapseddays(day, month, year):

	if isdatevalid(day, month, year) == True:
		outcome = extractelapseddaysfromyear(year) + extractelapseddaysfrommonth(month, year) + day
	else:
		outcome = -999

	return outcome



# ---------------------------------------------------------
# Converts a daysinmillennium integer into a
# day, month and year triplet
# ---------------------------------------------------------

def convertelapseddaystotriplet(daysintomillennium):

	year, daysintocurrentyear, isthisleapyear = extractyearfromdays(daysintomillennium)
#	print("Year = ", year, "     | Remaining days into year = ", daysintocurrentyear, "     (Leap year = ", isthisleapyear, ")")
	month, day = extractmonthfromdays(daysintocurrentyear, isthisleapyear)
#	print("Month = ", month, "     | Day = ", day)
	return day, month, year



# ---------------------------------------------------------
# Converts a day, month, year triplet of integers
# into an iso (YYYYYMMDD) string
# ---------------------------------------------------------

def converttriplettoiso(day, month, year):

	if isdatevalid(day, month, year) == True:
		monthstring = str(month)
		if len(monthstring) < 2:
			monthstring = "0" + monthstring
		daystring = str(day)
		if len(daystring) < 2:
			daystring = "0" + daystring
		outcome = str(year) + monthstring + daystring
	else:
		outcome = "????????"

	return outcome



# ---------------------------------------------------------
# Converts an iso (YYYYYMMDD) string into a
# day, month, year triplet of integers
# ---------------------------------------------------------

def convertisototriplet(datestring):

	try:
		year = int(datestring[0:4])
		month = int(datestring[4:6])
		day = int(datestring[6:8])
	except:
		year = -999
		month = -999
		day = -999

	return day, month, year



# ---------------------------------------------------------
# Converts an integer year, 2000-2099 into a number of
# days into the millennium, to day before 1st Jan 20xx
# ---------------------------------------------------------

def extractelapseddaysfromyear(year):

	if isyearvalid(year) == True:
		yearssincetwothousand = year - 2000
		daycount = 0
		if yearssincetwothousand > 0:
			for currentyear in range(0, yearssincetwothousand):
				daycount = daycount + getdaysinyear(isleapyear(currentyear))
	else:
		daycount = -999
	return daycount



# ---------------------------------------------------------
# Converts an integer month, 1-12 into a number of
# days into the year, to day before 1st xxx
# ---------------------------------------------------------

def extractelapseddaysfrommonth(month, year):

	if ismonthvalid(month) == True:
		monthdaycounts = getlistofmonthdays(isleapyear(year))
		totaldaycount = 0
		for currentmonth in range(0, 11):
			if month > (currentmonth + 1):
				totaldaycount = totaldaycount + monthdaycounts[currentmonth]
	else:
		totaldaycount = -999

	return totaldaycount



# ---------------------------------------------------------
# Determines if the integer year, 2000-2099, is a leap year
# ---------------------------------------------------------

def isleapyear(year):

	if (year % 4) == 0:
		outcome = True
	else:
		outcome = False

	return outcome



# ---------------------------------------------------------
# Extracts the AD year number of a daysinmillennium integer
# as well as the remainder number of days in the year
# and whether the year is a leap year
# ---------------------------------------------------------

def extractyearfromdays(daysintomillennium):

	fouryearblocks = int((daysintomillennium - 1) / 1461)
	daysintofouryearblock = daysintomillennium - (fouryearblocks * 1461)
	year = 2000 + (fouryearblocks * 4)

	yeardaycounts = [366, 365, 365]  # Final year isn't required
	yeardayoffset = 0
	isleapyear = True
	daysintocurrentyear = daysintofouryearblock
	for currentyear in range(0, 3):
		yeardayoffset = yeardayoffset + yeardaycounts[currentyear]
		if daysintofouryearblock > yeardayoffset:
			isleapyear = False
			year = year + 1
			daysintocurrentyear = daysintocurrentyear - yeardaycounts[currentyear]

	return year, daysintocurrentyear, isleapyear



# ---------------------------------------------------------
# Extracts the month of a daysinyear integer and leap year
# flag, as well as the remainder number of days in the
# month
# ---------------------------------------------------------

def extractmonthfromdays(daysintocurrentyear, isleapyear):

	monthdaycounts = getlistofmonthdays(isleapyear)
	monthdayoffset = 0
	month = 1
	daysintocurrentmonth = daysintocurrentyear
	for currentmonth in range(0, 11):
		monthdayoffset = monthdayoffset + monthdaycounts[currentmonth]
		if daysintocurrentyear > monthdayoffset:
			month = month + 1
			daysintocurrentmonth = daysintocurrentmonth - monthdaycounts[currentmonth]

	return month, daysintocurrentmonth



# ---------------------------------------------------------
# Returns the list of month lengths, taking into account
# if the year is a leap year
# ---------------------------------------------------------

def getlistofmonthdays(isyearleapyear):

	if isyearleapyear == True:
		februarydaycount = 29
	else:
		februarydaycount = 28

	return [31, februarydaycount, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]



# ---------------------------------------------------------
# Returns the size of the month, taking into account
# if the year is a leap year
# ---------------------------------------------------------

def getdaysinmonth(month, isyearleapyear):

	if ismonthvalid(month) == True:
		monthdays = getlistofmonthdays(isyearleapyear)
		outcome = monthdays[month - 1]
	else:
		outcome = -999

	return outcome



# ---------------------------------------------------------
# Returns the size of the year, taking into account
# if the year is a leap year
# ---------------------------------------------------------

def getdaysinyear(isyearleapyear):

	if isyearleapyear == True:
		daycount = 366
	else:
		daycount = 365

	return daycount



# ---------------------------------------------------------
# Returns if an integer year is valid (2000-2099)
# ---------------------------------------------------------

def isyearvalid(year):

	if (year > 1999) and (year < 2100):
		outcome = True
	else:
		outcome = False

	return outcome



# ---------------------------------------------------------
# Returns if an integer month is valid (1-12)
# ---------------------------------------------------------

def ismonthvalid(month):

	if (month > 0) and (month < 13):
		outcome = True
	else:
		outcome = False

	return outcome



# ---------------------------------------------------------
# Returns if an integer day, for a given month/year is valid
# ---------------------------------------------------------

def isdatevalid(day, month, year):

	if (ismonthvalid(month) == True) and (isyearvalid(year) == True):
		if (day > 0) and (day < 1 + getdaysinmonth(month, isleapyear(year))):
			outcome = True
		else:
			outcome = False
	else:
		outcome = False

	return outcome



# ---------------------------------------------------------
# Returns a human readable version of the date, as a string
# ---------------------------------------------------------

def getreadabledate(day, month, year, dayflag, dateflag, monthflag, yearflag, separator):

	outcome = ""

	# Year
	if yearflag != "0":
		outcome = str(year)
		if yearflag == "2":
			outcome = outcome[-2:]
		outcome = separator + outcome

	# Month
	if monthflag != "0":
		if monthflag == "4":
			ml = getmonthlabel(month)
		elif monthflag == "3":
			ml = getmonthlabel(month)[:3]
		elif monthflag =="2":
			ml = gettwodigitvalue(month)
		else:
			ml = str(month)
		outcome = separator + ml + outcome

	# Day
	if dateflag == "3":
		dl = getordinallabel(day)
	elif dateflag == "2":
		dl = gettwodigitvalue(day)
	else:
		dl = str(day)
	outcome = dl + outcome

	# Day of week
	if dayflag != "0":
		wl = getdayofweek(day, month, year)
		if dayflag == "3":
			wl = wl[:3]
		outcome = wl + " " + outcome


	return outcome



def getdayofweek(day, month, year):

	dayindex = converttriplettoelapseddays(day, month, year) % 7
	if dayindex == 1:
		outcome = "Saturday"
	elif dayindex == 2:
		outcome = "Sunday"
	elif dayindex == 3:
		outcome = "Monday"
	elif dayindex == 4:
		outcome = "Tuesday"
	elif dayindex == 5:
		outcome = "Wednesday"
	elif dayindex == 6:
		outcome = "Thursday"
	elif dayindex == 7:
		outcome = "Friday"
	else:
		outcome = "?????"
	return outcome
	
	
	
def getmonthlabel(monthval):

	if monthval == 1:
		outcome = "January"
	elif monthval == 2:
		outcome = "February"
	elif monthval == 3:
		outcome = "March"
	elif monthval == 4:
		outcome = "April"
	elif monthval == 5:
		outcome = "May"
	elif monthval == 6:
		outcome = "June"
	elif monthval == 7:
		outcome = "July"
	elif monthval == 8:
		outcome = "August"
	elif monthval == 9:
		outcome = "September"
	elif monthval == 10:
		outcome = "October"
	elif monthval == 11:
		outcome = "November"
	elif monthval == 12:
		outcome = "December"
	else:
		outcome = "?????"

	return outcome



def getordinallabel(dayval):

	dl = str(dayval)
	if (dayval == 1) or (dayval == 21) or (dayval == 31):
		outcome = dl + "st"
	elif (dayval == 2) or (dayval == 22):
		outcome = dl + "nd"
	elif (dayval == 3) or (dayval == 23):
		outcome = dl + "rd"
	else:
		outcome = dl + "th"

	return outcome



def gettwodigitvalue(dayormonthval):

	outcome = str(dayormonthval)
	if dayormonthval < 10:
		outcome = "0" + outcome

	return outcome