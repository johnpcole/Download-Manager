from ...common_components.datetime_datatypes import eras_module as EraFunctions



def getgraphaxes(nowtimedate, erasize, boxwidth, horizontaloffset, firsttop, secondtop, graphwidth, graphheight):

	outcome = {"axeslines": [], "biglabels": [], "littlelabels": []}

	#horizontal axes
	outcome["axeslines"].append(printline(horizontaloffset, firsttop, graphwidth, 0))
	outcome["axeslines"].append(printline(horizontaloffset, secondtop, graphwidth, 0))

	#vertical axes
	outcome["axeslines"].append(printline(horizontaloffset + 2, firsttop, 0, 0 - graphheight))
	outcome["axeslines"].append(printline(horizontaloffset + 2, secondtop, 0, 0 - graphheight))

	#vertical markers
	for indexer in [31, 61, 91, 121]:
		outcome["axeslines"].append(printline(horizontaloffset, firsttop - indexer, 2, 0))
		outcome["axeslines"].append(printline(horizontaloffset, secondtop - indexer, 2, 0))

	#horizontal markers

	currentmarker = EraFunctions.geteraasobject(nowtimedate, 5)
	currentmarker.adjusthours(-1)
	markerposition = 0
	while markerposition < 1000:
		currentmarker.adjusthours(1)
		markerposition = calculatecolumnposition(boxwidth, horizontaloffset, nowtimedate, currentmarker, erasize)
		if markerposition >= horizontaloffset:

			if (currentmarker.gettimevalue() % 10800) == 0:
				markerheight = 4
				texttype = "biglabels"
				textoffset = 16
			else:
				markerheight = 2
				texttype = "littlelabels"
				textoffset = 12

			outcome[texttype].append(printtext(markerposition, firsttop + textoffset, EraFunctions.geteralabel(currentmarker, erasize)))
			outcome[texttype].append(printtext(markerposition, secondtop + textoffset, EraFunctions.geteralabel(currentmarker, erasize)))
			outcome["axeslines"].append(printline(markerposition, firsttop, 0, markerheight))
			outcome["axeslines"].append(printline(markerposition, secondtop, 0, markerheight))

	return outcome



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


