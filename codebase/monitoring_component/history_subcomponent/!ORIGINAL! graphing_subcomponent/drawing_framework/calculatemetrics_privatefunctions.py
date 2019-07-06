from .....common_components.datetime_datatypes import eras_module as EraFunctions


def columnposition(boxwidth, horizontaloffset, origindatetime, bardatetime, erasize):
	return (((boxwidth + 1) * EraFunctions.geteradifference(origindatetime, bardatetime, erasize)) + horizontaloffset)

def rowposition(boxheight, verticaloffset, previousboxes):
	return (verticaloffset - ((boxheight + 1) * (previousboxes + 1)) - 1)

def barheight(graphheight, datavalue, datavaluerange):
	return ((graphheight * min(datavalue, datavaluerange)) / datavaluerange)

def barscaling(erasize):

	if erasize == 4:
		divisor = 1.0
	elif erasize == 5:
		divisor = 6.0
	else:
		divisor = 1/0
	return divisor

def firstcurrentmarker(erasize, origintimedate):

	if erasize == 4:
		baselineerasize = 5
		baselineadjuster = -1
	elif erasize == 5:
		baselineerasize = 7
		baselineadjuster = -24
	else:
		x = 1/0

	currentmarker = EraFunctions.geteraasobject(origintimedate, baselineerasize)
	currentmarker.adjusthours(baselineadjuster)
	return currentmarker

def markertype(erasize, currentmarker):

	if erasize == 4:
		bigmarkergap = 10800
	elif erasize == 5:
		bigmarkergap = 86400
	else:
		x = 1 / 0

	if (currentmarker.gettimevalue() % bigmarkergap) == 0:
		outcome = "Big"
	else:
		outcome = "Little"

	return outcome

def markergapsize(erasize):

	if erasize == 4:
		littlemarkergap = 1
	elif erasize == 5:
		littlemarkergap = 6
	else:
		x = 1/0

	return littlemarkergap



