from ...common_components.datetime_datatypes import eras_module as EraFunctions



def getgraphaxes(nowtimedate, erasize, boxwidth, horizontaloffset, firsttop, secondtop, graphwidth, graphheight):

	linesoutcome = []
	littlelabelsoutcome = []
	biglabelsoutcome = []

	#horizontal axes
	linesoutcome.append(printline(horizontaloffset, firsttop, graphwidth, 0))
	linesoutcome.append(printline(horizontaloffset, secondtop, graphwidth, 0))

	#vertical axes
	linesoutcome.append(printline(horizontaloffset + 2, firsttop, 0, 0 - graphheight))
	linesoutcome.append(printline(horizontaloffset + 2, secondtop, 0, 0 - graphheight))


	# currentmarker = EraFunctions.geteraasobject(nowtimedate, 5)
	# currentmarker.adjusthours(-1)
	# markerposition = 0
	# while markerposition < 1000:
	# 	currentmarker.adjusthours(1)
	# 	markerposition = calculatecolumnposition(boxwidth, horizontaloffset, nowtimedate, currentmarker, erasize)
	# 	if markerposition >= horizontaloffset:
	#
	# 		if (currentmarker.gettimevalue() % 10800) == 0:
	# 			markerheight = 4
	# 			biglabelsoutcome.append(printtext(markerposition, firsttop + 16, EraFunctions.geteralabel(currentmarker, erasize)))
	# 			biglabelsoutcome.append(printtext(markerposition, secondtop + 16, EraFunctions.geteralabel(currentmarker, erasize)))
	# 		else:
	# 			markerheight = 2
	# 			littlelabelsoutcome.append(printtext(markerposition, firsttop + 12, EraFunctions.geteralabel(currentmarker, erasize)))
	# 			littlelabelsoutcome.append(printtext(markerposition, secondtop + 12, EraFunctions.geteralabel(currentmarker, erasize)))
	#
	# 		markersoutcome.append(printline(markerposition, firsttop, 0, markerheight))
	# 		markersoutcome.append(printline(markerposition, secondtop , 0, markerheight))

	return {"axeslines": linesoutcome, "biglabels": biglabelsoutcome, "littlelabels": littlelabelsoutcome}



def printrectangle(x, y, w, h):

	outcome = {}
	outcome["x"] = x
	outcome["y"] = y
	outcome["w"] = w
	outcome["h"] = h
	return outcome

def printline(x, y, w, h):

	outcome = {}
	outcome["xa"] = x
	outcome["ya"] = y
	outcome["xb"] = w + x
	outcome["yb"] = h + y
	return outcome

def printtext(x, y, t):

	outcome = {}
	outcome["x"] = x
	outcome["y"] = y
	outcome["t"] = t
	return outcome

def calculatecolumnposition(boxwidth, horizontaloffset, origindatetime, bardatetime, erasize):

	return ((boxwidth + 1) * EraFunctions.geteradifference(origindatetime, bardatetime, erasize)) + horizontaloffset


