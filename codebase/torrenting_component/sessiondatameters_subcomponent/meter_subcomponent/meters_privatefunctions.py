import math as Maths



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

