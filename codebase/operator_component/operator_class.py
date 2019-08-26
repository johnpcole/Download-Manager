from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper
from .delugeinterface_subcomponent import delugeinterface_module as DelugeInterface
from .configfile_subcomponent import configfile_module as FileManager
from ..common_components.thermometer_framework import thermometer_module as Thermometer
from .network_subcomponent import network_module as VPNStatus


class DefineOperator:

	def __init__(self, webaddress, erasize, retrylimit):

		self.delayer = Delayer.createdelayer(erasize)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)

		self.torrentmanager = DelugeInterface.createinterface(FileManager.gettorrentconnectionconfig())




	def refresh(self):

		self.delayer.wait(5)

		self.scraper.posttourl(self.generatereturndata())
		newinstructions = self.sanitiseinstructions(self.scraper.getjsonresult())

		if newinstructions['action'] == "Null":
			newinstructions['context'] = "None"
			if self.delayer.checkdelay() == True:
				newinstructions['action'] = "Monitor-History"

		if newinstructions['action'] != "Null":
			self.torrentmanager.performdelugeaction(newinstructions['action'], newinstructions['context'])
		else:
			self.torrentmanager.blankdata()


	def generatereturndata(self):

		datatosend = self.torrentmanager.getdelugedata()
		datatosend['sessiondata'].update({'temperature': Thermometer.getoveralltemperature()})
		datatosend['sessiondata'].update({'vpnstatus': VPNStatus.getvpnstatus()})


	def sanitiseinstructions(self, instructionset):

		outcome = {'action': "Null", 'context': "None"}
		if ('action' in instructionset.keys()) and ('context' in instructionset.keys()):
			outcome['action'] = instructionset['action']
			outcome['context'] = instructionset['context']

		return outcome



