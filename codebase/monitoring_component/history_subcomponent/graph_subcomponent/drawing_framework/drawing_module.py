from .....common_components.datetime_datatypes import eras_module as EraFunctions
from . import drawelements_privatefunctions as Draw
from . import calculatemetrics_privatefunctions as Calculate


def statusblocks(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, history, boxheight, originalgraph):

	outcome = originalgraph.copy()

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add Torrent Status Blocks
			colourlist = historyitem.getgraphdata()
			indexmax = min(len(colourlist), 21)
			for index in range(0, indexmax):
				row = Calculate.rowposition(boxheight, graphbottom, index)
				outcome[colourlist[index]].append(Draw.rectangle(column, row, boxwidth, boxheight))

	return outcome



def statusbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history, originalgraph):

	outcome = originalgraph.copy()

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
					outcome[colourindex].append(Draw.rectangle(column, row, boxwidth, barheight))
					baseline = baseline + barheight

	return outcome



def tempbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history, originalgraph):

	outcome = originalgraph.copy()

	barmax = graphheight - 5
	tempmin = 20
	tempmax = 30 #50
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
					outcome[colourindex].append(Draw.rectangle(column, row, boxwidth, barheight))

	return outcome



def graphaxes(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphwidth, graphheight, originalgraph):

	outcome = originalgraph.copy()

	#horizontal axes
	outcome["axeslines"].append(Draw.line(horizontaloffset, graphbottom, graphwidth, 0))

	#vertical axes
	outcome["axeslines"].append(Draw.line(horizontaloffset + 2, graphbottom, 0, 0 - graphheight))

	#vertical markers
	for indexer in [31, 61, 91, 121]:
		outcome["axeslines"].append(Draw.line(horizontaloffset, graphbottom - indexer, 2, 0))

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
			outcome[texttype].append(Draw.text(column, graphbottom + textoffset, markerlabel))
			outcome["axeslines"].append(Draw.line(column, graphbottom, 0, markerheight))

	return outcome



def uploadedbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history, originalgraph):

	outcome = originalgraph.copy()

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
				outcome['blue'].append(Draw.rectangle(column, row, boxwidth, barheight))

		previousuploaded = historyitem.getuploaded()

	return outcome


def vpnbars(origintimedate, erasize, boxwidth, horizontaloffset, graphbottom, graphheight, history, originalgraph):

	outcome = originalgraph.copy()

	for historyitem in history:

		column = Calculate.columnposition(boxwidth, horizontaloffset, origintimedate, historyitem.getdatetime(), erasize)
		if column >= horizontaloffset + 2:

			# Add VPN Down Warning Bar
			if historyitem.getvpnstatus() != 1:
				barheight = graphheight - 2
				row = graphbottom - graphheight + 1
				outcome['brightred'].append(Draw.rectangle(column - 1, row, boxwidth + 2, barheight))

	return outcome



def titles(horizontaloffset, verticaloffset, verticalspacing, originalgraph):

	outcome = originalgraph.copy()

	horizontalposition = horizontaloffset + 10
	verticalposition = verticalspacing + verticaloffset - 131
	graphindex = 0
	for label in ['Latest Tracker Statuses', 'Latest Upload Rates', 'Recent Tracker Statuses', 'Recent Upload Rates',
																								'Recent Temperature']:
		#verticalposition = verticalposition + verticalspacing
		graphindex = graphindex + 1
		outcome[graphindex]['graphtitles'].append(Draw.text(horizontalposition, verticalposition, label))

	return outcome


