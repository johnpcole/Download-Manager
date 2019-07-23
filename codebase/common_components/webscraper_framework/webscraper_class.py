from urllib.request import urlopen as GetWebPage
from urllib.request import Request as GenerateWebRequest
from urllib.request import URLError as WebError
#from urllib.parse import urlencode as GeneratePostData
import ssl as Security
from ...common_components.logging_framework import logging_module as Logging
from ..datetime_datatypes import datetime_module as DateTime
from json import loads as ReadJson
from json import dumps as MakeJson



class DefineScraper:

	def __init__(self, webaddress, retrylimit):

		self.webcalltries = retrylimit

		self.securitycontext = Security._create_unverified_context()

		self.webaddress = GenerateWebRequest(webaddress)

		self.latestresult = {}

		self.latestdatetime = DateTime.getnow()


	def performwebcall(self, webaddress, datadictionary):

		tries = 0

		#Logging.printrawline("Triggering Deluge-Monitor at " + datetimestamp + "...")

		while tries < self.webcalltries:
			try:
				if datadictionary is None:
					rawwebresponse = GetWebPage(webaddress, context=self.securitycontext).read(1000)
				else:
					unencodedpostdata = MakeJson(datadictionary)
					postdata = unencodedpostdata.encode("ascii")
					rawwebresponse = GetWebPage(webaddress, context=self.securitycontext, data=postdata).read(1000)
				webresponse = rawwebresponse.decode("utf-8")
				tries = 99999
				self.latestresult = webresponse
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

		self.performwebcall(self.webaddress, None)

	def posttourl(self, datadictionary):

		addresswithheader = self.webaddress
		addresswithheader.add_header('Content-Type', 'application/json')

		self.performwebcall(addresswithheader, datadictionary)

	def getwebresult(self):

		return self.latestresult

	def getjsonresult(self):

		return ReadJson(self.latestresult)

