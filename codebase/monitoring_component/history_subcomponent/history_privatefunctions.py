from ...common_components.datetime_datatypes import eras_module as EraFunctions



def getgraphblocks(origintimedate, erasize, boxwidth, horizontaloffset, firsttop, secondtop, graphheight, history, boxheight, outcome):

	previousuploaded = 0

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add Torrent Status Blocks
			colourlist = historyitem.getgraphdata()
			indexmax = min(len(colourlist), 21)
			for index in range(0, indexmax):
				outcome[colourlist[index]].append(printrectangle(column, calculaterowposition(boxheight, firsttop,
																						index), boxwidth, boxheight))

			# Add Uploaded Delta Bar
			uploadeddelta = historyitem.getuploaded() - previousuploaded
			if uploadeddelta > 0:
				barheight = calculateuploadbarheight(graphheight - 5, uploadeddelta)
				outcome['blue'].append(printrectangle(column, secondtop - barheight - 2, boxwidth, barheight))


			# Add VPN Down Warning Bar
			if historyitem.getvpnstatus() != 1:
				outcome['brightred'].append(printrectangle(column - 1, firsttop - graphheight + 1, boxwidth + 2, graphheight - 2))

		previousuploaded = historyitem.getuploaded()

	return outcome



def getlonggraphblocks(origintimedate, erasize, boxwidth, horizontaloffset, firsttop, secondtop, graphheight, history, outcome):

	previousuploaded = 0

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:
			# Add Torrent Status Blocks
			datalist = historyitem.getlonggraphdata()
			baseline = 0
			for colourindex in ['red', 'orange', 'amber', 'yellow', 'green']:
				barheight = datalist[colourindex]
				if barheight + baseline > 120:
					barheight = 120 - baseline
				if barheight > 0:
					outcome[colourindex].append(printrectangle(column, firsttop - (baseline + barheight + 2), boxwidth, barheight))
					baseline = baseline + barheight

			# Add Uploaded Delta Bar
			uploadeddelta = historyitem.getuploaded() - previousuploaded
			if uploadeddelta > 0:
				barheight = calculateuploadbarheight(graphheight - 5, uploadeddelta / 6.0)
				outcome['blue'].append(printrectangle(column, secondtop - barheight - 2, boxwidth, barheight))


			# Add VPN Down Warning Bar
			if historyitem.getvpnstatus() != 1:
				outcome['brightred'].append(printrectangle(column - 1, firsttop - graphheight + 1, boxwidth + 2, graphheight - 2))

		previousuploaded = historyitem.getuploaded()

	return outcome


def gettempgraphblocks(origintimedate, erasize, boxwidth, horizontaloffset, firsttop, graphheight, history, outcome):

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			blockcount = historyitem.gettemp() - 10.0
			for colourindex in ['amber', 'orange', 'red']:
				blockcount = blockcount - 10.0
				if blockcount > 0.0:
					barheight = calculatetempbarheight(graphheight, blockcount, 10.0)
					outcome[colourindex].append(printrectangle(column, firsttop - barheight, boxwidth, barheight))

	return outcome




def getgraphaxes(origintimedate, erasize, boxwidth, horizontaloffset, graphtop, graphwidth, graphheight, outcome):

	#horizontal axes
	outcome["axeslines"].append(printline(horizontaloffset, graphtop, graphwidth, 0))

	#vertical axes
	outcome["axeslines"].append(printline(horizontaloffset + 2, graphtop, 0, 0 - graphheight))

	#vertical markers
	for indexer in [31, 61, 91, 121]:
		outcome["axeslines"].append(printline(horizontaloffset, graphtop - indexer, 2, 0))

	#horizontal markers
	if erasize == 4:
		baselineerasize = 5
		baselineadjuster = -1
		bigmarkergap = 10800
		littlemarkergap = 1
	elif erasize == 5:
		baselineerasize = 7
		baselineadjuster = -24
		bigmarkergap = 86400
		littlemarkergap = 6
	else:
		x = 1/0

	currentmarker = EraFunctions.geteraasobject(origintimedate, baselineerasize)
	currentmarker.adjusthours(baselineadjuster)
	column = 0
	hoffset = horizontaloffset + (boxwidth / 2.0)
	while column < 1000:
		currentmarker.adjusthours(littlemarkergap)
		column = calculatecolumnposition(boxwidth, hoffset, origintimedate, currentmarker, erasize)
		if column >= horizontaloffset + 2:

			if (currentmarker.gettimevalue() % bigmarkergap) == 0:
				markerheight = 4
				texttype = "biglabels"
				textoffset = 16
			else:
				markerheight = 2
				texttype = "littlelabels"
				textoffset = 12

			outcome[texttype].append(printtext(column, graphtop + textoffset, EraFunctions.geteralabel(currentmarker, erasize)))
			outcome["axeslines"].append(printline(column, graphtop, 0, markerheight))

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

def calculateuploadbarheight(graphheight, dataamount):
	return ((graphheight * min(dataamount, 1000000000)) / 1000000000)

def calculatetempbarheight(graphheight, temperature, temperaturerange):
	return ((graphheight * min(temperature, temperaturerange)) / temperaturerange)