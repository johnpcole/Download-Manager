from ...common_components.datetime_datatypes import datetime_module as DateTime

def getdatetimeera(datetimeobject):

	thistimeera = datetimeobject.getiso()
	thistimeera = thistimeera[:11] + "000"
	print(thistimeera)
	return DateTime.createfromiso(thistimeera)


def geteradifference(origindatetimeobject, currentdatetimeobject):

	originitem = getdatetimeera(origindatetimeobject)
	currentitem = getdatetimeera(currentdatetimeobject)
	print(originitem.getiso(), currentitem.getiso(), DateTime.secondsdifference(originitem, currentitem))


	if DateTime.isfirstlaterthansecond(originitem, currentitem) == True:
		outcome = -99999
	else:
		differencevalue = DateTime.secondsdifference(originitem, currentitem)
		outcome = int(differencevalue.getsecondsvalue() / 600)

	return outcome

