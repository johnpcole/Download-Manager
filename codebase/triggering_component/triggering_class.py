from .delayer_subcomponent import delayer_module as Delayer
from .webscraper_subcomponent import webscraper_module as WebScraper



class DefineTrigger:

	def __init__(self, webaddress, erasize):

		self.delayer = Delayer.createdelayer(erasize)

		self.scraper = WebScraper.createscraper(webaddress)


	def refresh(self):

		if self.delayer.checkdelay() == True:
			self.scraper.retrievewebpages(self.delayer.getlatestcall())
			self.delayer.waitlong()
		else:
			self.delayer.waitshort()
