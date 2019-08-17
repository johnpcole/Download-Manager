from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper
from .delugeinterface_subcomponent import delugeinterface_module as DelugeInterface
from .configfile_subcomponent import configfile_module as FileManager


class DefineOperator:

	def __init__(self, webaddress, erasize, retrylimit):

		self.delayer = Delayer.createdelayer(erasize)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)

		self.torrentmanager = DelugeInterface.createinterface(FileManager.gettorrentconnectionconfig())




	def refresh(self):

		self.delayer.wait(5)

		self.scraper.posttourl(self.torrentmanager.getdelugedata())
		newinstructions = self.scraper.getjsonresult()
		newinstruction = newinstructions['action']
		instructioncontext = newinstructions['context']
		if newinstruction == "Null":
			if self.delayer.checkdelay() == True:
				newinstruction = "Refresh"
				instructioncontext = "None"
		else:
			self.delayer.reset()

		if newinstruction != "Null":
			self.torrentmanager.performdelugeaction(newinstruction, instructioncontext)

