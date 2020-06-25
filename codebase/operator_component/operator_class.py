from .delugeinterface_subcomponent import delugeinterface_module as DelugeInterface
from ..common_components.thermometer_framework import thermometer_module as Thermometer
from .network_subcomponent import network_module as VPNStatus
from ..common_components.queue_framework import queue_module as Queue
from ..common_components.delayer_framework import delayer_module as Delayer
from ..common_components.filesystem_framework import filesystem_module as FileSystem


class DefineOperator:

	def __init__(self, operatorqueuelocation, sessiondataqueuelocation, operatorconfiglocation, historydatalocation):

		self.torrentmanager = DelugeInterface.createinterface(FileSystem.readjsonfromdisk(operatorconfiglocation))

		self.actions = Queue.createqueuereader(operatorqueuelocation)

		self.results = Queue.createqueuewriter(sessiondataqueuelocation, 1)

		self.historypath = historydatalocation

		self.historytrigger = Delayer.createdelayer(4)



	def refresh(self):

		self.historytrigger.wait(5)

		self.performaction()

		temperature = Thermometer.getoveralltemperature()
		vpnstatus = VPNStatus.getvpnstatus()

		self.savesessiondata(temperature, vpnstatus)

		if self.historytrigger.checkdelay() is True:
			self.savehistorydata(temperature, vpnstatus)




	def performaction(self):

		newinstruction = self.actions.readfromqueue()
		if newinstruction is not None:
			self.torrentmanager.performdelugeaction(newinstruction['actiontype'], newinstruction['context'])




	def savesessiondata(self, temperature, vpnstatus):

		rawdata = self.torrentmanager.getdelugedata()
		rawdata['sessiondata']['temperature'] = temperature
		rawdata['sessiondata']['vpnstatus'] = vpnstatus
		self.results.createqueueditem(rawdata)




	def savehistorydata(self, temperature, vpnstatus):

		fullfilepath = FileSystem.concatenatepaths(self.historypath, self.historytrigger.getlatestcallera())
		rawdata = self.torrentmanager.gethistorydata()
		rawdata['temperature'] = temperature
		rawdata['vpnstatus'] = vpnstatus
		FileSystem.writejsontodisk(fullfilepath + ".draft", rawdata)
		FileSystem.movefile(fullfilepath + ".draft", fullfilepath + ".queued")

