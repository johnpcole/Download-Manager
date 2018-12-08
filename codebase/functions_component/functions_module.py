import math as Maths
import operator as Operators


def sortdictionary(rawdictionary, sortattribute, reverseflag):

	outcome = sorted(rawdictionary, key=Operators.attrgetter(sortattribute), reverse=reverseflag)

	return outcome



def sanitisesize(rawsize):

	if rawsize > 1000000000:
		outcome = ("%8.2f" % (int(rawsize / 10000000) * 0.01)) + " Gb"
	elif rawsize > 1000000:
		outcome = ("%8.2f" % (int(rawsize / 10000) * 0.01)) + " Mb"
	elif rawsize > 1000:
		outcome = ("%8.2f" % (int(rawsize / 10) * 0.01)) + " kb"
	else:
		outcome = str(int(rawsize)) + " b"

	return outcome


def sanitisetime(rawtime):

	if rawtime > 86400:
		outcome = ("%8.1f" % (int(rawtime / 8640) * 0.1)) + " d"
	elif rawtime > 3600:
		outcome = ("%8.1f" % (int(rawtime / 360) * 0.1)) + " h"
	elif rawtime > 60:
		outcome = ("%8.1f" % (int(rawtime / 6) * 0.1)) + " m"
	elif rawtime > 1:
		outcome = str(rawtime) + "s"
	else:
		outcome = "-"

	return outcome


def sanitisetext(rawtext):

	outcome = ""

	stringsize = len(rawtext)

	if stringsize > 0:

		if rawtext.isalnum() == True:
			outcome = rawtext

		else:

			for index in range(0, stringsize, 1):
				charitem = rawtext[index:index+1]
				charval = ord(charitem)

				if (charval >= 48) and (charval <= 57):
					outcome = outcome + charitem
				elif (charval >= 65) and (charval <= 90):
					outcome = outcome + charitem
				elif (charval >= 97) and (charval <= 122):
					outcome = outcome + charitem
				elif charval == 46:
					outcome = outcome + charitem
				else:
					outcome = outcome + "_"

	return outcome


def minifyseason(seasonname, episodename):

	episodesplit = episodename.split(" ")

	if episodesplit[0] == "Special":
		outcome = "s00"
	else:
		seasonsplit = seasonname.split(" ")
		if seasonsplit[0] == "Season":
			s = "00" + seasonsplit[1]
			outcome = "s" + s[-2:]
		elif seasonname[:7] == "Special":
			outcome = "s00"
		else:
			outcome = "-"

	return outcome



def minifyepisode(episodename):

	episodesplit = episodename.split(" ")
	if len(episodesplit) > 1:
		if episodesplit[0] == "Ep.":
			f = "00" + episodesplit[1]
			f = "e" + f[-2:]
			g = "00" + episodesplit[3]
			g = "e" + g[-2:]
			e = f + g
		else:
			e = "00" + episodesplit[1]
			e = "e" + e[-2:]
	else:
		e = episodename
	return e


def getinitial(name):

	namesplit = name.split(" ")
	if len(namesplit) > 1:
		firstword = namesplit[0]
		firstword = firstword.lower()
		if (firstword == "the") or (firstword == "a") or (firstword == "an"):
			noun = namesplit[1]
		else:
			noun = namesplit[0]
	else:
		noun = name
	outcome = noun[:1]
	if (outcome == "1") or (outcome == "2") or (outcome == "3") or (outcome == "4") or (outcome == "5"):
		outcome = "0"
	elif (outcome == "6") or (outcome == "7") or (outcome == "8") or (outcome == "9") or (outcome == "#"):
		outcome = "0"
	elif (outcome == "!") or (outcome == "$") or (outcome == "%") or (outcome == "#") or (outcome == "@"):
		outcome = "0"

	return outcome.upper()



def getmeterdata(needleangle, needlesize, needlepivot):

	decalheight = 68
	decalwidth = 121
	# Assumes the decal image is 688 x 1236 pixels big, scaled
	#1212 678
	# Needle length is 564 at 100% scaling

#	fullneedlestretch = 544.0
#	verticalratio = decalheight / 678.0
#	horizontalratio = decalwidth / 1212.0
#	verticalneedlelength = verticalratio * fullneedlestretch * needlesize
#	horizontalneedlelength = horizontalratio * fullneedlestretch * needlesize
#	verticalpivotlength = verticalratio * fullneedlestretch * needlepivot
#	horizontalpivotlength = horizontalratio * fullneedlestretch * needlepivot
#	verticalorigin = verticalratio * 74.0
#	horizontalorigin = horizontalratio * 610.0
#	verticalstart = (verticalpivotlength * Maths.sin(needleangle)) + verticalorigin
#	horizontalstart = (horizontalpivotlength * Maths.cos(needleangle)) + horizontalorigin
#	verticalfinal = (verticalneedlelength * Maths.sin(needleangle)) + verticalorigin
#	horizontalfinal = (horizontalneedlelength * Maths.cos(needleangle)) + horizontalorigin
	metersize = 58.0
	verticalorigin = 7.0
	horizontalorigin = decalwidth * 0.5
	needlestart = needlepivot * metersize
	needlefinal = needlesize * metersize
	verticalstart = (needlestart * Maths.sin(needleangle)) + verticalorigin
	horizontalstart = (needlestart * Maths.cos(needleangle)) + horizontalorigin
	verticalfinal = (needlefinal * Maths.sin(needleangle)) + verticalorigin
	horizontalfinal = (needlefinal * Maths.cos(needleangle)) + horizontalorigin

	outcome = {}
	outcome['vo'] = decalheight - verticalstart
	outcome['ho'] = decalwidth - horizontalstart
	outcome['vf'] = decalheight - verticalfinal
	outcome['hf'] = decalwidth - horizontalfinal

	return outcome



def getlogmeterangle(currentval, scale):

	if currentval < 1:
		segment = -1.0
	else:
		segment = scale * Maths.log10(currentval)
		if segment > 7.0:
			segment = 7.0

	outcome = Maths.pi * (segment + 1.0) / 8.0

	return outcome



def getlinmeterangle(currentval, scalemin, scalemax):

	fraction = (currentval - scalemin) / (scalemax - scalemin)

	if fraction < 0.0:
		fraction = 0.0
	if fraction > 1.0:
		fraction = 1.0

	outcome = Maths.pi * fraction

	return outcome



def getblockmeterangle(currentval, anglemax, blocksin180):

	blockanglesize = 180.0 / blocksin180

	blockstart = currentval * blockanglesize

	if blockstart > anglemax:
		blockstart = anglemax

	return blockstart



def getmeter2data(circleradius, startangle, endangle):

	circumference = circleradius * Maths.pi * 2.0

	filledangle = (endangle - startangle) / 360.0

	outcome = {}
	outcome['fill'] = filledangle * circumference
	outcome['gap'] = circumference - outcome['fill']
	outcome['offset'] = ((180.0 - startangle) / 360.0) * circumference

	return outcome
