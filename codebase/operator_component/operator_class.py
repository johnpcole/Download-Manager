from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper
from .delugeinterface_subcomponent import delugeinterface_module as DelugeInterface
from ..common_components.thermometer_framework import thermometer_module as Thermometer
from .network_subcomponent import network_module as VPNStatus
from ..common_components.filesystem_framework import configfile_module as ConfigFile



class DefineOperator:

	def __init__(self, webaddress, erasize, retrylimit):

		self.delayer = Delayer.createdelayer(erasize)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)

		self.torrentmanager = DelugeInterface.createinterface(ConfigFile.readconfigurationfile(
																	'./data/application_config/operator_connection.cfg',
																	['Address', 'Port', 'Username', 'Password']))




	def refresh(self):

		self.delayer.wait(5)

		self.scraper.posttourl(self.generatereturndata())
		monitormode = self.delayer.checkdelay()
		print("==================================================")
		print("==================================================")
		print("Latest Instruction from Manager: ", self.scraper.getjsonresult())
		print("==================================================")
		newinstructions = self.sanitiseinstructions(self.scraper.getjsonresult(), monitormode)

		if newinstructions['action'] != "Null":
			print("Requested Action: ", newinstructions['action'], ", On :", newinstructions['context'], ", Monitor:", monitormode)
			self.torrentmanager.performdelugeaction(newinstructions['action'], newinstructions['context'], monitormode)
		else:
			print("Remaining Dormant")
			self.torrentmanager.blankdata()
		print("==================================================")
		print("==================================================")


	def generatereturndata(self):

		datatosend = self.torrentmanager.getdelugedata()
		if 'sessiondata' in datatosend.keys():
			datatosend['sessiondata'].update({'temperature': Thermometer.getoveralltemperature()})
			datatosend['sessiondata'].update({'vpnstatus': VPNStatus.getvpnstatus()})
		return datatosend


	def sanitiseinstructions(self, instructionset, monitormode):

		outcome = {'action': "Null", 'context': "None"}

		if ('action' in instructionset.keys()) and ('context' in instructionset.keys()):
			outcome['action'] = instructionset['action']
			outcome['context'] = instructionset['context']

		if (outcome['action'] == "Null") and (monitormode is True):
			outcome['action'] = "Refresh"
			outcome['context'] = "None"

		return outcome



