from urllib.request import urlopen as GetWebPage
from urllib.request import Request as GenerateWebRequest
from urllib.request import URLError as WebError
import ssl as Security
from codebase.common_components.logging_framework import logging_module as Logging


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
