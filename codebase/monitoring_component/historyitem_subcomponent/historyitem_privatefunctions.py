from ...common_components.datetime_datatypes import datetime_module as DateTime

def getdatetimeera(datetimeobject):

	thistimeera = datetimeobject.getiso()
	thistimeera = thistimeera[:11] + "000"
	return DateTime.createfromiso(thistimeera)


def geteradifference(origindatetimeobject, currentdatetimeobject):

	originitem = getdatetimeera(origindatetimeobject)
	currentitem = getdatetimeera(currentdatetimeobject)
	print(originitem.getiso(), currentitem.getiso())

	differencevalueobject = DateTime.secondsdifference(currentitem, originitem)
	differencevalue = differencevalueobject.getsecondsvalue()

	if differencevalue < 0:
		outcome = -99999
	else:
		outcome = int(differencevalue / 600)

	return outcome

