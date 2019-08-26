import math as Maths
from . import meters_privatefunctions as MeterFunctions

class DefinePointerMeter:

	def __init__(self, metermin, metermax, needletype):

		self.datavalue = 0

		self.metermin = metermin

		self.metermax = metermax

		self.needletype = needletype



	def setmetervalue(self, newvalue):

		self.datavalue = newvalue



	def getmeterdata(self):

		if self.metermin < -999:
			needleangle = MeterFunctions.getlogmeterangle(self.datavalue, self.metermax)
		else:
			needleangle = MeterFunctions.getlinmeterangle(self.datavalue, self.metermin, self.metermax)

		decalheight = 68
		decalwidth = 121

		needlepivot = 0.45 #Fraction of decal size the the middle of the needle is missing

		if self.needletype == "Long":
			needlesize = 0.9
		else:
			needlesize = 0.75

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


	def getmetervalue(self):

		return self.datavalue



