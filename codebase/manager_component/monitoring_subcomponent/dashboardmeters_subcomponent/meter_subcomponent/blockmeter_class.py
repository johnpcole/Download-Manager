import math as Maths
from . import meters_privatefunctions as MeterFunctions

class DefineBlockMeter:

	def __init__(self, metertype):

		self.datavalue = 0

		self.metertype = metertype

		self.endangle = 185.0

		self.countermax = 9.5

		if self.metertype == "Outer":
			self.circleradius = 49.5
		else:
			self.circleradius = 36.5

		self.circumference = self.circleradius * Maths.pi * 2.0

	def setmetervalue(self, newvalue):

		self.datavalue = newvalue



	def getmeterdata(self):

		return self.generatemeterdata(self.datavalue)


	def getdummydata(self):

		return self.generatemeterdata(0)


	def generatemeterdata(self, countervalue):

		startangle = MeterFunctions.getblockmeterangle(countervalue, self.endangle, self.countermax)

		filledangle = (self.endangle - startangle) / 360.0

		outcome = {}
		outcome['fill'] = filledangle * self.circumference
		outcome['gap'] = self.circumference - outcome['fill']
		outcome['offset'] = ((180.0 - startangle) / 360.0) * self.circumference

		return outcome





