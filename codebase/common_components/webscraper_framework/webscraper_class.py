from urllib.request import urlopen as GetWebPage
from urllib.request import Request as GenerateWebRequest
from urllib.request import URLError as WebError
from urllib.parse import urlencode as GeneratePostData
import ssl as Security
from ...common_components.logging_framework import logging_module as Logging
from ..datetime_datatypes import datetime_module as DateTime

class DefineScraper:

	def __init__(self, webaddress, retrylimit):

		self.webcalltries = retrylimit

		self.securitycontext = Security._create_unverified_context()

		self.webaddress = GenerateWebRequest(webaddress)

		self.latestresult = {}

		self.latestdatetime = DateTime.getnow()


	def performwebcall(self, datadictionary):

		tries = 0

		#Logging.printrawline("Triggering Deluge-Monitor at " + datetimestamp + "...")

		while tries < self.webcalltries:
			try:
				webresponse = {}
				if datadictionary is None:
					rawwebresponse = GetWebPage(self.webaddress, context=self.securitycontext).read(1000)
				else:
					postdata = GeneratePostData(datadictionary)
					rawwebresponse = GetWebPage(self.webaddress, context=self.securitycontext, data=postdata).read(1000)
				webresponse = rawwebresponse.decode("utf-8")
				tries = 99999
				self.latestresult = webresponse.copy()
				self.latestdatetime = DateTime.getnow()
			except WebError as errorobject:
				tries = tries + 1
				#Logging.printrawline(" -   Error Triggering Deluge-Monitor: " + errorobject.reason)


		if tries != 99999:
			currentdatetime = DateTime.getnow()
			Logging.printrawline(" -   Gave up Triggering Deluge-Monitor at " + currentdatetime.getiso())
		#else:
			#Logging.printrawline(" -   Successfully Triggered Monitor: " + webresponse)



	def retrievewebpage(self):

		self.performwebcall(None)

	def posttourl(self, datadictionary):

		self.performwebcall(datadictionary)

	def getwebresult(self):

		return self.latestresult
