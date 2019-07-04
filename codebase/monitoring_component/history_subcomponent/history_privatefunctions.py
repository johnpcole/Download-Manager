from ...common_components.datetime_datatypes import eras_module as EraFunctions



def getstatusblocks(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, history, boxheight, outcome):

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add Torrent Status Blocks
			colourlist = historyitem.getgraphdata()
			indexmax = min(len(colourlist), 21)
			for index in range(0, indexmax):
				row = calculaterowposition(boxheight, graphbottom, index)
				outcome[colourlist[index]].append(printrectangle(column, row, boxwidth, boxheight))

	return outcome



def getstatusbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history, outcome):

	barmax = graphheight - 5

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add Torrent Status Blocks
			datalist = historyitem.getlonggraphdata()
			baseline = 0
			for colourindex in ['red', 'orange', 'amber', 'yellow', 'green']:
				barheight = datalist[colourindex]
				if barheight + baseline > barmax:
					barheight = barmax - baseline
				if barheight > 0:
					row = graphbottom - (baseline + barheight + 2)
					outcome[colourindex].append(printrectangle(column, row, boxwidth, barheight))
					baseline = baseline + barheight

	return outcome



def gettempbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history, outcome):

	barmax = graphheight - 5

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			baseline = -10
			for colourindex in ['darkred', 'orange', 'red']:
				baseline = baseline + 10
				blockcount = historyitem.gettemp() - baseline - 10
				if blockcount > 0.0:
					barheight = calculatetempbarheight(barmax / 3, blockcount, 10.0)
					row = graphbottom - calculatetempbarheight(barmax, baseline, 30) - barheight - 2
					outcome[colourindex].append(printrectangle(column - baseline, row, boxwidth, barheight))

	return outcome



def getgraphaxes(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphwidth, graphheight, outcome):

	#horizontal axes
	outcome["axeslines"].append(printline(horizontaloffset, graphbottom, graphwidth, 0))

	#vertical axes
	outcome["axeslines"].append(printline(horizontaloffset + 2, graphbottom, 0, 0 - graphheight))

	#vertical markers
	for indexer in [31, 61, 91, 121]:
		outcome["axeslines"].append(printline(horizontaloffset, graphbottom - indexer, 2, 0))

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

			outcome[texttype].append(printtext(column, graphbottom + textoffset, EraFunctions.geteralabel(currentmarker, erasize)))
			outcome["axeslines"].append(printline(column, graphbottom, 0, markerheight))

	return outcome



def getuploadandvpnbars(origintimedate, erasize, boxwidth, horizontaloffset, firstbottom, secondbottom, graphheight,
																									history, outcome):

	previousuploaded = 0

	if erasize == 4:
		divisor = 1.0
	elif erasize == 5:
		divisor = 6.0
	else:
		x = 1/0

	for historyitem in history:

		column = calculatecolumnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add Uploaded Delta Bar
			uploadeddelta = historyitem.getuploaded() - previousuploaded
			if uploadeddelta > 0:
				barheight = calculateuploadbarheight(graphheight - 5, uploadeddelta / divisor)
				row = secondbottom - barheight - 2
				outcome['blue'].append(printrectangle(column, row, boxwidth, barheight))

			# Add VPN Down Warning Bar
			if historyitem.getvpnstatus() != 1:
				barheight = graphheight - 2
				row = firstbottom - graphheight + 1
				outcome['brightred'].append(printrectangle(column - 1, row, boxwidth + 2, barheight))

		previousuploaded = historyitem.getuploaded()

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