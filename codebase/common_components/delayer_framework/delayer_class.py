from ...common_components.datetime_datatypes import datetime_module as DateTime
from ...common_components.datetime_datatypes import eras_module as EraFunctions
from time import sleep as Wait


class DefineDelayer:

	def __init__(self, eraflag):

		self.latestcall = DateTime.getnow()

		self.erasize = eraflag



	def checkdelay(self):

		nowdatetime = DateTime.getnow()

		if EraFunctions.compareeras(nowdatetime, self.latestcall, self.erasize) == False:
			self.latestcall.setfromobject(nowdatetime)
			outcome = True
		else:
			outcome = False

		return outcome



	def getlatestcall(self):

		return self.latestcall.getiso()



	def waitshort(self):

		if self.erasize > 1:
			Wait(1)



	def waitlong(self):

		if self.erasize == 4:
			Wait(598)
		elif self.erasize == 3:
			Wait(58)
		elif self.erasize == 2:
			Wait(8)


	def wait(self, seconds):

		Wait(seconds)

