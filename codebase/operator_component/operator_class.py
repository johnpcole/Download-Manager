from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper
from .delugeinterface_subcomponent import delugeinterface_module as DelugeInterface
from .configfile_subcomponent import configfile_module as FileManager
from ..common_components.thermometer_framework import thermometer_module as Thermometer


class DefineOperator:

	def __init__(self, webaddress, erasize, retrylimit):

		self.delayer = Delayer.createdelayer(erasize)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)

		self.torrentmanager = DelugeInterface.createinterface(FileManager.gettorrentconnectionconfig())




	def refresh(self):

		self.delayer.wait(5)

		datatosend = {'temperature' : Thermometer.getoveralltemperature()}
		datatosend.update(self.torrentmanager.getdelugedata())
		self.scraper.posttourl(datatosend)
		newinstructions = self.scraper.getjsonresult()
		if ('action' in newinstructions.keys()) and ('context' in newinstructions.keys()):
			newinstruction = newinstructions['action']
			instructioncontext = newinstructions['context']
		else:
			newinstruction = "Null"
			instructioncontext = "None"

		if newinstruction == "Null":
			if self.delayer.checkdelay() == True:
				newinstruction = "Refresh"
				instructioncontext = "None"
		else:
			self.delayer.reset()

		if newinstruction != "Null":
			self.torrentmanager.performdelugeaction(newinstruction, instructioncontext)

