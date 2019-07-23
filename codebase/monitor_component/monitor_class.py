from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper



class DefineTrigger:

	def __init__(self, webaddress, erasize, retrylimit):

		self.delayer = Delayer.createdelayer(erasize)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)


	def refresh(self):

		if self.delayer.checkdelay() == True:
			self.scraper.retrievewebpage()
			self.delayer.waitlong()
		else:
			self.delayer.waitshort()
