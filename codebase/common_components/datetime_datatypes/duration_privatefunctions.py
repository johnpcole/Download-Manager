# ---------------------------------------------------------
# Returns if a duration unit is valid
# ---------------------------------------------------------

def isdurationunitvalid(durationunit):

	outcome = False
	for x in ['Weeks', 'Days', 'Hours', 'Minutes', 'Seconds']:
		if x == durationunit:
			outcome = True

	return outcome


# ---------------------------------------------------------
# Returns a duration in a desired unit
# ---------------------------------------------------------

def convertunit(oldduration, oldunit, newunit):

	durationinseconds = abs(oldduration) * getunitmultiplier(oldunit)
	newduration = int(durationinseconds / getunitmultiplier(newunit))
	if oldduration < 0:
		newduration = 0 - newduration
	return newduration



# ---------------------------------------------------------
# Returns the conversion factor for a specified unit,
# compared to seconds
# ---------------------------------------------------------

def getunitmultiplier(unitlabel):

	if unitlabel == "Seconds":
		multiplier = 1
	elif unitlabel == "Minutes":
		multiplier = 60
	elif unitlabel == "Hours":
		multiplier = 3600
	elif unitlabel == "Days":
		multiplier = 86400
	elif unitlabel == "Weeks":
		multiplier = 604800
	else:
		multiplier = 0
		print("Invalid unit - ", unitlabel)

	return multiplier



