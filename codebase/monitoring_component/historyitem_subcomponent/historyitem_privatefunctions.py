from ...common_components.datetime_datatypes import datetime_module as DateTime

def getdatetimeera(datetimeobject):

	thistimeera = datetimeobject.getiso()
	thistimeera = thistimeera[:11] + "000"

	return DateTime.createdatefromiso(thistimeera)


def geteradifference(origindatetimeobject, currentdatetimeobject):

	originitem = getdatetimeera(origindatetimeobject)
	currentitem = getdatetimeera(currentdatetimeobject)

	if DateTime.isfirstlaterthansecond(originitem, currentitem) == True:
		outcome = -99999
	else:
		differencevalue = DateTime.secondsdifference(originitem, currentitem)
		outcome = int(differencevalue / 600)

	return outcome

