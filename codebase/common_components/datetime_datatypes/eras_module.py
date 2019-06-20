from . import datetime_module as DateTime



def getera(datetimeobject, erasize):

	lookupsize = 15 - erasize
	datetimetext = datetimeobject.getiso()
	filler = "00000000"
	outcome = datetimetext[:lookupsize] + filler[:erasize-1]
	return outcome



def geteraasobject(datetimeobject, erasize):

	era = getera(datetimeobject, erasize)
	outcome = DateTime.createfromiso(era)
	return outcome



def compareeras(datetimeobjectone, datetimeobjecttwo, erasize):

	if getera(datetimeobjectone, erasize) == getera(datetimeobjecttwo, erasize):
		outcome = True
	else:
		outcome = False

	return outcome



def geteradifference(origindatetimeobject, currentdatetimeobject, erasize):

	originitem = geteraasobject(origindatetimeobject, erasize)
	currentitem = geteraasobject(currentdatetimeobject, erasize)

	differencevalueobject = DateTime.secondsdifference(currentitem, originitem)
	differencevalue = differencevalueobject.getsecondsvalue()

	divisor = 1
	if erasize > 1:
		divisor = divisor * 10
		if erasize > 2:
			divisor = divisor * 6
			if erasize > 3:
				divisor = divisor * 10
				if erasize > 4:
					divisor = divisor * 6

	return int(differencevalue / divisor)



def adjustobject(originaldatetimeobject, adjustvalue, erasize):

	newobject = DateTime.createfromobject(originaldatetimeobject)
	if erasize == 1:
		newobject.adjustseconds(adjustvalue)
	elif erasize == 2:
		newobject.adjustseconds(adjustvalue * 10)
	elif erasize == 3:
		newobject.adjustminutes(adjustvalue)
	elif erasize == 4:
		newobject.adjustminutes(adjustvalue * 10)
	else:
		newobject.adjusthours(adjustvalue)

	return newobject



def geteralabel(datetimeobject, erasize):

	era = getera(datetimeobject, erasize)

	if era[-6:] == "000000":
		outcome = era[6:8] + "-" + era[4:6] + "-" + era[0:4]
	else:
		outcome = era[8:10] + ":" + era[10:12]

	return outcome


