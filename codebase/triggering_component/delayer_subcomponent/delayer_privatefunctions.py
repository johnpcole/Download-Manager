def getdatetimeera(datetimeobject, erasize):

	lookupsize = 15 - erasize
	datetimetext = datetimeobject.getiso()
	return datetimetext[:lookupsize]



def comparedatetimes(datetimeobjectone, datetimeobjecttwo, erasize):

	if getdatetimeera(datetimeobjectone, erasize) == getdatetimeera(datetimeobjecttwo, erasize):
		outcome = True
	else:
		outcome = False

	return outcome