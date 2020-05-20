from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.webscraper_framework import webscraper_module as WebScraper
from .delugeinterface_subcomponent import delugeinterface_module as DelugeInterface
from ..common_components.thermometer_framework import thermometer_module as Thermometer
from .network_subcomponent import network_module as VPNStatus
from ..common_components.filesystem_framework import configfile_module as ConfigFile
from .. import database_definitions as Database
import operator as Operator
from ..common_components.datetime_datatypes import datetime_module as DateTime
from json import dumps as MakeJson


class DefineOperator:

	def __init__(self, webaddress, retrylimit):

		self.delayer = Delayer.createdelayer(4)

		self.scraper = WebScraper.createscraper(webaddress, retrylimit)

		self.torrentmanager = DelugeInterface.createinterface(ConfigFile.readconfigurationfile(
																	'./data/application_config/operator_connection.cfg',
																	['Address', 'Port', 'Username', 'Password']))

		self.actions = Database.createoperatoractionsdatabase(2)

		self.results = Database.createoperatorresultsdatabase(1)

		self.outstandingactions = []


	def refresh(self):

		self.delayer.wait(5)

		self.refreshoutstandingactions()

		newinstruction = self.getoldestinstruction()

		self.torrentmanager.performdelugeaction(newinstruction['actiontype'], newinstruction['context'])

		if newinstruction['actiontype'] != "Refresh":
			self.tickoffinstruction(newinstruction['actionid'])

		self.savesessiondata()



	def savesessiondata(self):

		rawdata = self.torrentmanager.getdelugedata()

		if 'torrents' in rawdata.keys():
			lastseen = rawdata['lastpolled']
			dataout = []
			deleter = []
			torrents = rawdata['torrents']
			for torrentid in torrents.keys():
				dataout.append({'recordtype': 'torrent', 'torrentid': torrentid,
												'torrentstats': MakeJson(torrents[torrentid]), 'lastseen': lastseen})
				deleter.append({'recordtype': 'torrent', 'torrentid': torrentid})

			if 'sessiondata' in rawdata.keys():
				session = rawdata['sessiondata']
				for sessionstat in session.keys():
					dataout.append({'recordtype': 'session', 'sessionstat': sessionstat,
																				'sessionvalue': session[sessionstat]})
			dataout.append({'recordtype': 'session', 'sessionstat': 'temperature',
																'sessionvalue': Thermometer.getoveralltemperature()})
			dataout.append({'recordtype': 'session', 'sessionstat': 'vpnstatus',
																			'sessionvalue': VPNStatus.getvpnstatus()})
			dataout.append({'recordtype': 'session', 'sessionstat': 'lastseen', 'sessionvalue': lastseen})

			deleter.append({'recordtype': 'session'})

			self.results.deletedatabaserows(deleter)
			self.results.insertdatabaserows(dataout)



	def clearmissingtorrents(self):

		deleter = []

		dataset = []
		dataset.append({'recordtype': 'torrent'})
		currentlsting = self.results.extractdatabaserows(dataset)
		for currentitem in currentlsting:
			if self.isdeleted(currentitem['lastseen']) is True:
				deleter.append({'recordtype': 'torrent', 'torrentid': currentitem['torrentid']})
				print("Deleting Torrent From Database: ", currentitem['torrentid'])

		self.results.deletedatabaserows(deleter)



	def isdeleted(self, lastseen):

		reallastseen = DateTime.createfromiso(lastseen)
		timedifference = DateTime.timedifferenceasduration(reallastseen, DateTime.getnow())
		if abs(timedifference.getsecondsvalue()) > 30:
			outcome = True
		else:
			outcome = False

		return outcome



	def refreshoutstandingactions(self):

		outstandingactions = []
		actiondata = self.actions.extractdatabaserows([{'recordtype': 'queuedaction'}])
		resultdata = self.results.extractdatabaserows([{'recordtype': 'processedaction'}])

		for action in actiondata:
			matchfound = False
			for result in resultdata:
				if result['actionid'] == action['actionid']:
					matchfound = True
			if matchfound is False:
				outstandingactions.append(action)

		self.outstandingactions = outstandingactions



	def getoldestinstruction(self):

		if len(self.outstandingactions) > 0:
			sortedlist = sorted(self.outstandingactions, key=Operator.itemgetter('actionid'))
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
