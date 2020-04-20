from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper
from .delugeinterface_subcomponent import delugeinterface_module as DelugeInterface
from ..common_components.thermometer_framework import thermometer_module as Thermometer
from .network_subcomponent import network_module as VPNStatus
from ..common_components.filesystem_framework import configfile_module as ConfigFile
from .. import database_definitions as Database
import operator as Operator
from ..common_components import datetime_datatypes as DateTime


class DefineOperator:

	def __init__(self, webaddress, retrylimit):

		self.delayer = Delayer.createdelayer(4)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)

		self.torrentmanager = DelugeInterface.createinterface(ConfigFile.readconfigurationfile(
																	'./data/application_config/operator_connection.cfg',
																	['Address', 'Port', 'Username', 'Password']))

		self.actions = Database.createoperatoractionsdatabase()

		self.results = Database.createoperatorresultsdatabase()

		self.outstandingactions = []


	def refresh(self):

		self.delayer.wait(3)

		self.refreshoutstandingactions()

		newinstruction = self.getoldestinstruction()

		self.torrentmanager.performdelugeaction(newinstruction['action'], newinstruction['context'])

		if newinstruction['action'] != "Refresh":
			self.tickoffinstruction(newinstruction['actionid'])

		self.savesessiondata()



	def savesessiondata(self):

		rawdata = self.torrentmanager.getdelugedata()
		lastseen = rawdata['lastpolled']
		dataout = []
		deleter = []
		if 'torrents' in rawdata.keys():
			torrents = rawdata['torrents']
			for torrentid in torrents.keys():
				dataout.append({'recordtype': 'torrent', 'torrentid': torrentid, 'torrentstats': torrents[torrentid],
																								'lastseen': lastseen})
				deleter.append({'recordtype': 'torrent', 'torrentid': torrentid})
		if 'sessiondata' in rawdata.keys():
			session = rawdata['sessiondata']
			for sessionstat in session.keys():
				dataout.append({'recordtype': 'session', 'sessionstat': sessionstat,
															'sessionvalue': session[sessionstat], 'lastseen': lastseen})
				deleter.append({'recordtype': 'session', 'sessionstat': sessionstat})
		dataout.append({'recordtype': 'session', 'sessionstat': 'temperature',
											'sessionvalue': Thermometer.getoveralltemperature(), 'lastseen': lastseen})
		dataout.append({'recordtype': 'session', 'sessionstat': 'vpnstatus',
														'sessionvalue': VPNStatus.getvpnstatus(), 'lastseen': lastseen})
		deleter.append({'recordtype': 'session', 'sessionstat': 'temperature'})
		deleter.append({'recordtype': 'session', 'sessionstat': 'vpnstatus'})

		self.results.deletedatabaserows(deleter)
		self.results.insertdatabaserows(dataout)




	def refreshoutstandingactions(self):

		outstandingactions = []
		actiondata = self.actions.extractdatabaserows([{'recordtype': 'queuedaction'}])
		resultdata = self.results.extractdatabaserows([{'recordtype': 'actionresult'}])

		for action in actiondata:
			matchfound = False
			for result in resultdata:
				if result['actionid'] == action['actionid']:
					matchfound = True
			if matchfound is False:
				outstandingactions.append(action)

		self.outstandingactions = outstandingactions



	def getoldestinstruction(self):

		if len(self.actions) > 0:
			sortedlist = sorted(self.actions, key=Operator.itemgetter('actionid'))
			oldestinstruction = sortedlist[0]
		else:
			currentdatetime = DateTime.getnow()
			actionid = currentdatetime.getiso() + "---"
			oldestinstruction = {'actionid': actionid, 'actiontype': 'Refresh', 'context': 'None'}
		return oldestinstruction



	def tickoffinstruction(self, actionid):

		completedaction = []
		completedaction.append({'recordtype': 'processedaction', 'actionid': actionid})

		self.results.insertdatabaserows(completedaction)
