from .....common_components.datetime_datatypes import eras_module as EraFunctions
from . import drawelements_privatefunctions as Draw
from . import calculatemetrics_privatefunctions as Calculate
from ..graph_subcomponent import graph_module as Graph


def statusblocks(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, history, boxheight):

	outcome = Graph.creategraph()

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



def statusbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = Graph.creategraph()

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



def tempbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = Graph.creategraph()

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



def graphaxes(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphwidth, graphheight):

	outcome = Graph.creategraph()

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
	while column < 1000:
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



def uploadedbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = Graph.creategraph()

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


def vpnbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history):

	outcome = Graph.creategraph()

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add VPN Down Warning Bar
			if historyitem.getvpnstatus() != 1:
				barheight = graphheight - 2
				row = graphbottom - graphheight + 1
				outcome.additem('brightred', Draw.rectangle(column - 1, row, boxwidth + 2, barheight))

	return outcome



def titles(horizontaloffset, verticaloffset, verticalspacing, graphindex):

	outcome = Graph.creategraph()

	horizontalposition = horizontaloffset + 10
	verticalposition = verticalspacing + verticaloffset - 131
	labellist = {1: 'Latest Tracker Statuses', 2: 'Latest Upload Rates', 3: 'Recent Tracker Statuses',
									4: 'Recent Upload Rates', 5: 'Recent Temperature'}

	outcome.additem('graphtitles', Draw.text(horizontalposition, verticalposition, labellist[graphindex]))

	return outcome

