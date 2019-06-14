from ..datetime_datatypes import datetime_module as DateTime
from . import delayer_privatefunctions as Functions
from time import sleep as Wait


class DefineDelayer:

	def __init__(self):

		self.latestcall = DateTime.getnow()


	def checkdelay(self):

		nowdatetime = DateTime.getnow()

		if Functions.getdatetimeera(nowdatetime) != Functions.getdatetimeera(self.latestcall):
			self.latestcall.setfromobject(nowdatetime)
			outcome = True
		else:
			outcome = False

		return outcome



	def getlatestcall(self):

		return self.latestcall.getiso()


	def waitshort(self):

		Wait(2)

	def waitlong(self):

		Wait(8)
