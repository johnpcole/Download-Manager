from urllib.request import urlopen as GetWebPage
from urllib.request import Request as GenerateWebRequest
from urllib.request import URLError as WebError
from time import sleep as Wait
import ssl as Security
from codebase.common_components.logging_framework import logging_module as Logging
from codebase.common_components.datetime_datatypes import datetime_module as DateTime


def getdatetimeera(datetimeobject):

	datetimetext = datetimeobject.getiso()
	return datetimetext[:13]



class DefineScraper:

	def __init__(self, webaddress):

		self.webcalltries = 1

		self.securitycontext = Security._create_unverified_context()

		self.webaddress = webaddress


	def retrievewebpages(self, datetimestamp):

		tries = 0

		Logging.printrawline("Triggering Deluge-Monitor at " + datetimestamp + "...")

		while tries < self.webcalltries:
			try:
				webresponse = {}
				webrequest = GenerateWebRequest(self.webaddress)
				rawwebresponse = GetWebPage(webrequest, context=self.securitycontext).read(1000)
				webresponse = rawwebresponse.decode("utf-8")
				tries = 99999
			except WebError as errorobject:
				tries = tries + 1
				Logging.printrawline(" -   Error Triggering Deluge-Monitor: " + errorobject.reason)

		if tries == 99999:
			Logging.printrawline(" -   Successfully Triggered Monitor: " + webresponse)
		else:
			Logging.printrawline(" -   Gave up Triggering Deluge-Monitor")




class DefineDelayer:

	def __init__(self):

		self.latestcall = DateTime.getnow()


	def checkdelay(self):

		nowdatetime = DateTime.getnow()

		if getdatetimeera(nowdatetime) != getdatetimeera(self.latestcall):
			self.latestcall.setfromobject(nowdatetime)
			outcome = True
		else:
			outcome = False

		return outcome



	def getlatestcall(self):

		return self.latestcall.getiso()



Logging.printrawline("Starting Download-Manager Application")

delayer = DefineDelayer()
scraper = DefineScraper("http://127.0.0.1:5000/Monitor")

while 1 != 0:

	if delayer.checkdelay() == True:
		scraper.retrievewebpages(delayer.getlatestcall())
		Wait(8)
	else:
		Wait(1)

Logging.printrawline("Ending Download-Manager Application")

