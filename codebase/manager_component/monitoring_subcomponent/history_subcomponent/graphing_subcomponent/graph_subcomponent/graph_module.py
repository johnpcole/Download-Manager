from . import graph_class as GraphClass
from ......common_components.datetime_datatypes import eras_module as EraFunctions
from . import drawelements_privatefunctions as Draw
from . import calculatemetrics_privatefunctions as Calculate
from . import graphset_class as GraphSetClass


def creategraphset(size):

	return GraphSetClass.DefineGraphSet(size)


def createblank():

	return GraphClass.DefineGraph()


def createstatuslegend(horizontaloffset, graphbottom):

	outcome = createblank()
	ho = 696 + horizontaloffset
	vo = graphbottom - 134

	outcome.additem('red', Draw.rectangle(ho + 244, vo - 7, 5, 7))
	outcome.additem('graphlegends', Draw.text(ho + 254, vo, 'Other-Error'))

	outcome.additem('orange', Draw.rectangle(ho + 164, vo - 7, 5, 7))
	outcome.additem('graphlegends', Draw.text(ho + 174, vo, 'Invalid-Argument'))

	outcome.additem('amber', Draw.rectangle(ho + 103, vo - 7, 5, 7))
	outcome.additem('graphlegends', Draw.text(ho + 113, vo, 'Timed-Out'))

	outcome.additem('yellow', Draw.rectangle(ho + 46, vo - 7, 5, 7))
	outcome.additem('graphlegends', Draw.text(ho + 56, vo, 'Unknown'))

	outcome.additem('green', Draw.rectangle(ho + 0, vo - 7, 5, 7))
	outcome.additem('graphlegends', Draw.text(ho + 10, vo, 'Good'))

	return outcome




def createstatusblocks(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, history, boxheight):

	outcome = createblank()

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add Torrent Status Blocks
			colourlist = historyitem.getgraphdata()
			indexmax = min(len(colourlist), 21)
			for index in range(0, indexmax):
				row = Calculate.rowposition(boxheight, graphbottom, index)
				outcome.additem(colourlist[index], Draw.rectangle(column, row, boxwidth, boxheight))

	return outcome



def createstatusbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = createblank()

	barmax = graphheight - 5

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
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
					outcome.additem(colourindex, Draw.rectangle(column, row, boxwidth, barheight))
					baseline = baseline + barheight

	return outcome



def createtempbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = createblank()

	barmax = graphheight - 5
	tempmin = 20
	tempmax = 50
	temprange = tempmax - tempmin
	tempstep = temprange / 6
	minibarmax = barmax / 6

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			baseline = 0 - tempstep
			for colourindex in ['tempe', 'tempd', 'tempc', 'tempb', 'tempa', 'red']:
				baseline = baseline + tempstep
				blockcount = historyitem.gettemp() - baseline - tempmin
				if blockcount > 0.0:
					barheight = Calculate.barheight(minibarmax, blockcount, tempstep)
					row = graphbottom - Calculate.barheight(barmax, baseline, temprange) - barheight - 2
					outcome.additem(colourindex, Draw.rectangle(column, row, boxwidth, barheight))

	return outcome



def creategraphaxes(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphwidth, graphheight):

	outcome = createblank()

	#horizontal axes
	outcome.additem("axeslines", Draw.line(horizontaloffset, graphbottom, graphwidth, 0))

	#vertical axes
	outcome.additem("axeslines", Draw.line(horizontaloffset + 2, graphbottom, 0, 0 - graphheight))

	#vertical markers
	for indexer in [31, 61, 91, 121]:
		outcome.additem("axeslines", Draw.line(horizontaloffset, graphbottom - indexer, 2, 0))

	#horizontal markers & labels
	littlemarkergapsize = Calculate.markergapsize(erasize)
	currentmarker = Calculate.firstcurrentmarker(erasize, origintimedate)
	column = 0
	hoffset = horizontaloffset + (boxwidth / 2.0)
	while column < graphwidth:
		currentmarker.adjusthours(littlemarkergapsize)
		column = Calculate.columnposition(boxwidth, hoffset, origintimedate, currentmarker, erasize)
		if column >= horizontaloffset + 2:

			if Calculate.markertype(erasize, currentmarker) == "Big":
				markerheight = 4
				texttype = "biglabels"
				textoffset = 16
			else:
				markerheight = 2
				texttype = "littlelabels"
				textoffset = 12

			markerlabel = EraFunctions.geteralabel(currentmarker, erasize)
			outcome.additem(texttype, Draw.text(column, graphbottom + textoffset, markerlabel))
			outcome.additem("axeslines", Draw.line(column, graphbottom, 0, markerheight))

	return outcome



def createuploadedbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = createblank()

	previousuploaded = 0
	divisor = Calculate.barscaling(erasize)

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add Uploaded Delta Bar
			uploadeddelta = historyitem.getuploaded() - previousuploaded
			if uploadeddelta > 0:
				barheight = Calculate.barheight(graphheight - 5, uploadeddelta / divisor, 1000000000)
				row = graphbottom - barheight - 2
				outcome.additem('blue', Draw.rectangle(column, row, boxwidth, barheight))

		previousuploaded = historyitem.getuploaded()

	return outcome


def createvpnbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = createblank()

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add VPN Down Warning Bar
			if historyitem.getvpnstatus() != 1:
				barheight = graphheight - 2
				row = graphbottom - graphheight + 1
				outcome.additem('brightred', Draw.rectangle(column - 1, row, boxwidth + 2, barheight))

	return outcome



def createtitles(longhistorymode, horizontaloffset, verticaloffset, verticalspacing, graphindex):

	outcome = createblank()

	horizontalposition = horizontaloffset + 10
	verticalposition = verticalspacing + verticaloffset - 131
	labellist = {1: 'Tracker Statuses', 2: 'Upload Rate', 0: 'Temperature'}
	if longhistorymode == True:
		labeltext = 'Latest '
	else:
		labeltext = 'Recent '

	outcome.additem('graphtitles', Draw.text(horizontalposition, verticalposition, labeltext +
																							labellist[graphindex % 3]))

	return outcome


