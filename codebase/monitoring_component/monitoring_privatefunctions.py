from ..common_components.datetime_datatypes import eras_module as EraFunctions



def getxaxis(nowtimedate, erasize, boxwidth, horizontaloffset, verticaloffset):

	top = verticaloffset + 7
	markersoutcome = []
	labelsoutcome = []
	currentmarker = EraFunctions.geteraasobject(nowtimedate, 5)
	currentmarker.adjusthours(-1)
	markerposition = 0
	while markerposition < 960:
		currentmarker.adjusthours(1)
		markerposition = ((boxwidth + 1) * EraFunctions.geteradifference(nowtimedate, currentmarker,
																					erasize)) + horizontaloffset + 1
		if (currentmarker.gettimevalue() % 86400) == 0:
			bottom = top + 6
		elif (currentmarker.gettimevalue() % 10800) == 0:
			bottom = top + 4
		else:
			bottom = top + 2

		if markerposition >= horizontaloffset:
			instruction = 'x1="' + str(markerposition) + '" y1="' + str(top) + '" x2="' + str(markerposition) + '" y2="' + str(bottom) + '"'
			markersoutcome.append(instruction)
			if (currentmarker.gettimevalue() % 10800) == 0:
				instruction = 'x="' + str(markerposition) + '" y="' + str(bottom + 13) + '" >' + EraFunctions.geteralabel(currentmarker, erasize)
				labelsoutcome.append(instruction)
	return {"markers": markersoutcome, "labels": labelsoutcome}
