from ..common_components.datetime_datatypes import eras_module as EraFunctions



def getxaxis(nowtimedate, erasize, boxwidth, horizontaloffset):

	markersoutcome = []
	labelsoutcome = []
	currentmarker = EraFunctions.geteraasobject(nowtimedate, 5)
	while ((int(currentmarker[8:10])) % 3) != 0:
		currentmarker.adjusthours(-1)
	markerposition = 0
	while markerposition < 960:
		currentmarker.adjusthours(3)
		markerposition = ((boxwidth + 1) * EraFunctions.geteradifference(nowtimedate, currentmarker,
																					erasize)) + horizontaloffset + 1
		if markerposition >= horizontaloffset:
			instruction = 'x1="' + str(markerposition) + '" y1="130" x2="' + str(markerposition) + '" y2="132"'
			markersoutcome.append(instruction)
			instruction = 'x="' + str(markerposition) + '" y="145" >' + EraFunctions.geteralabel(currentmarker, erasize)
			labelsoutcome.append(instruction)
	return {"markers": markersoutcome, "labels": labelsoutcome}
