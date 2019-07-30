def sanitisestatus(statuslabel):

	if statuslabel == "In Progress":
		outcome = "InProgress"
	else:
		outcome = statuslabel

	return outcome.lower()




def sanitisetargetpath(rawpath):

	target = rawpath
	target = target.replace("/", " / ")
	return target[1:]




def sanitisecopydatetimestamp(actionid):

	datetime = actionid[:4] + "-" + actionid[4:6] + "-" + actionid[6:8] + " "
	datetime = datetime + actionid[8:10] + ":" + actionid[10:12] + ":" + actionid[12:14]
	datetime = datetime + " [" + actionid[14:] + "]"

	return datetime


