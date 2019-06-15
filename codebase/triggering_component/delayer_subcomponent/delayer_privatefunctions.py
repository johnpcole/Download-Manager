def getdatetimeera(datetimeobject):

	datetimetext = datetimeobject.getiso()
	return datetimetext[:12]
