from ...common_components.datetime_datatypes import eras_module as EraFunctions



def getgraphaxes(origintimedate, erasize, boxwidth, horizontaloffset, firsttop, secondtop, graphwidth, graphheight):

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

	currentmarker = EraFunctions.geteraasobject(origintimedate, 5)
	currentmarker.adjusthours(-1)
	markerposition = 0
	while markerposition < 1000:
		currentmarker.adjusthours(1)
		markerposition = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, currentmarker, erasize)
		if markerposition >= horizontaloffset + 2:

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


def getgraphblocks(origintimedate, erasize, boxwidth, horizontaloffset, firsttop, secondtop, graphwidth, graphheight, history, boxheight):

	outcome = {"brightred": [], "red": [], "orange": [], "amber": [], "yellow": [], "green": [], "blue": []}

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)

		if column >= horizontaloffset + 2:

			statusdata = historyitem.getgraphdata()
			statusdata = {'1_red': 4, '2_orange': 4, '3_amber': 4, '4_yellow': 4, '5_green': 4}
			blockcount = 0
			for colourkey in sorted(statusdata.keys()):
				if statusdata[colourkey] > 0:
					for indexer in range(0, statusdata[colourkey]):
						instruction = printrectangle(column, calculaterowposition(boxheight, firsttop, blockcount), boxwidth, boxheight)
						blockcount = blockcount + 1
						outcome[colourkey[2:]].append(instruction)

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

def calculaterowposition(boxheight, verticaloffset, previousboxes):

	return verticaloffset - ((boxheight + 1) * (previousboxes + 1)) - 1
