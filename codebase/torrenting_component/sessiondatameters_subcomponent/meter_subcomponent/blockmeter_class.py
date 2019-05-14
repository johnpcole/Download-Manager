import math as Maths
from . import meters_privatefunctions as MeterFunctions

class DefineBlockMeter:

	def __init__(self, metertype):

		self.datavalue = 0

		self.metertype = metertype



	def setmetervalue(self, newvalue):

		self.datavalue = newvalue



	def getmeterdata(self):

		endangle = 185.0
		countermax = 9.5

		startangle = MeterFunctions.getblockmeterangle(self.datavalue, endangle, countermax)

		if self.metertype == "Outer":
			circleradius = 49.5
		else:
			circleradius = 36.5

		circumference = circleradius * Maths.pi * 2.0

		filledangle = (endangle - startangle) / 360.0

		outcome = {}
		outcome['fill'] = filledangle * circumference
		outcome['gap'] = circumference - outcome['fill']
		outcome['offset'] = ((180.0 - startangle) / 360.0) * circumference

		return outcome
