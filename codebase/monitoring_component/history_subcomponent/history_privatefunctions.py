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
	column = 0
	hoffset = horizontaloffset + (boxwidth / 2.0)
	while column < 1000:
		currentmarker.adjusthours(1)
		column = calculatecolumnposition(boxwidth, hoffset, origintimedate, currentmarker, erasize)
		if column >= horizontaloffset + 2:

			if (currentmarker.gettimevalue() % 10800) == 0:
				markerheight = 4
				texttype = "biglabels"
				textoffset = 16
			else:
				markerheight = 2
				texttype = "littlelabels"
				textoffset = 12

			outcome[texttype].append(printtext(column, firsttop + textoffset, EraFunctions.geteralabel(currentmarker, erasize)))
			outcome[texttype].append(printtext(column, secondtop + textoffset, EraFunctions.geteralabel(currentmarker, erasize)))
			outcome["axeslines"].append(printline(column, firsttop, 0, markerheight))
			outcome["axeslines"].append(printline(column, secondtop, 0, markerheight))

	return outcome


def getgraphblocks(origintimedate, erasize, boxwidth, horizontaloffset, firsttop, secondtop, graphheight, history, boxheight):

	outcome = {"brightred": [], "red": [], "orange": [], "amber": [], "yellow": [], "green": [], "blue": []}

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)

		if column >= horizontaloffset + 2:

			statusdata = historyitem.getgraphdata()
			blockcount = 0
			for colourkey in sorted(statusdata.keys()):
				if statusdata[colourkey] > 0:
					for indexer in range(0, 30): #statusdata[colourkey]):
						instruction = printrectangle(column, calculaterowposition(boxheight, firsttop, blockcount), boxwidth, boxheight)
						blockcount = blockcount + 1
						if blockcount < 21:
							outcome[colourkey[2:]].append(instruction)

			if historyitem.getuploaded() > 0:
				barheight = calculatebarheight(graphheight - 5, historyitem.getuploaded())
				print(historyitem.getuploaded(), "barheight", barheight)
				outcome['blue'].append(printrectangle(column, secondtop - barheight - 2, boxwidth, barheight))

			if historyitem.getvpnstatus() != 1:
				outcome['brightred'].append(printrectangle(column - 1, firsttop - graphheight + 1, boxwidth + 2, graphheight - 2))



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
	return (((boxwidth + 1) * EraFunctions.geteradifference(origindatetime, bardatetime, erasize)) + horizontaloffset)

def calculaterowposition(boxheight, verticaloffset, previousboxes):
	return (verticaloffset - ((boxheight + 1) * (previousboxes + 1)) - 1)

def calculatebarheight(graphheight, dataamount):
	if dataamount > 1000000000:
		limiteddata = 1000000000
	else:
		limiteddata = dataamount
	return ((graphheight * limiteddata) / 1000000000)


